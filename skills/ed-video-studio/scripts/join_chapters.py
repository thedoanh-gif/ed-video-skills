#!/usr/bin/env python3
"""Join rendered chapter MP4s (same size/fps/codec) into one video, optionally replace audio.

Usage:
  python3 join_chapters.py renders/ch01.mp4 renders/ch02.mp4 ... -o final/video.mp4 [--audio mix.wav]

Chapters are joined without re-encoding (concat demuxer, -c copy). If the files do not share
the same encoding, the script stops and says which one differs (re-render it with the same
settings instead of re-encoding everything).
"""
import argparse, glob, json, subprocess, sys, tempfile
from pathlib import Path


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=codec_name,width,height,r_frame_rate,pix_fmt", "-of", "json", str(p)],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"Không đọc được {p}: {r.stderr.strip()}")
    return json.loads(r.stdout)["streams"][0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapters", nargs="+")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--audio", help="file âm thanh đã mix cho cả video (thay audio gốc)")
    a = ap.parse_args()
    # PowerShell/cmd do not expand ch*.mp4
    a.chapters = [f for c in a.chapters for f in (sorted(glob.glob(c)) if '*' in c else [c])]
    if not a.chapters:
        ap.error('không tìm thấy file chương nào')

    ref = probe(a.chapters[0])
    for c in a.chapters[1:]:
        p = probe(c)
        if p != ref:
            sys.exit(f"{c} khác thông số với {a.chapters[0]}: {p} vs {ref}. Render lại chương này cùng cấu hình.")

    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    tmp_out = out.with_name(out.stem + ".partial.mp4")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        for c in a.chapters:
            f.write(f"file '{Path(c).resolve()}'\n")
        lst = f.name
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst]
    if a.audio:
        cmd += ["-i", a.audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    else:
        cmd += ["-c", "copy"]
    cmd += ["-movflags", "+faststart", str(tmp_out)]
    r = subprocess.run(cmd)
    if r.returncode:
        sys.exit("ffmpeg lỗi khi ghép.")
    tmp_out.replace(out)
    print(f"OK: {out} ({out.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
