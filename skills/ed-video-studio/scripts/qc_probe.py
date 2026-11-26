#!/usr/bin/env python3
"""Technical QC for a finished video against a delivery preset.

Usage:
  python3 qc_probe.py final/video.mp4 --preset lms|zalo|teams|youtube|screen [--srt narration.srt] [--frames review/frames]

Checks: size limit, resolution/aspect, fps, codec (H.264/yuv420p), audio present, integrated
loudness (target ~ -16 LUFS, true peak <= -1 dBTP), black/silent gaps, SRT ends near video end.
--frames: writes one JPEG every 10 s + a contact sheet for the reviewer to look at.
Prints a PASS/WARN/FAIL table and writes qc.json next to the video.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

PRESETS = {
    "lms":     {"max_mb": 600, "w": 1920, "h": 1080},
    "teams":   {"max_mb": 250, "w": 1920, "h": 1080},
    "youtube": {"max_mb": 4000, "w": 1920, "h": 1080},
    "screen":  {"max_mb": 2000, "w": 1920, "h": 1080},
    "zalo":    {"max_mb": 100, "w": 1080, "h": 1920},
}


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--preset", default="lms", choices=PRESETS)
    ap.add_argument("--srt")
    ap.add_argument("--frames")
    a = ap.parse_args()
    v = Path(a.video); P = PRESETS[a.preset]
    res = []

    def add(name, status, detail):
        res.append({"check": name, "status": status, "detail": detail})

    info = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(v)]).stdout)
    vs = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    au = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"]); mb = v.stat().st_size / 1e6

    add("Dung lượng", "PASS" if mb <= P["max_mb"] else "FAIL", f"{mb:.1f} MB / giới hạn {P['max_mb']} MB")
    add("Kích thước", "PASS" if (vs["width"], vs["height"]) == (P["w"], P["h"]) else "WARN",
        f"{vs['width']}x{vs['height']} (preset {P['w']}x{P['h']})")
    num, den = map(int, vs["r_frame_rate"].split("/")); fps = num / den
    add("FPS", "PASS" if 24 <= fps <= 60 else "WARN", f"{fps:.2f}")
    ok_codec = vs["codec_name"] == "h264" and vs.get("pix_fmt") == "yuv420p"
    add("Codec", "PASS" if ok_codec else "WARN", f"{vs['codec_name']} / {vs.get('pix_fmt')} (nên h264/yuv420p để mọi máy phát được)")
    add("Có âm thanh", "PASS" if au else "FAIL", au["codec_name"] if au else "không có track audio")

    if au:
        r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(v), "-af", "ebur128=peak=true", "-f", "null", "-"])
        I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr); TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
        if I:
            i = float(I[-1]); add("Độ lớn (LUFS)", "PASS" if -18 <= i <= -13 else "WARN", f"{i:.1f} LUFS (mục tiêu -16)")
        if TP:
            tp = float(TP[-1]); add("True peak", "PASS" if tp <= -1.0 else "WARN", f"{tp:.1f} dBTP (≤ -1)")
        r = run(["ffmpeg", "-hide_banner", "-i", str(v), "-af", "silencedetect=n=-45dB:d=2.5", "-f", "null", "-"])
        sil = re.findall(r"silence_start: ([\d.]+)", r.stderr)
        add("Khoảng lặng > 2.5s", "PASS" if not sil else "WARN", ", ".join(f"{float(s):.1f}s" for s in sil) or "không có")

    r = run(["ffmpeg", "-hide_banner", "-i", str(v), "-vf", "blackdetect=d=1.0:pix_th=0.08", "-an", "-f", "null", "-"])
    blk = re.findall(r"black_start:([\d.]+)", r.stderr)
    blk = [b for b in blk if 0.5 < float(b) < dur - 1.5]
    add("Màn đen giữa video", "PASS" if not blk else "WARN", ", ".join(f"{float(b):.1f}s" for b in blk) or "không có")

    if a.srt:
        last = re.findall(r"--> (\d+):(\d+):(\d+),(\d+)", Path(a.srt).read_text(encoding="utf-8"))
        if last:
            h, m, s, ms = map(int, last[-1]); end = h * 3600 + m * 60 + s + ms / 1000
            add("SRT khớp độ dài", "PASS" if abs(dur - end) < 8 else "WARN", f"SRT kết thúc {end:.1f}s / video {dur:.1f}s")

    if a.frames:
        fd = Path(a.frames); fd.mkdir(parents=True, exist_ok=True)
        run(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-vf", "fps=1/10,scale=640:-2", "-q:v", "3", str(fd / "f_%03d.jpg")])
        n = len(list(fd.glob("f_*.jpg"))); cols = 5; rows = max(1, -(-n // cols))
        run(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-vf",
             f"fps=1/10,scale=384:-2,tile={cols}x{rows}:padding=6:color=white", "-frames:v", "1", str(fd / "contact_sheet.jpg")])
        add("Frame cho reviewer", "PASS", f"{n} frame + contact_sheet.jpg trong {fd}")

    w = max(len(x["check"]) for x in res)
    for x in res:
        print(f"{x['status']:<5} {x['check']:<{w}}  {x['detail']}")
    (v.with_name(v.stem + ".qc.json")).write_text(json.dumps({"video": str(v), "duration": dur, "preset": a.preset, "checks": res},
                                                       ensure_ascii=False, indent=1), encoding="utf-8")
    sys.exit(1 if any(x["status"] == "FAIL" for x in res) else 0)


if __name__ == "__main__":
    main()
