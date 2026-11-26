#!/usr/bin/env python3
"""Evidence pack for an independent video review.

Usage:
  python3 review_frames.py video.mp4 --out review/ [--ref styleframes_dir_or_reference.mp4] [--every 5]

Creates in --out:
  frames/t_XXXX.jpg      one frame every N s (960 px wide)
  contact_XX.jpg         contact sheets, 12 frames each (one per minute at 5 s)
  phone/phone_XXXX.jpg   frames shrunk to phone width (360 px) - the "can I read it on a phone" test
  compare/cmp_XX.jpg     side-by-side MẪU | CỦA BẠN (when --ref is given: images are paired in order,
                         a reference video is sampled at the same relative positions)
  beats.json             visual change events + stats (pacing check: target 8-10 changes/min, max still <= 10 s)
"""
import argparse, json, re, subprocess
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def dur(v):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)]).stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", default="review")
    ap.add_argument("--ref")
    ap.add_argument("--every", type=float, default=5)
    a = ap.parse_args()
    v, out = Path(a.video), Path(a.out)
    fr, ph, cp = out / "frames", out / "phone", out / "compare"
    for d in (fr, ph, cp):
        d.mkdir(parents=True, exist_ok=True)
    D = dur(v)

    run(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-vf", f"fps=1/{a.every},scale=960:-2", "-q:v", "3", str(fr / "t_%04d.jpg")])
    frames = sorted(fr.glob("t_*.jpg"))
    for i in range(0, len(frames), 12):
        tmp = out / "_c"; tmp.mkdir(exist_ok=True)
        for f in frames[i:i + 12]:
            (tmp / f.name).write_bytes(f.read_bytes())
        run(["ffmpeg", "-y", "-v", "error", "-pattern_type", "glob", "-i", str(tmp / "t_*.jpg"), "-vf",
             "scale=400:-2,tile=4x3:padding=6:color=white", "-frames:v", "1", str(out / f"contact_{i // 12:02d}.jpg")])
        for f in tmp.iterdir():
            f.unlink()
        tmp.rmdir()

    for f in frames[::3]:  # every 15 s at default
        run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-vf", "scale=360:-2", str(ph / f.name.replace("t_", "phone_"))])

    if a.ref:
        ref = Path(a.ref)
        if ref.is_dir():
            refs = sorted([p for p in ref.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg")])
            n = len(refs)
            picks = [frames[min(len(frames) - 1, int(i * len(frames) / max(n, 1)))] for i in range(n)]
        else:
            n = 6; RD = dur(ref); refs = []
            for i in range(n):
                t = RD * (i + 0.5) / n; p = cp / f"_ref_{i}.jpg"
                run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(ref), "-frames:v", "1", "-vf", "scale=960:-2", str(p)])
                refs.append(p)
            picks = [frames[min(len(frames) - 1, int(len(frames) * (i + 0.5) / n))] for i in range(n)]
        for i, (r, m) in enumerate(zip(refs, picks)):
            dst = cp / f"cmp_{i:02d}.jpg"
            res = run(["ffmpeg", "-y", "-v", "error", "-i", str(r), "-i", str(m), "-filter_complex",
                 "[0]scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2:white,"
                 "drawtext=text='MẪU':x=12:y=12:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.7[a];"
                 "[1]scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2:white,"
                 "drawtext=text='CỦA BẠN':x=12:y=12:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.7[b];[a][b]hstack",
                 str(dst)])
            if res.returncode or not dst.exists():  # drawtext has no font (common on Windows): no labels, left = MẪU
                run(["ffmpeg", "-y", "-v", "error", "-i", str(r), "-i", str(m), "-filter_complex",
                     "[0]scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2:white[a];"
                     "[1]scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2:white[b];[a][b]hstack",
                     str(dst)])
        for p in cp.glob("_ref_*.jpg"):
            p.unlink()

    r = run(["ffmpeg", "-hide_banner", "-i", str(v), "-vf", "scale=320:-2,select='gt(scene,0.035)',showinfo", "-an", "-f", "null", "-"])
    ev = []
    for x in (float(t) for t in re.findall(r"pts_time:([\d.]+)", r.stderr)):
        if not ev or x - ev[-1] > 0.6:
            ev.append(x)
    pts = [0.0] + ev + [D]
    gaps = [(round(pts[i], 1), round(pts[i + 1] - pts[i], 1)) for i in range(len(pts) - 1)]
    long_stills = [g for g in gaps if g[1] > 10]
    beats = {"duration": round(D, 1), "changes": len(ev), "per_min": round(len(ev) / (D / 60), 1),
             "long_stills_over_10s": [{"at": s, "len": l} for s, l in long_stills]}
    (out / "beats.json").write_text(json.dumps(beats, indent=1), encoding="utf-8")
    print(f"{len(frames)} khung · {len(list(ph.glob('*.jpg')))} khung cỡ điện thoại · "
          f"{len(list(cp.glob('cmp_*.jpg')))} khung so sánh · nhịp {beats['per_min']} lần/phút (chuẩn 8–10) · "
          f"khung đứng yên >10s: {len(long_stills)} " + (str([f"{s}s ({l}s)" for s, l in long_stills[:6]]) if long_stills else ""))


if __name__ == "__main__":
    main()
