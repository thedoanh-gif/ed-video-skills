# -*- coding: utf-8 -*-
"""Dựng video Dark Studio từ data.json + mốc từng từ.
Sinh hf/index.html, hf/compositions/*.html, timing.json.
Chạy:  py -3 build.py
Cảnh: intro, CH01-CH03 ở file này; CH04-CH07 scenes_p12.py; CH08-CH10 scenes_p3.py; CH11-CH13 và outro scenes_p4.py.
"""
import json

from comp import ROOT, D, X, Y, TAIL, INTRO, YEL, BLUE, GREEN, PINK, INK, MUTE, Comp, vn, media_dur
from scenes_p12 import scene_ch04, scene_ch05, scene_ch06, scene_ch07
from scenes_p3 import scene_ch08, scene_ch09, scene_ch10
from scenes_p4 import scene_ch11, scene_ch12, scene_ch13, scene_outro
import comp

comp.FOOTER = f"BÁO CÁO ĐÀO TẠO {Y}"
OUTRO = 3.4


# ====================================================================== CẢNH
def scene_intro(c):
    c.open_scene(0.05, c.dur)
    c.enter(c.text(192, 268, "ĐÀO TẠO VÀ PHÁT TRIỂN", 34, color=BLUE), .25, "left")
    c.enter(c.text(192, 340, "Báo cáo đào tạo", 118), .4)
    c.enter(c.text(186, 478, str(Y), 290, color=YEL), .65, "pop", .6)
    c.enter(c.text(196, 812, f"Số liệu đến {D['moc_du_lieu']}", 44, color=MUTE, weight=500), 1.2, "fade")
    c.enter(c.box(1200, 250, 528, 580, cls="card"), .5, "right")
    hs = [g["ty_le"] for g in X["nhom"]]
    for k, v in enumerate(hs):
        h = int(60 + 250 * v / max(hs))
        c.grow(c.box(1250 + k * 90, 770 - h, 58, h, style=f"background:{[YEL, BLUE, GREEN, PINK, '#A78BFA'][k]};border-radius:14px"), .9 + k * .12, .8, "y")
    c.path(1250, 310, 430, 130, "M4 120 C90 110 110 60 190 76 S320 62 420 10", 1.5, INK, 7, 1.1)
    c.path(1250, 310, 430, 130, "M388 8 L424 7 L414 42", 2.55, INK, 7, .25)
    c.close_scene()
    c.cue(.15, "whoosh")


def scene_ch01(c):
    t2, t3 = c.A("Nghĩa", 3) - .15, c.A("Nhưng", 6) - .15
    gio = X["gio_tb"]
    # a. lịch 12 tháng + số giờ
    c.open_scene(0.05, t2)
    cal = c.uid()
    c.html.append(f'<div id="{cal}" class="scene">')
    c.enter(c.text(192, 220, f"Cả năm {Y}", 56, color=MUTE), .15, "left")
    for m in range(12):
        x, y = 192 + (m % 4) * 168, 320 + (m // 4) * 162
        tile = c.box(x, y, 148, 142, f'<div style="font-size:42px;font-weight:700;text-align:center;line-height:138px">T{m + 1}</div>', "card")
        c.enter(tile, .2 + m * .04, "pop", .35)
        c.to(tile, .6 + m * .11, {"backgroundColor": "rgba(245,158,11,.30)", "borderColor": YEL}, .25)
    c.html.append("</div>")
    tn = c.N("dành", 1)
    c.to(cal, tn, {"opacity": .38}, .4)
    num = c.count(970, 300, gio, tn, 330, YEL, 1.0, 1, w=758, align="center", fade=False)
    c.enter(num, tn - .05, "pop", .45)
    c.enter(c.text(970, 668, "giờ học / người", 70, w=758, align="center"), c.A("giờ", 2), "up")
    c.cue(tn, "pop")
    c.close_scene()
    # b. quy ra ngày làm việc
    c.open_scene(t2, t3)
    full, rem = int(gio // 8), round(gio - 8 * int(gio // 8), 1)
    cards = [8] * full + ([rem] if rem > 0 else [])
    tt = c.N("là", t2)
    c.enter(c.text(192, 190, f"{'Hơn ' if rem > 0 else ''}{full} ngày làm việc", 96, color=INK), tt, "up")
    n = len(cards)
    gap = 28
    cw = min(284, int((1536 - gap * (n - 1)) / n))
    x0 = 192 + (1536 - (cw * n + gap * (n - 1))) // 2
    for k, hours in enumerate(cards):
        x = x0 + k * (cw + gap)
        t = t2 + .15 + k * .09
        c.enter(c.box(x, 340, cw, 500, cls="card"), t, "up", .4)
        c.enter(c.text(x, 362, f"NGÀY {k + 1}", 34, w=cw, color=MUTE, align="center"), t + .1, "fade")
        for s in range(8):
            sy = 420 + (7 - s) * 44
            c.enter(c.box(x + 34, sy, cw - 68, 36, style="background:rgba(255,255,255,.08);border-radius:9px"), t + .12, "fade", .2)
            part = max(0, min(1, hours - s))
            if part > 0:
                c.grow(c.box(x + 34, sy, int((cw - 68) * part), 36, style=f"background:{YEL};border-radius:9px"),
                       t2 + .45 + (k * 8 + s) * (1.5 / (n * 8)), .18)
        c.enter(c.text(x, 780, f"{vn(hours)} giờ", 38, w=cw, align="center"), t2 + .55 + (k + 1) * (1.5 / n), "pop", .3)
    c.cue(t2 + .1, "swipe")
    c.close_scene()
    # c. trước / sau
    c.open_scene(t3, c.dur)
    tq = c.A("điều", 8)
    c.enter(c.text(192, 190, "Điều gì thay đổi?", 96, w=1536, align="center"), tq, "pop")
    jobs = ["Báo cáo tuần", "Trả lời khách hàng", "Giao ca, họp đội"]
    for side, (x, title, col) in enumerate([(192, "TRƯỚC KHI HỌC", MUTE), (1088, "SAU KHI HỌC", YEL)]):
        t = t3 + .15 + side * .35
        c.enter(c.box(x, 360, 640, 470, cls="card"), t, "left" if side == 0 else "right")
        c.enter(c.text(x + 48, 396, title, 40, color=col), t + .15, "fade")
        for k, job in enumerate(jobs):
            c.enter(c.box(x + 48, 486 + k * 104, 44, 44, style="border:4px solid rgba(255,255,255,.45);border-radius:10px"), t + .25 + k * .1, "pop", .3)
            c.enter(c.text(x + 118, 486 + k * 104, job, 40, weight=500), t + .28 + k * .1, "left", .35)
    c.enter(c.text(832, 480, f"+{vn(gio)} giờ", 44, w=256, color=BLUE, align="center"), t3 + .8, "pop")
    c.path(860, 560, 200, 80, "M8 40 L186 40 M150 12 L188 40 L150 68", t3 + .85, BLUE, 10, .5)
    to = c.A("thay", 9)
    c.path(1052, 326, 712, 540, "M360 12 C80 -4 6 130 12 280 C20 460 160 528 380 522 C600 516 704 420 698 260 C690 90 560 6 290 24", to, YEL, 9, .7)
    c.cue(to, "swipe")
    c.close_scene()


def scene_ch02(c):
    c.open_scene(0.05, c.dur)
    c.enter(c.text(192, 190, "Nội dung hôm nay", 84), .15, "left")
    starts = [c.A("Một", 1.5), c.A("Hai", 3.5), c.A("Ba", 7), c.A("Bốn", 10)]
    all_on = round(c.words[-1]["end"] + .1, 2)
    items = [("01", "Bức tranh<br>chung", BLUE), ("02", "Tư duy<br>và AI", YEL),
             ("03", "Ứng dụng<br>và phản hồi", GREEN), ("04", f"Cải thiện<br>và {Y + 1}", PINK)]
    for k, (num, title, col) in enumerate(items):
        x = 192 + k * 392
        grp = c.uid()
        c.html.append(f'<div id="{grp}" class="scene">')
        c.box(x, 330, 360, 560, cls="card", style=f"border-top:10px solid {col}")
        c.text(x + 36, 368, num, 130, color=col)
        c.text(x + 36, 524, title, 52, w=300)
        c.html.append("</div>")
        c.tw(grp, .4 + k * .12, {"opacity": 0, "y": 30}, {"opacity": .2, "y": 0, "duration": .5, "ease": "power3.out"})
        t = starts[k]
        c.to(grp, t - .05, {"opacity": 1, "y": -14}, .35, "back.out(2)")
        if k < 3:
            c.to(grp, starts[k + 1] - .05, {"opacity": .42, "y": 0}, .35)
        else:
            c.to(grp, all_on, {"y": 0}, .3)
        if k < 3:
            c.to(grp, all_on, {"opacity": 1}, .4)
        c.cue(t - .05, "pop")
        mini = c.uid()
        c.html.append(f'<div id="{mini}" class="scene">')
        if k == 0:
            for j, h in enumerate([70, 110, 90, 160]):
                c.grow(c.box(x + 48 + j * 70, 850 - h, 48, h, style=f"background:{col};border-radius:10px"), t + .25 + j * .12, .5, "y")
        elif k == 1:
            c.enter(c.box(x + 72, 668, 256, 62, "Tóm tắt giúp tôi", "pill", f"background:{BLUE};color:#0E1116;font-size:30px"), c.A("tư", t), "right")
            c.enter(c.box(x + 32, 758, 214, 62, "5 ý chính ✓", "pill", f"background:{col};color:#0E1116;font-size:32px"), c.A("AI", t), "left")
        elif k == 2:
            for j in range(5):
                st = c.svg(x + 44 + j * 56, 668, 48, 48, f'<path d="M24 3 L30 18 L46 19 L33 30 L38 45 L24 36 L10 45 L15 30 L2 19 L18 18 Z" fill="{YEL}"/>')
                c.enter(st, t + .35 + j * .13, "pop", .3)
            c.enter(c.box(x + 36, 750, 288, 68, "“Rất sát việc!”", "pill", f"background:{col};color:#0E1116;font-size:34px"), c.A("tiếng", t), "up")
        else:
            c.path(x + 36, 660, 288, 170, "M14 150 C90 150 70 80 140 90 S210 60 230 46", t + .3, col, 9, .9)
            c.path(x + 36, 660, 288, 170, "M230 46 L230 4 L284 18 L230 32", c.A("kế", t), col, 9, .5)
            c.enter(c.text(x + 204, 722, str(Y + 1), 44, color=INK), c.A("năm", t), "pop")
        c.html.append("</div>")
        c.tw(mini, 0, {"opacity": 1}, {"opacity": 1, "duration": .01})
    c.close_scene()


def scene_ch03(c):
    t1 = c.N("mô", 0) - .1
    t2 = c.A("Có", 5) - .1
    t3 = round(c.N("trước", t2) - .12, 2)   # đầu câu "…% nhân sự"
    t4 = c.A("Riêng", 12) - .1
    # a. thẻ chương
    c.open_scene(0.05, t1)
    c.enter(c.text(1080, 190, "01", 520, color="rgba(255,255,255,.08)"), .1, "right", .7)
    c.enter(c.text(192, 360, "PHẦN 1", 56, color=YEL), .15, "left")
    c.enter(c.text(192, 440, "Quy mô", 190), c.A("quy") - .1, "up")
    c.path(196, 668, 640, 30, "M4 20 Q160 4 320 18 T636 14", c.A("mô"), YEL, 12, .5)
    c.close_scene()
    c.cue(.1, "whoosh")
    # b. số lớp
    c.open_scene(t1, t2)
    tn = c.N("chức", t1)
    c.count(192, 200, D["so_lop_thuc_hien"], tn, 270, YEL, 1.0, 0)
    c.enter(c.text(200, 478, "lớp đào tạo", 60), c.A("lớp", tn), "up")
    for r in range(5):
        for k in range(9):
            q = c.box(1060 + k * 76, 220 + r * 62, 62, 48, style="background:rgba(96,165,250,.16);border-radius:10px")
            c.enter(q, t1 + .05 + (r + k) * .012, "fade", .2)
            c.to(q, t1 + .3 + (r * 9 + k) * .03, {"backgroundColor": BLUE}, .2)
    tp = c.N("lớp", tn)
    plan, act = D["so_lop_ke_hoach"], D["so_lop_thuc_hien"]
    big = max(plan, act)
    for k, (name, val, col) in enumerate([("Kế hoạch", plan, "#8794AD"), ("Thực hiện", act, YEL)]):
        y = 646 + k * 112
        c.enter(c.text(192, y + 12, name, 42, weight=500), tp - .1 + k * .2, "left")
        bw = int(920 * val / big)
        c.grow(c.box(450, y, bw, 72, style=f"background:{col};border-radius:16px"), tp + k * .25, .8)
        c.enter(c.text(470 + bw, y + 10, vn(val), 48), tp + .6 + k * .25, "fade")
    diff = round((act / plan - 1) * 100)
    label = f"+{diff}% kế hoạch" if diff > 0 else (f"Đạt {round(act / plan * 100)}% kế hoạch" if diff < 0 else "Đúng kế hoạch")
    td = c.N("hoạch", tp) if diff > 0 else tp + .5
    c.enter(c.box(1250, 548, 430, 76, label, "pill", f"background:{GREEN};color:#0E1116;font-size:42px"), td, "slam")
    c.cue(tn, "pop")
    c.cue(td, "stamp")
    c.close_scene()
    # c. lượt học
    c.open_scene(t2, t3)
    a, b = D["luot_hoc_nam_truoc"], D["luot_hoc"]
    c.enter(c.text(192, 190, "Lượt học", 96), t2 + .1, "left")
    for k, (yr, val, col, t) in enumerate([(Y - 1, a, "#8794AD", c.N("Có", t2) - .15), (Y, b, BLUE, c.A("lượt", t2) - .2)]):
        x = 360 + k * 400
        h = int(440 * val / max(a, b))
        c.grow(c.box(x, 800 - h, 260, h, style=f"background:{col};border-radius:20px 20px 6px 6px"), t, .8, "y")
        c.count(x - 20, 800 - h - 92, val, t, 70, INK, .8, 0, w=300, align="center")
        c.enter(c.text(x, 826, str(yr), 44, w=260, align="center", color=MUTE), t, "fade")
    tg = c.N("học", t2)
    d = round((b / a - 1) * 100)
    c.enter(c.box(1210, 420, 470, 220, f"{'+' if d > 0 else ''}{d}%", "pill", f"background:{GREEN if d >= 0 else PINK};color:#0E1116;font-size:150px"), tg, "slam")
    c.enter(c.text(1210, 668, "so với năm trước", 44, w=470, align="center", color=MUTE), tg + .6, "up")
    c.cue(tg, "stamp")
    c.close_scene()
    # d. 100 hình người
    c.open_scene(t3, t4)
    pct = round(X["ty_le_tham_gia"])
    for i in range(100):
        r, k = divmod(i, 10)
        p = c.svg(192 + k * 66, 205 + r * 66, 46, 58,
                  '<circle cx="23" cy="13" r="12" fill="currentColor"/><path d="M3 56 C3 22 43 22 43 56 Z" fill="currentColor"/>',
                  "color:rgba(255,255,255,.16)")
        c.enter(p, t3 + .02 + r * .02, "fade", .2)
        if i < pct:
            c.to(p, t3 + .25 + i * (1.35 / max(pct, 1)), {"color": YEL}, .18)
    c.count(940, 280, pct, t3 + .25, 300, YEL, 1.4, 0, "%", 788, "center")
    c.enter(c.text(940, 620, "nhân sự đã học<br>ít nhất 1 khóa", 64, w=788, align="center"), c.A("nhân", t3), "up")
    c.cue(t3 + .25, "pop")
    c.close_scene()
    # e. ba khối
    c.open_scene(t4, c.dur)
    c.enter(c.text(192, 190, "Theo từng khối", 84), t4 + .1, "left")
    low = X["khoi_thap_nhat"]["ma"]
    tlow = c.A("thấp", t4)
    for k, u in enumerate(X["khoi"]):
        x = 192 + k * 524
        grp = c.uid()
        c.html.append(f'<div id="{grp}" class="scene">')
        is_low = u["ma"] == low
        t = c.A("khối", t4) if is_low else t4 + .2 + k * .12
        card = c.box(x, 340, 488, 540, cls="card")
        c.ring(x + 244, 560, 140, u["ty_le"], t, YEL if is_low else BLUE, 34, .9)
        c.count(x + 94, 522, u["ty_le"], t, 88, INK, .9, 0, "%", 300, "center", 60, fade=False)
        c.text(x, 750, f"Khối {u['ten'].lower()}", 46, w=488, align="center")
        if is_low:
            tag = c.box(x + 104, 818, 280, 52, "THẤP NHẤT", "pill", f"background:{YEL};color:#0E1116;font-size:32px")
            c.enter(tag, tlow, "slam")
        c.html.append("</div>")
        c.enter(grp, t4 + .15 + k * .12, "up")
        if is_low:
            c.to(card, tlow, {"borderColor": YEL, "backgroundColor": "rgba(245,158,11,.14)"}, .3)
        else:
            c.to(grp, tlow, {"opacity": .4}, .4)
    c.cue(tlow, "stamp")
    c.close_scene()


# ====================================================================== LẮP RÁP
SCENES = [("ch01", scene_ch01, "mo", "MỞ ĐẦU"),
          ("ch02", scene_ch02, "mo", "NỘI DUNG HÔM NAY"),
          ("ch03", scene_ch03, "p1", "P1 · QUY MÔ"),
          ("ch04", scene_ch04, "p1", "P1 · NỘI DUNG VÀ NGÂN SÁCH"),
          ("ch05", scene_ch05, "p2", "P2 · TƯ DUY"),
          ("ch06", scene_ch06, "p2", "P2 · AI"),
          ("ch07", scene_ch07, "p2", "P2 · CHƯƠNG TRÌNH KHÁC"),
          ("ch08", scene_ch08, "p3", "P3 · TÍNH ỨNG DỤNG"),
          ("ch09", scene_ch09, "p3", "P3 · PHẢN HỒI HỌC VIÊN"),
          ("ch10", scene_ch10, "p3", "P3 · ĐIỂM HÀI LÒNG"),
          ("ch11", scene_ch11, "p4", "P4 · ĐIỂM CẦN CẢI THIỆN"),
          ("ch12", scene_ch12, "p4", f"P4 · KẾ HOẠCH {Y + 1}"),
          ("ch13", scene_ch13, "mo", "TỔNG KẾT")]


def main():
    (ROOT / "hf" / "compositions").mkdir(parents=True, exist_ok=True)
    comps = [Comp("intro", INTRO, "mo", f"BÁO CÁO NĂM {Y}")]
    scene_intro(comps[0])
    starts, t = [0.0], INTRO
    for cid, fn, panel, label in SCENES:
        c = Comp(cid, media_dur(ROOT / "audio" / f"{cid}.mp3") + TAIL, panel, label)
        fn(c)
        comps.append(c)
        starts.append(round(t, 3))
        t = round(t + c.dur, 3)
    out = Comp("outro", OUTRO, "mo", f"BÁO CÁO NĂM {Y}")
    scene_outro(out)
    comps.append(out)
    starts.append(round(t, 3))
    total = round(t + out.dur, 3)
    hosts, sfx = [], []
    for c, s in zip(comps, starts):
        c.write()
        hosts.append(f'      <div id="{c.id}" class="clip" data-composition-id="{c.id}" data-composition-src="compositions/{c.id}.html" '
                     f'data-start="{s}" data-duration="{c.dur}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>')
        sfx += [[round(s + a, 2), n] for a, n in c.sfx]
    index = f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #0E1116; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
      <audio id="mix" class="clip" data-start="0" data-duration="{int(total * 10) / 10}" data-track-index="3" src="assets/audio/mix.wav" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    (ROOT / "hf" / "index.html").write_text(index, encoding="utf-8", newline="\n")
    (ROOT / "timing.json").write_text(json.dumps({
        "total": total,
        "chapters": [{"id": c.id, "start": s, "off": 0, "voice": True} for c, s in zip(comps, starts) if c.words],
        "sfx": sorted(sfx)}, ensure_ascii=False), encoding="utf-8")
    print("Tổng", total, "giây:", [(c.id, s, c.dur) for c, s in zip(comps, starts)])


if __name__ == "__main__":
    main()
