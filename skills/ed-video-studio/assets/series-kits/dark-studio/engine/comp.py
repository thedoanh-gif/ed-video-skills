# -*- coding: utf-8 -*-
"""Bộ dựng Dark Studio · Nắng sớm: dữ liệu, màu, lớp Comp (mốc giờ theo lời, phần tử, chuyển động, xuất file).

Chép các file trong engine/ vào thư mục dự án. Cần có: script-voice.txt, audio/<chương>.words.json, hf/ (đã init).
data.json là tùy chọn: {"nhap": {"nam": 2026, "nhan_gia_lap": "có", "chan_trang": "..."}, "tinh": {...}}.
Dòng chữ ở chân khung: data "chan_trang", hoặc gán comp.FOOTER trong build.py."""
import json, math, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.stdout.reconfigure(encoding="utf-8")
_DATA = ROOT / "data.json"
DATA = json.loads(_DATA.read_text(encoding="utf-8")) if _DATA.exists() else {}
D, X = DATA.get("nhap", {}), DATA.get("tinh", {})
Y = D.get("nam", "")
FAKE = str(D.get("nhan_gia_lap", "")).lower().startswith("c")   # hiện nhãn "NỘI DUNG GIẢ LẬP"
FOOTER = D.get("chan_trang", "")
TAIL = 0.6      # nhịp thở cuối mỗi chương
INTRO = 4.0

YEL, BLUE, GREEN, PINK = "#F59E0B", "#60A5FA", "#34D399", "#FB7185"
INK, MUTE = "#F5F7FA", "#AEB8CC"
PANEL = {"mo": ("#1E2A44", "#141D33"), "p1": ("#1B2C4D", "#121C34"), "p2": ("#34251A", "#221811"),
         "p3": ("#17342C", "#0F231E"), "p4": ("#2B2046", "#1C152F")}


def vn(x, nd=1):
    x = round(float(x), nd)
    if x.is_integer():
        return f"{int(x):,}".replace(",", ".")
    a, b = f"{x:,.{nd}f}".split(".")
    return a.replace(",", ".") + "," + b


def media_dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout)


def load_voice():
    """{"CH01": [dòng, ...]} từ script-voice.txt (bỏ dòng [nghỉ])."""
    out, cur = {}, None
    for line in (ROOT / "script-voice.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("###"):
            cur = line.split()[1]
            out[cur] = []
        elif cur and line and line != "[nghỉ]":
            out[cur].append(line)
    return out


VOICE = load_voice()


class Comp:
    def __init__(self, cid, dur, panel, label):
        self.id, self.dur, self.panel, self.label = cid, round(dur, 3), panel, label
        self.html, self.js, self.sfx, self.n = [], [], [], 0
        wf = ROOT / "audio" / f"{cid}.words.json"
        self.words = json.loads(wf.read_text(encoding="utf-8")) if wf.exists() else []
        self.lines = self._lines()

    # ---------- mốc giờ theo dòng lời (không phụ thuộc nội dung dữ liệu)
    def _lines(self):
        """Chia lời của chương: dòng -> đoạn (ngăn bởi dấu câu) -> vị trí từ trong words.json.
        Đồng thời bắt lỗi giọng cũ: lời đã đổi mà chưa tạo lại giọng."""
        block = VOICE.get(self.id.upper())
        if block is None:
            return []
        out, k = [], 0
        for line in block:
            segs = []
            for seg in re.split(r"[,:;.?!“”]+", line):
                toks = re.findall(r"\w+", seg)
                if not toks:
                    continue
                segs.append(k)
                for tok in toks:
                    if k >= len(self.words) or tok.lower() != re.sub(r"\W", "", self.words[k]["word"]).lower():
                        raise SystemExit(f"LỖI: giọng đọc {self.id} không khớp lời mới (từ '{tok}'). "
                                         f"Tạo lại giọng: tts_vi.py script-voice.txt --only {self.id}")
                    k += 1
            out.append(segs)
        if k != len(self.words):
            raise SystemExit(f"LỖI: giọng đọc {self.id} dài hơn lời mới. Tạo lại giọng chương này.")
        return out

    def L(self, i, j=0, lag=0.05):
        """Giây bắt đầu đoạn j của dòng lời i (i âm = tính từ cuối)."""
        segs = self.lines[i]
        return round(self.words[segs[min(j, len(segs) - 1)]]["start"] + lag, 2)

    def type(self, i, t, dur):
        """Gõ dần: phần tử i chứa các <span class="ch">."""
        self.js.append(f'typeIn("#{i} .ch",{round(t, 2)},{round(dur, 2)});')

    # ---------- mốc giờ theo lời
    def A(self, word, after=0.0, lag=0.05):
        for w in self.words:
            if w["word"].lower() == word.lower() and w["start"] >= after - 0.02:
                return round(w["start"] + lag, 2)
        raise SystemExit(f"LỖI: không thấy từ '{word}' sau giây {after} trong {self.id}")

    def N(self, word, after=0.0, lag=0.05):
        """Giây của từ đứng NGAY SAU một từ cố định: dùng khi từ cần bắt là con số (đổi theo dữ liệu)."""
        for k, w in enumerate(self.words[:-1]):
            if w["word"].lower() == word.lower() and w["start"] >= after - 0.02:
                return round(self.words[k + 1]["start"] + lag, 2)
        raise SystemExit(f"LỖI: không thấy từ '{word}' sau giây {after} trong {self.id}")

    def uid(self):
        self.n += 1
        return f"{self.id}-e{self.n}"

    def cue(self, t, name):
        self.sfx.append((t, name))

    # ---------- phần tử tĩnh trong HTML
    def box(self, x, y, w=None, h=None, inner="", cls="", style="", attrs=""):
        i = self.uid()
        s = f"left:{x}px;top:{y}px;"
        if w is not None:
            s += f"width:{w}px;"
        if h is not None:
            s += f"height:{h}px;"
        self.html.append(f'<div id="{i}" class="el {cls}" style="{s}{style}" {attrs}>{inner}</div>')
        return i

    def text(self, x, y, s, size=56, w=None, color=INK, weight=700, align="left", extra=""):
        st = f"font-size:{size}px;color:{color};font-weight:{weight};text-align:{align};line-height:1.12;"
        if w is None:
            st += "white-space:nowrap;"
        return self.box(x, y, w, None, s, "", st + extra)

    def open_scene(self, t0, t1=None):
        i = self.uid()
        self.html.append(f'<div id="{i}" class="scene" data-layout-allow-overflow>')
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:.22,ease:"power1.out"}},{t0});')
        if t1 is not None:
            self.js.append(f'tl.to("#{i}",{{opacity:0,y:-12,duration:.22,ease:"power2.in"}},{round(t1 - .23, 2)});')

    def close_scene(self):
        self.html.append("</div>")

    # ---------- chuyển động
    def tw(self, i, t, frm, to):
        self.js.append(f'tl.fromTo("#{i}",{json.dumps(frm)},{json.dumps(to)},{round(t, 2)});')

    def enter(self, i, t, how="up", dur=.5):
        frm = {"up": {"opacity": 0, "y": 28, "scale": .97}, "pop": {"opacity": 0, "scale": .6},
               "left": {"opacity": 0, "x": 44}, "right": {"opacity": 0, "x": 60},
               "fade": {"opacity": 0}, "slam": {"opacity": 0, "scale": 1.8, "rotation": -10}}[how]
        to = {"opacity": 1, "x": 0, "y": 0, "scale": 1, "duration": dur,
              "ease": "back.out(1.8)" if how in ("pop", "slam") else "power3.out"}
        if how == "slam":
            to["rotation"] = -4
        self.tw(i, t, frm, to)
        return i

    def to(self, i, t, props, dur=.35, ease="power2.out"):
        self.js.append(f'tl.to("#{i}",{json.dumps({**props, "duration": dur, "ease": ease})},{round(t, 2)});')

    def grow(self, i, t, dur=.8, axis="x"):
        a = {"scaleX": 0} if axis == "x" else {"scaleY": 0}
        b = {"scaleX": 1} if axis == "x" else {"scaleY": 1}
        origin = "0% 50%" if axis == "x" else "50% 100%"
        self.tw(i, t, {**a, "transformOrigin": origin}, {**b, "transformOrigin": origin, "duration": dur, "ease": "power2.out"})

    def count(self, x, y, to, t, size=200, color=INK, dur=1.1, nd=0, suffix="", w=None, align="left", ssize=None, fade=True):
        i = self.uid()
        st = f"left:{x}px;top:{y}px;font-size:{size}px;color:{color};font-weight:700;line-height:1;text-align:{align};white-space:nowrap;"
        if w:
            st += f"width:{w}px;"
        suf = f'<span style="font-size:{ssize or int(size * .55)}px">{suffix}</span>' if suffix else ""
        self.html.append(f'<div id="{i}" class="el" style="{st}"><span id="{i}-v">0</span>{suf}</div>')
        self.js.append(f'count("{i}-v",{to},{round(t, 2)},{dur},{nd});')
        if fade:  # không để số "0" đứng chờ trước khi giọng đọc tới
            self.tw(i, max(0, t - .05), {"opacity": 0}, {"opacity": 1, "duration": .2, "ease": "power1.out"})
        return i

    def svg(self, x, y, w, h, body, style=""):
        return self.box(x, y, w, h, f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="overflow:visible;display:block">{body}</svg>', "", style)

    def path(self, x, y, w, h, d, t, color=YEL, sw=8, dur=.6):
        i = self.uid()
        self.html.append(f'<div class="el" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px" data-layout-ignore>'
                         f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="overflow:visible;display:block">'
                         f'<path id="{i}" d="{d}" pathLength="1" fill="none" stroke="{color}" stroke-width="{sw}" '
                         f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 1" opacity="0"/></svg></div>')
        self.js.append(f'tl.set("#{i}",{{opacity:1}},{round(t, 2)});')
        self.tw(i, t, {"strokeDashoffset": 1}, {"strokeDashoffset": 0, "duration": dur, "ease": "power2.inOut"})
        return i

    def ring(self, x, y, r, pct, t, color=BLUE, sw=26, dur=1.0):
        i = self.uid()
        s = 2 * (r + sw)
        c = r + sw
        self.html.append(f'<div class="el" style="left:{x - c}px;top:{y - c}px;width:{s}px;height:{s}px" data-layout-ignore>'
                         f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}"><circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="{sw}"/>'
                         f'<circle id="{i}" cx="{c}" cy="{c}" r="{r}" pathLength="100" fill="none" stroke="{color}" stroke-width="{sw}" '
                         f'stroke-dasharray="{pct} 200" transform="rotate(-90 {c} {c})"/></svg></div>')
        self.tw(i, t, {"strokeDashoffset": pct}, {"strokeDashoffset": 0, "duration": dur, "ease": "power2.out"})
        return i

    # ---------- xuất file
    def write(self):
        top, bot = PANEL[self.panel]
        fonts = "".join(f"@font-face{{font-family:'DINRoundOT';font-weight:{w};src:url('assets/fonts/DINROUNDOT-{n}.otf')}}"
                        for w, n in ((400, "REGULAR"), (500, "MEDIUM"), (700, "BOLD")))
        fake = ('<div class="el fake">NỘI DUNG GIẢ LẬP</div>' if FAKE else "")
        squares = "".join(f'<i style="background:{c}"></i>' for c in (YEL, BLUE, GREEN))
        chosen = ROOT / "hf" / "assets" / "phong-cach.css"      # font người dùng chọn (tao_mau.py --ap-dung P5)
        chosen = chosen.read_text(encoding="utf-8") if chosen.exists() else ""
        out = f"""<template>
<style>
{fonts}
@font-face{{font-family:'StudioMono';src:local('Consolas')}}
#root{{position:absolute;inset:0;font-family:'DINRoundOT',sans-serif;color:{INK};overflow:hidden;background:#0E1116}}
#root *{{box-sizing:border-box;margin:0;padding:0}}
#root .panel{{position:absolute;left:64px;top:48px;width:1792px;height:984px;border-radius:40px;background:linear-gradient(160deg,{top},{bot});border:1px solid rgba(255,255,255,.10);overflow:hidden}}
#root .glow{{position:absolute;left:1000px;top:-360px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle,rgba(96,165,250,.16),rgba(96,165,250,0) 68%)}}
#root .scene{{position:absolute;inset:0}}
#root .el{{position:absolute}}
#root .card{{background:rgba(255,255,255,.065);border:2px solid rgba(255,255,255,.13);border-radius:26px}}
#root .mono{{font-family:'StudioMono',monospace;letter-spacing:.14em;font-size:28px;color:{MUTE};white-space:nowrap}}
#root .pill{{display:flex;align-items:center;justify-content:center;border-radius:999px;font-weight:700;white-space:nowrap}}
#root .fake{{right:192px;top:108px;font-size:28px;font-weight:700;letter-spacing:.08em;color:#0E1116;background:{YEL};border-radius:999px;padding:7px 20px}}
#root .foot{{left:192px;top:934px;display:flex;gap:10px;align-items:center}}
#root .foot i{{display:block;width:18px;height:18px;border-radius:5px}}
{chosen}
</style>
<div id="root" data-composition-id="{self.id}" data-width="1920" data-height="1080">
<div class="panel"><div id="{self.id}-glow" class="glow" data-layout-ignore></div></div>
<div class="el mono" style="left:192px;top:112px">{self.label}</div>
{fake}
<div class="el foot">{squares}<span class="mono" style="font-size:28px;margin-left:10px">{FOOTER}</span></div>
{chr(10).join(self.html)}
</div>
<script>
(function(){{
const tl = gsap.timeline({{ paused: true }});
const fmt = (v, nd) => {{ const p = v.toFixed(nd).split("."); let a = p[0].replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, "."); return nd && +p[1] ? a + "," + p[1] : a; }};
function typeIn(sel, t, d) {{
  const els = document.querySelectorAll(sel);
  if (els.length) tl.fromTo(els, {{ opacity: 0 }}, {{ opacity: 1, duration: .02, stagger: d / els.length, ease: "none" }}, t);
}}
function count(id, to, t, d, nd) {{
  const o = {{ v: 0 }};
  tl.fromTo(o, {{ v: 0 }}, {{ v: to, duration: d, ease: "power2.out", onUpdate: () => {{ const e = document.getElementById(id); if (e) e.textContent = fmt(o.v, nd); }} }}, t);
}}
tl.fromTo("#{self.id}-glow", {{ x: 0, y: 0 }}, {{ x: -220, y: 150, duration: {self.dur}, ease: "sine.inOut" }}, 0);
{chr(10).join(self.js)}
window.__timelines = window.__timelines || {{}};
window.__timelines["{self.id}"] = tl;
}})();
</script>
</template>
"""
        (ROOT / "hf" / "compositions" / f"{self.id}.html").write_text(out, encoding="utf-8", newline="\n")


