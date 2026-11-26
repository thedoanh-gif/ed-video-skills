#!/usr/bin/env python3
"""Measure a reference video so the agent can write the Style Bible from facts, not guesses.

Usage:
  python3 analyze_reference.py sample.mp4 [--captions sample.vi.vtt] [--out analysis/sample] [--scene 0.30]

Writes into --out:
  beats.json        every visible change (build steps) - the real pacing of motion videos
  shots.json        cut points + shot lengths (ffmpeg scene detection)
  frames/           one JPEG per shot (middle frame) + one every 5 s
  contact_*.jpg     contact sheets (look at these with your image viewer / Read tool)
  palette.json      dominant colours over the whole video (hex + share)
  pacing.json       words per minute and pauses, per 30 s window (needs --captions)
  report.md         a numeric summary to paste into the Style Bible

Needs ffmpeg/ffprobe; Pillow + numpy for the palette (pip install pillow numpy).
"""
import argparse, json, re, subprocess, sys
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def duration(v):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)]).stdout.strip())


def vinfo(v):
    s = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate", "-of", "json", str(v)]).stdout)["streams"][0]
    n, d = map(int, s["r_frame_rate"].split("/"))
    return s["width"], s["height"], n / d


def detect_cuts(v, thr):
    r = run(["ffmpeg", "-hide_banner", "-i", str(v), "-vf", f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"])
    return [float(x) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]


def change_events(v, thr=0.035, merge=0.6):
    """Every visible state change (element enters, build step, cut). Motion videos rarely 'cut',
    so this is the real pacing number."""
    r = run(["ffmpeg", "-hide_banner", "-i", str(v), "-vf", f"scale=320:-2,select='gt(scene,{thr})',showinfo",
             "-an", "-f", "null", "-"])
    ev = []
    for x in (float(t) for t in re.findall(r"pts_time:([\d.]+)", r.stderr)):
        if not ev or x - ev[-1] > merge:
            ev.append(x)
    return ev


def ts_to_s(t):
    p = [float(x) for x in t.replace(",", ".").split(":")]
    while len(p) < 3:
        p.insert(0, 0)
    return p[0] * 3600 + p[1] * 60 + p[2]


def caption_words(path):
    txt = Path(path).read_text(encoding="utf-8-sig").replace("\r", "")
    words, prev = [], []
    for b in re.split(r"\n\s*\n", txt):
        m = re.search(r"([\d:.,]+)\s*-->\s*([\d:.,]+)", b)
        if not m:
            continue
        st, en = ts_to_s(m.group(1)), ts_to_s(m.group(2))
        body = re.sub(r"<[^>]+>", "", " ".join(b[m.end():].split("\n"))).strip()
        body = re.sub(r"\s+", " ", body)
        cur = body.split()
        k = next((n for n in range(min(len(prev), len(cur)), 0, -1) if prev[-n:] == cur[:n]), 0)
        toks = cur[k:]
        prev = cur or prev
        if toks and en > st:
            d = (en - st) / len(toks)
            words += [(st + i * d, tk) for i, tk in enumerate(toks)]
    return words


def palette(frames, k=8):
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return {"error": "pip install pillow numpy để lấy bảng màu"}
    px = []
    for f in frames[:120]:
        im = Image.open(f).convert("RGB").resize((96, 54))
        px.append(np.asarray(im).reshape(-1, 3))
    X = np.concatenate(px).astype(float)
    q = (X // 24).astype(int)  # coarse buckets, then average inside bucket
    keys, inv, cnt = np.unique(q, axis=0, return_inverse=True, return_counts=True)
    inv = inv.ravel()
    order = np.argsort(-cnt)[:k]
    out = []
    for o in order:
        c = X[inv == o].mean(axis=0).astype(int)
        out.append({"hex": "#%02X%02X%02X" % tuple(c), "share": round(float(cnt[o]) / len(X), 3)})
    return out


def sheet(src_glob_dir, pattern, out, cols=6, w=320):
    files = sorted(src_glob_dir.glob(pattern))
    if not files:
        return
    rows = -(-len(files) // cols)
    run(["ffmpeg", "-y", "-v", "error", "-pattern_type", "glob", "-i", str(src_glob_dir / pattern), "-vf",
         f"scale={w}:-2,tile={cols}x{rows}:padding=6:color=white", "-frames:v", "1", str(out)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--captions")
    ap.add_argument("--out")
    ap.add_argument("--scene", type=float, default=0.30)
    a = ap.parse_args()
    v = Path(a.video)
    out = Path(a.out or f"analysis/{v.stem}"); fr = out / "frames"; fr.mkdir(parents=True, exist_ok=True)
    dur = duration(v); W, H, fps = vinfo(v)

    cuts = [c for c in detect_cuts(v, a.scene) if 0.2 < c < dur - 0.2]
    bounds = [0.0] + cuts + [dur]
    shots = [{"start": round(bounds[i], 2), "end": round(bounds[i + 1], 2), "len": round(bounds[i + 1] - bounds[i], 2)}
             for i in range(len(bounds) - 1)]
    lens = sorted(s["len"] for s in shots)
    median = lens[len(lens) // 2]
    (out / "shots.json").write_text(json.dumps(shots, indent=1), encoding="utf-8")

    for i, s in enumerate(shots):  # middle frame of each shot
        t = (s["start"] + s["end"]) / 2
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(v), "-frames:v", "1", "-vf", "scale=960:-2",
             "-q:v", "3", str(fr / f"shot_{i:03d}_{t:07.2f}s.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-vf", "fps=1/5,scale=960:-2", "-q:v", "3", str(fr / "t_%04d.jpg")])
    sheet(fr, "shot_*.jpg", out / "contact_shots.jpg")
    # one sheet per minute of the 5 s grid keeps them readable
    tfiles = sorted(fr.glob("t_*.jpg"))
    for m in range(0, len(tfiles), 12):
        grp = out / f"_m{m // 12:02d}"; grp.mkdir(exist_ok=True)
        for f in tfiles[m:m + 12]:
            (grp / f.name).write_bytes(f.read_bytes())
        sheet(grp, "t_*.jpg", out / f"contact_min{m // 12:02d}.jpg", cols=4)
        for f in grp.iterdir():
            f.unlink()
        grp.rmdir()

    ev = change_events(v)
    gaps = sorted(b - a for a, b in zip(ev, ev[1:])) or [dur]
    beats = {"events": len(ev), "per_min": round(len(ev) / (dur / 60), 1), "median_gap": round(gaps[len(gaps) // 2], 1),
             "p90_gap": round(gaps[int(len(gaps) * .9)], 1), "max_gap": round(gaps[-1], 1), "times": [round(x, 2) for x in ev]}
    (out / "beats.json").write_text(json.dumps(beats, indent=1), encoding="utf-8")

    pal = palette(sorted(fr.glob("t_*.jpg")))
    (out / "palette.json").write_text(json.dumps(pal, indent=1), encoding="utf-8")

    pacing = None
    if a.captions:
        words = caption_words(a.captions)
        win = []
        for t0 in range(0, int(dur) + 1, 30):
            n = sum(1 for t, _ in words if t0 <= t < t0 + 30)
            win.append({"from": t0, "wpm": n * 2})
        span = (words[-1][0] - words[0][0]) if len(words) > 1 else dur
        total_wpm = round(len(words) / (span / 60), 1) if span else 0
        gaps = [round(words[i + 1][0] - words[i][0], 2) for i in range(len(words) - 1) if words[i + 1][0] - words[i][0] > 1.2]
        pacing = {"words": len(words), "covered_s": round(span, 1), "wpm_avg": total_wpm, "per_30s": win, "pauses_over_1.2s": len(gaps)}
        (out / "pacing.json").write_text(json.dumps(pacing, ensure_ascii=False, indent=1), encoding="utf-8")
        (out / "transcript.txt").write_text(" ".join(w for _, w in words), encoding="utf-8")

    rep = [f"# Đo đạc: {v.name}", "",
           f"- Thời lượng: {dur:.1f}s ({dur/60:.1f} phút) · {W}x{H} · {fps:.0f} fps",
           f"- Số shot: {len(shots)} · độ dài shot trung vị {median:.1f}s · ngắn nhất {lens[0]:.1f}s · dài nhất {lens[-1]:.1f}s",
           f"- Cắt cảnh hẳn: {len(shots)/(dur/60):.1f} lần/phút (video motion ít cắt — xem nhịp thay đổi hình bên dưới)",
           f"- **Nhịp thay đổi hình** (phần tử mới/bước dựng/cắt): {beats['per_min']} lần/phút · khoảng cách trung vị {beats['median_gap']}s · 90% dưới {beats['p90_gap']}s · lâu nhất {beats['max_gap']}s",
           f"- Màu chiếm ưu thế: " + (", ".join(f"{p['hex']} ({p['share']:.0%})" for p in pal[:6]) if isinstance(pal, list) else str(pal))]
    if pacing:
        rep.append(f"- Lời (trên {pacing['covered_s']}s có transcript): {pacing['words']} từ · {pacing['wpm_avg']} từ/phút · {pacing['pauses_over_1.2s']} chỗ ngắt > 1.2s")
    rep += ["", "## Shot dài nhất (thường là cảnh 'thở' hoặc cảnh chính)"]
    for s in sorted(shots, key=lambda s: -s["len"])[:5]:
        rep.append(f"- {s['start']:.1f}–{s['end']:.1f}s ({s['len']:.1f}s)")
    rep += ["", "Ảnh để xem: contact_shots.jpg (1 ảnh/shot), contact_minXX.jpg (1 ảnh/5s)."]
    (out / "report.md").write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
