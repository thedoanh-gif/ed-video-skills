# -*- coding: utf-8 -*-
"""Dựng lại video sau khi sửa du-lieu.txt (hoặc sau khi thêm nhạc audio/theme.mp3).

  py -3 dung_lai.py              làm đủ: số liệu -> giọng chương đổi -> dựng -> trộn -> kiểm tra -> render -> phụ đề
  py -3 dung_lai.py --thu        dừng sau bước kiểm tra (không render)
  py -3 dung_lai.py --ghi-moc    chỉ ghi lại "giọng hiện tại khớp lời hiện tại" (không tạo gì)

Cần mạng để tạo giọng (edge-tts). Bước kiểm tra và render mất khoảng 15 phút.
Kết quả: final/<tên thư mục dự án>.mp4 và .srt (ghi đè bản cũ cùng tên).
"""
import hashlib, json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
KIT = Path.home() / ".claude" / "skills" / "ed-video-studio" / "scripts"
HF = "hyperframes@0.9.84"
MARK = ROOT / "audio" / "voice-hash.json"
sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONUTF8"] = "1"


def run(args, **kw):
    print("\n>", " ".join(str(a) for a in args), flush=True)
    r = subprocess.run([str(a) for a in args], cwd=ROOT, **kw)
    if r.returncode and "stdout" not in kw:
        sys.exit(f"DỪNG: lệnh trên báo lỗi (mã {r.returncode}).")
    return r


def py(*args):
    run([sys.executable, *args])


def hashes():
    out, cur = {}, None
    for line in (ROOT / "script-voice.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("###"):
            cur = line.split()[1].lower()
            out[cur] = ""
        elif cur and line:
            out[cur] += line + "\n"
    return {k: hashlib.sha1(v.encode("utf-8")).hexdigest() for k, v in out.items()}


def main():
    if "--ghi-moc" in sys.argv:
        MARK.write_text(json.dumps(hashes(), indent=1), encoding="utf-8")
        print("Đã ghi mốc giọng đọc.")
        return
    py(ROOT / "gen_script.py")
    new = hashes()
    old = json.loads(MARK.read_text(encoding="utf-8")) if MARK.exists() else {}
    changed = [c for c, h in new.items() if old.get(c) != h or not (ROOT / "audio" / f"{c}.mp3").exists()]
    if changed:
        s = json.loads((ROOT / "audio" / "voice-settings.json").read_text(encoding="utf-8"))
        py(KIT / "tts_vi.py", "script-voice.txt", "--out", "audio/", "--voice", s["voice"],
           f"--rate={s['rate']}", "--only", ",".join(changed))
        MARK.write_text(json.dumps(new, indent=1), encoding="utf-8")
    else:
        print("Lời đọc không đổi, giữ nguyên giọng.")
    py(ROOT / "build.py")
    mix = [KIT / "mix_audio.py", "timing.json", "--voice-dir", "audio", "--sfx-dir", "audio/sfx",
           "-o", "hf/assets/audio/mix.wav"]
    if (ROOT / "audio" / "theme.mp3").exists():
        mix += ["--music", "audio/theme.mp3"]   # mặc định: nhạc giữ một mức suốt video
    else:
        print("Chưa có audio/theme.mp3: video không có nhạc nền.")
    py(*mix)
    npx = "npx.cmd" if os.name == "nt" else "npx"
    with open(ROOT / "check.json", "w", encoding="utf-8") as out:
        run([npx, "-y", HF, "check", "hf", "--json", "--at-transitions", "--safe-zone=standard"], stdout=out)
    result = json.loads((ROOT / "check.json").read_text(encoding="utf-8"))
    if not result.get("ok"):
        sys.exit("DỪNG: cổng kiểm tra báo lỗi bố cục. Xem check.json (thường do chữ mới dài hơn chỗ trống).")
    print("Cổng kiểm tra: đạt.")
    if "--thu" in sys.argv:
        return
    final = ROOT / "final" / f"{ROOT.name}.mp4"
    final.parent.mkdir(exist_ok=True)
    tmp = final.with_name("dang-render.mp4")
    run([npx, "-y", HF, "render", "hf", "-o", tmp])
    os.replace(tmp, final)
    py(ROOT / "make_srt.py", final.with_suffix(".srt"))
    py(KIT / "qc_probe.py", final, "--preset", "lms", "--srt", final.with_suffix(".srt"))
    print("\nXONG:", final)


if __name__ == "__main__":
    main()
