#!/usr/bin/env python3
"""AI voice for Vietnamese narration, one file per chapter, with word timings.

Engines:
  edge   (default) Microsoft Edge neural voices via `<python> -m pip install edge-tts`. Natural, free, needs internet.
         Voices: vi-VN-HoaiMyNeural (nữ), vi-VN-NamMinhNeural (nam). Unofficial use of an online
         service: fine for internal drafts; for important videos prefer ElevenLabs or a real voice.
  piper  Offline, open-source (`pip install piper-tts`, then download a vi_VN voice). Less natural.
         No word timings -> run `npx -y hyperframes@0.9.84 transcribe` + to_srt.py --script afterwards.

Input: script-voice.txt with "### CH01 ..." blocks (ed-video-script format). [nghỉ] = 0.7 s pause.

Usage (<python> = python3 on macOS/Linux; on Windows `py -3` or the full python.exe path):
  <python> tts_vi.py script-voice.txt --out audio/ [--voice vi-VN-HoaiMyNeural] [--rate +12%] [--only ch02,ch04] [--pitch +0Hz]
  <python> tts_vi.py script-voice.txt --out audio/ --engine piper --piper-model vi_VN-vais1000-medium.onnx
  <python> tts_vi.py script-voice.txt --out audio/ --list-voices

Writes: audio/ch01.mp3 (or .wav), ..., audio/chXX.words.json (edge only), audio/voice-settings.json
Keep voice/rate/pitch identical across episodes (record them in the Series Kit voice profile).
"""
import argparse, asyncio, json, re, subprocess, sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # Windows consoles/pipes default to cp1252
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

RETRY_WAITS = [2, 4, 8, 15, 20]  # seconds between attempts; the free service often drops a request

PAUSE = "[nghỉ]"


def chapters(text):
    parts = re.split(r"^###\s*(CH\d+)[^\n]*\n", text, flags=re.M)
    if len(parts) < 3:
        return [("ch01", text.strip())]
    return [(parts[i].lower(), parts[i + 1].strip()) for i in range(1, len(parts), 2) if parts[i + 1].strip()]


def silence(path, sec):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(sec),
                    "-c:a", "libmp3lame", "-q:a", "4", str(path)], check=True)


def concat(files, out):
    lst = out.with_suffix(".txt")
    lst.write_text("".join(f"file '{Path(f).resolve()}'\n" for f in files), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c:a", "libmp3lame", "-q:a", "2", str(out)], check=True)
    lst.unlink()


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


async def edge_piece(text, voice, rate, pitch, out_mp3):
    import edge_tts
    com = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, boundary="WordBoundary")
    words = []
    with open(out_mp3, "wb") as f:
        async for ch in com.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"word": ch["text"], "start": ch["offset"] / 1e7,
                              "end": (ch["offset"] + ch["duration"]) / 1e7})
    return words


class ChapterFailed(Exception):
    pass


async def run_edge(chs, out, voice, rate, pitch):
    """Every chapter is tried even if another fails; failed ones get a second round. Returns the ids still failing."""
    for rnd in (1, 2):
        bad = []
        for item in chs:
            try:
                await edge_chapter(*item, out, voice, rate, pitch)
            except ChapterFailed as e:
                print(e, file=sys.stderr, flush=True)
                bad.append(item)
                for f in out.glob(f"_{item[0]}_*"):
                    f.unlink()
        if not bad:
            return []
        chs = bad
    return [c for c, _ in bad]


async def edge_chapter(cid, body, out, voice, rate, pitch):
    pieces = [p.strip() for p in body.split(PAUSE)]
    files, words, t = [], [], 0.0
    for k, p in enumerate(pieces):
        if p:
            f = out / f"_{cid}_{k:02d}.mp3"
            for attempt in range(len(RETRY_WAITS) + 1):
                try:
                    w = await edge_piece(re.sub(r"\s+", " ", p), voice, rate, pitch, f)
                    break
                except ImportError:
                    sys.exit(f'Thiếu edge-tts. Cài bằng: "{sys.executable}" -m pip install edge-tts')
                except (ValueError, TypeError) as e:  # wrong voice/rate/pitch: retrying cannot help
                    sys.exit(f"edge-tts: tham số sai ở {cid}: {e}")
                except Exception as e:  # service/network hiccup
                    if attempt == len(RETRY_WAITS):
                        raise ChapterFailed(f"edge-tts lỗi ở {cid} sau {attempt + 1} lần thử: {e}")
                    wait = RETRY_WAITS[attempt]
                    print(f"{cid}: lần {attempt + 1} lỗi ({e}); chờ {wait}s rồi thử lại", file=sys.stderr, flush=True)
                    await asyncio.sleep(wait)
            words += [{"word": x["word"], "start": round(x["start"] + t, 3), "end": round(x["end"] + t, 3)} for x in w]
            files.append(f); t += dur(f)
        if k < len(pieces) - 1:
            s = out / f"_{cid}_{k:02d}_pause.mp3"; silence(s, 0.7); files.append(s); t += 0.7
    concat(files, out / f"{cid}.mp3")
    for f in files:
        f.unlink()
    (out / f"{cid}.words.json").write_text(json.dumps(words, ensure_ascii=False, indent=0), encoding="utf-8")
    d = dur(out / f"{cid}.mp3")
    n = len(body.replace(PAUSE, " ").split())
    print(f"{cid}: {d:.1f}s, {n} từ, {n / d * 60:.0f} từ/phút (tính cả khoảng nghỉ)")


def run_piper(chs, out, model):
    for cid, body in chs:
        text = body.replace(PAUSE, ". ")  # piper has no SSML; a full stop gives a short pause
        dst = out / f"{cid}.wav"
        r = subprocess.run(["piper", "-m", model, "-f", str(dst)], input=text, text=True, capture_output=True)
        if r.returncode:
            sys.exit(f"piper lỗi: {r.stderr[-400:]}")
        print(f"{cid}: {dur(dst):.1f}s (piper không có mốc từng từ → chạy hyperframes transcribe + to_srt.py --script)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", nargs="?")
    ap.add_argument("--out", default="audio")
    ap.add_argument("--engine", choices=["edge", "piper"], default="edge")
    ap.add_argument("--voice", default="vi-VN-HoaiMyNeural")
    ap.add_argument("--rate", default="+12%")
    ap.add_argument("--pitch", default="+0Hz")
    ap.add_argument("--piper-model")
    ap.add_argument("--only", help="chỉ tạo các chương này, ví dụ ch02,ch04")
    ap.add_argument("--list-voices", action="store_true")
    a = ap.parse_args()
    if a.list_voices:
        subprocess.run([sys.executable, "-m", "edge_tts", "--list-voices"]); return
    if not a.script:
        ap.error("cần file script-voice.txt")
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    chs = chapters(Path(a.script).read_text(encoding="utf-8"))
    if a.only:
        want = {x.strip().lower() for x in a.only.split(",")}
        miss = want - {c for c, _ in chs}
        if miss:
            sys.exit(f"Không có chương: {', '.join(sorted(miss))}")
        chs = [c for c in chs if c[0] in want]
    failed = []
    if a.engine == "edge":
        failed = asyncio.run(run_edge(chs, out, a.voice, a.rate, a.pitch))
    else:
        if not a.piper_model:
            ap.error("--engine piper cần --piper-model <file .onnx>")
        run_piper(chs, out, a.piper_model)
    (out / "voice-settings.json").write_text(json.dumps({"engine": a.engine, "voice": a.voice if a.engine == "edge" else a.piper_model,
                                                        "rate": a.rate, "pitch": a.pitch}, ensure_ascii=False, indent=1), encoding="utf-8")
    if failed:
        sys.exit(f"Chưa tạo được: {', '.join(failed)}. Các chương khác đã xong. Chạy lại với --only {','.join(failed)}, kiểm tra mạng, hoặc dùng --engine piper.")


if __name__ == "__main__":
    main()
