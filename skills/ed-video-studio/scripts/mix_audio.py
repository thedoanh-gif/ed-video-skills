#!/usr/bin/env python3
"""Mix narration + looped music (one steady level) + SFX into one WAV for the whole video.

The music keeps the same level from start to end: it does NOT drop while the narrator speaks, there is only
a short fade in and a fade out. One fixed gain is computed so the track sits at --music-lufs (default -36 LUFS,
about 20 dB under the voice). --music-db sets that gain by hand instead (steady mode: closer to 0 = louder).
--duck restores the old behaviour (music ducked under the voice); use it only when the user asks for it.

Usage:
  <python> mix_audio.py timing.json --voice-dir audio --music audio/theme.wav --sfx-dir audio/sfx -o hf/assets/mix.wav
        [--music-lufs -36 | --music-db N] [--duck] [--sfx-db -14] [--voice-lufs -15.5]

timing.json:
  {"total": 153.2,
   "chapters": [{"id": "ch01", "start": 4.0, "off": 0, "voice": true}, ...],   # <voice-dir>/<id>.mp3|.wav|.m4a starts at start+off
   "sfx": [[4.6, "pop"], [7.1, "stamp"], ...]}                                  # <sfx-dir>/<name>.wav
SFX closer than 0.25 s to the previous one are dropped. Final peak is limited to about -2 dBFS; check LUFS with qc_probe.py.
"""
import argparse, json, re, subprocess, sys, tempfile
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

FMT = "aresample=48000,aformat=channel_layouts=stereo"


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def lufs(p):
    """Integrated loudness of a file (EBU R128)."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    found = re.findall(r"I:\s*(-?\d+(?:\.\d+)?) LUFS", r.stderr)
    if r.returncode or not found or float(found[-1]) <= -69:
        sys.exit(f"Không đo được độ lớn của nhạc {p} (file hỏng hoặc im lặng). Thử --music-db.")
    return float(found[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("timing")
    ap.add_argument("--voice-dir", default="audio")
    ap.add_argument("--music")
    ap.add_argument("--sfx-dir")
    ap.add_argument("--music-db", type=float, help="fixed music gain; default: from --music-lufs, or -6 with --duck")
    ap.add_argument("--music-lufs", type=float, default=-36, help="target music loudness in steady mode")
    ap.add_argument("--duck", action="store_true", help="lower the music while the narrator speaks")
    ap.add_argument("--sfx-db", type=float, default=-14)
    ap.add_argument("--voice-lufs", type=float, default=-15.5)
    ap.add_argument("-o", "--out", default="audio/mix.wav")
    a = ap.parse_args()
    T = json.loads(Path(a.timing).read_text(encoding="utf-8"))
    total = float(T["total"])
    inp, f, v, parts, n = [], [], [], ["[vo]"], 0

    for c in T["chapters"]:
        if not c.get("voice", True):
            continue
        src = next((Path(a.voice_dir) / f"{c['id']}{e}" for e in (".mp3", ".wav", ".m4a") if (Path(a.voice_dir) / f"{c['id']}{e}").exists()), None)
        if not src:
            sys.exit(f"Không thấy giọng của {c['id']} trong {a.voice_dir}")
        inp += ["-i", str(src)]
        f.append(f"[{n}:a]{FMT},adelay={int((c['start'] + c.get('off', 0)) * 1000)}:all=1[v{n}]")
        v.append(f"[v{n}]"); n += 1
    if not v:
        sys.exit("timing.json không có chương nào có giọng")
    tail = "asplit=2[vo][key]" if a.music and a.duck else "anull[vo]"
    f.append("".join(v) + f"amix=inputs={len(v)}:normalize=0,apad=whole_dur={total},loudnorm=I={a.voice_lufs}:TP=-2:LRA=11,aresample=48000,{tail}")

    if a.music:
        # finite loop count: an endless -stream_loop never lets the graph finish
        inp += ["-stream_loop", str(int(total // max(dur(a.music), 1)) + 1), "-i", a.music]
        if a.music_db is not None:
            gain = a.music_db
        else:
            gain = -6 if a.duck else round(a.music_lufs - lufs(a.music), 2)
        chain = (f"[{n}:a]{FMT},atrim=0:{total},volume={gain}dB,afade=t=in:d={0.4 if a.duck else 1.5},"
                 f"afade=t=out:st={max(total - 2.5, 0)}:d=2.5[mu]")
        if a.duck:
            chain += ";[mu][key]sidechaincompress=threshold=0.02:ratio=8:attack=80:release=700[du]"
        f.append(chain)
        parts.append("[du]" if a.duck else "[mu]"); n += 1
        print(f"Nhạc: {'tự hạ khi có lời' if a.duck else 'giữ một mức'}, gain {gain} dB")

    if a.sfx_dir and T.get("sfx"):
        keep, last = [], -9
        for t, k in sorted(T["sfx"]):
            if t - last >= .25:
                keep.append((t, k)); last = t
        out = []
        for k in sorted({k for _, k in keep}):
            p = Path(a.sfx_dir) / f"{k}.wav"
            if not p.exists():
                sys.exit(f"Thiếu SFX {p}")
            ts = [t for t, x in keep if x == k]
            inp += ["-i", str(p)]
            f.append(f"[{n}:a]{FMT},volume={a.sfx_db}dB,asplit={len(ts)}" + "".join(f"[{k}{i}]" for i in range(len(ts))))
            for i, t in enumerate(ts):
                f.append(f"[{k}{i}]adelay={int(t * 1000)}:all=1[{k}d{i}]"); out.append(f"[{k}d{i}]")
            n += 1
        f.append("".join(out) + f"amix=inputs={len(out)}:normalize=0,apad=whole_dur={total}[fx]")
        parts.append("[fx]")

    f.append("".join(parts) + (f"amix=inputs={len(parts)}:normalize=0," if len(parts) > 1 else "") + f"alimiter=limit=0.84:level=disabled,atrim=0:{total}[o]")
    graph = ";\n".join(f)
    with tempfile.TemporaryDirectory() as d:
        g = Path(d) / "graph.txt"; g.write_text(graph, encoding="utf-8")
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        base = ["ffmpeg", "-y", "-v", "error", *inp]
        end = ["-map", "[o]", "-t", str(total), "-ar", "48000", a.out]
        r = subprocess.run(base + ["-filter_complex_script", str(g)] + end, capture_output=True, text=True)
        if r.returncode and "filter_complex_script" in r.stderr:  # option removed in newer ffmpeg
            r = subprocess.run(base + ["-/filter_complex", str(g)] + end, capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"ffmpeg lỗi: {r.stderr[-600:]}")
    print(f"OK {a.out}: {dur(a.out):.1f}s")


if __name__ == "__main__":
    main()
