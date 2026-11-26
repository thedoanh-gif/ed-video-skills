#!/usr/bin/env python3
"""ED_Video Kit doctor: kiểm tra môi trường trước khi làm video.

Chỉ dùng thư viện chuẩn của Python. Không cài gì, không cần quyền admin.
Mọi gợi ý sửa đều là cách làm KHÔNG cần quyền admin (cài cho riêng người dùng).

Cách dùng:
  <python> doctor.py              # kiểm tra nhanh
  <python> doctor.py --full       # thêm: tải/kiểm HyperFrames bản ghim và Chrome để render (lần đầu có thể mất vài phút)
  <python> doctor.py --json       # kết quả dạng JSON cho agent đọc
Mã thoát: 0 = không có LỖI, 1 = có ít nhất một LỖI.
"""
import argparse, json, os, platform, re, shutil, socket, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCK = HERE.parent / "assets" / "kit.lock.json"
IS_WIN = os.name == "nt"

OK, WARN, FAIL, INFO = "OK", "CẢNH BÁO", "LỖI", "THÔNG TIN"
results = []


def add(name, status, detail, fix=""):
    results.append({"muc": name, "trang_thai": status, "chi_tiet": detail, "cach_sua": fix})


def run(cmd, timeout=30):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           shell=IS_WIN and isinstance(cmd, str), encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError:
        return 127, "not found"
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    except Exception as e:  # noqa: BLE001
        return 1, str(e)


def ver_tuple(s):
    return tuple(int(x) for x in re.findall(r"\d+", s)[:3]) or (0,)


def which(name):
    return shutil.which(name + ".cmd") if IS_WIN and shutil.which(name + ".cmd") else shutil.which(name)


def user_path_hint(folder):
    if IS_WIN:
        return ("Thêm vào PATH của NGƯỜI DÙNG (không cần admin), chạy trong PowerShell: "
                f"[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path','User') + ';{folder}', 'User') "
                "rồi đóng và mở lại terminal.")
    return f"Thêm `export PATH=\"{folder}:$PATH\"` vào ~/.zshrc hoặc ~/.bashrc rồi mở terminal mới."


def main():
    ap = argparse.ArgumentParser(description="ED_Video Kit doctor")
    ap.add_argument("--full", action="store_true", help="kiểm cả HyperFrames bản ghim và Chrome render (chậm lần đầu)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    lock = {}
    try:
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        add("kit.lock.json", WARN, f"không đọc được {LOCK}: {e}", "Cài lại skill ed-video-studio từ gói kit.")
    hf_ver = lock.get("hyperframes", "0.9.84")
    hf = f"npx -y hyperframes@{hf_ver}"

    # 1. Hệ điều hành + quyền
    add("Hệ điều hành", INFO, f"{platform.system()} {platform.release()} ({platform.machine()})")
    if IS_WIN:
        try:
            import ctypes
            admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:  # noqa: BLE001
            admin = False
        add("Quyền admin", INFO, "đang chạy với quyền admin" if admin else "không có quyền admin (bình thường với máy công ty; kit không cần admin)")

    # 2. Python
    pv = sys.version.split()[0]
    need = lock.get("python_min", "3.10")
    st = OK if ver_tuple(pv) >= ver_tuple(need) else FAIL
    add("Python", st, f"{pv} tại {sys.executable}",
        "" if st == OK else "Cài Python 3.12 bản 'Install for me only' từ python.org: bỏ chọn 'Use admin privileges when installing py.exe', chọn 'Add python.exe to PATH'.")
    pydir = str(Path(sys.executable).parent)
    on_path = any(Path(p).resolve() == Path(pydir).resolve() for p in os.environ.get("PATH", "").split(os.pathsep) if p and Path(p).exists())
    if not on_path and not (IS_WIN and shutil.which("py")):
        add("Python trong PATH", WARN, f"{pydir} chưa nằm trong PATH; agent phải gọi bằng đường dẫn đầy đủ", user_path_hint(pydir))
    if IS_WIN and os.environ.get("PYTHONUTF8") != "1":
        add("PYTHONUTF8", WARN, "chưa đặt, script có thể lỗi chữ tiếng Việt",
            "Chạy một lần (không cần admin): setx PYTHONUTF8 1   rồi mở terminal mới.")

    # 3. Thư viện Python
    try:
        from importlib.metadata import version, PackageNotFoundError
    except ImportError:  # pragma: no cover
        version = None
    pkgs = list(lock.get("pip_packages", ["pillow", "numpy"])) + ["edge-tts"]
    missing = []
    for pk in pkgs:
        try:
            v = version(pk) if version else "?"
        except Exception:  # noqa: BLE001
            v = None
        if v is None:
            missing.append(pk)
            continue
        if pk == "edge-tts" and lock.get("edge_tts") and v != lock["edge_tts"]:
            add("edge-tts", WARN, f"đang có {v}, kit đã thử với {lock['edge_tts']}",
                f"{Path(sys.executable).name} -m pip install --user edge-tts=={lock['edge_tts']}")
        else:
            add(pk, OK, v)
    if missing:
        pins = [f"edge-tts=={lock['edge_tts']}" if m == "edge-tts" and lock.get("edge_tts") else m for m in missing]
        add("Thư viện Python", FAIL, "thiếu: " + ", ".join(missing),
            f"\"{sys.executable}\" -m pip install --user " + " ".join(pins))

    # 4. Node + npx
    node = which("node")
    if not node:
        add("Node.js", FAIL, "không tìm thấy",
            "Không cần admin: tải bản .zip Node 22 LTS (Windows x64) từ nodejs.org, giải nén vào %LOCALAPPDATA%\\Programs\\nodejs, "
            "rồi thêm thư mục đó vào PATH người dùng. " + (user_path_hint("%LOCALAPPDATA%\\Programs\\nodejs") if IS_WIN else ""))
    else:
        rc, out = run([node, "--version"])
        nv = out.strip()
        st = OK if ver_tuple(nv) >= ver_tuple(lock.get("node_min", "22")) else FAIL
        add("Node.js", st, f"{nv} tại {node}", "" if st == OK else "Cần Node 22 trở lên. Tải bản .zip mới, giải nén đè, không cần admin.")
        if not which("npx"):
            add("npx", FAIL, "không tìm thấy npx cạnh node", "Cài lại Node bằng bản .zip đầy đủ (có npx).")

    # 5. FFmpeg
    ff = os.environ.get("HYPERFRAMES_FFMPEG_PATH") or which("ffmpeg")
    if not ff:
        add("FFmpeg", FAIL, "không tìm thấy",
            "Không cần admin: tải 'ffmpeg-release-essentials.zip' (gyan.dev) giải nén vào %LOCALAPPDATA%\\Programs\\ffmpeg, "
            "thêm thư mục bin vào PATH người dùng." if IS_WIN else "macOS: brew install ffmpeg (Homebrew cài trong thư mục người dùng).")
    else:
        rc, out = run([ff, "-version"])
        first = out.splitlines()[0] if out else "?"
        add("FFmpeg", OK if rc == 0 else FAIL, first[:80])
        if not (which("ffprobe") or (ff and Path(ff).with_name("ffprobe.exe" if IS_WIN else "ffprobe").exists())):
            add("FFprobe", WARN, "không thấy ffprobe cạnh ffmpeg", "Dùng bản FFmpeg 'essentials' đầy đủ (có ffprobe).")

    # 6. Telemetry
    if os.environ.get("HYPERFRAMES_NO_TELEMETRY") != "1":
        add("Telemetry HyperFrames", WARN, "chưa tắt (máy công ty nên tắt)",
            "Chạy một lần, không cần admin: " + ("setx HYPERFRAMES_NO_TELEMETRY 1  và  setx DO_NOT_TRACK 1  rồi mở terminal mới."
                                                 if IS_WIN else "thêm `export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1` vào ~/.zshrc"))
    else:
        add("Telemetry HyperFrames", OK, "đã tắt")

    # 7. Mạng
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        add("Mạng", INFO, "máy đi qua proxy (HTTPS_PROXY), bỏ qua kiểm kết nối trực tiếp; thử giọng AI bằng tts_vi.py để biết chắc")
    for host, why in ([] if proxy else [("registry.npmjs.org", "tải HyperFrames"), ("speech.platform.bing.com", "giọng AI edge-tts"),
                      ("cdn.jsdelivr.net", "không bắt buộc: kit dùng GSAP tại chỗ")]):
        try:
            socket.create_connection((host, 443), timeout=6).close()
            add(f"Mạng: {host}", OK, why)
        except Exception as e:  # noqa: BLE001
            st = INFO if "không bắt buộc" in why else WARN
            add(f"Mạng: {host}", st, f"không kết nối được ({e.__class__.__name__}); ảnh hưởng: {why}",
                "" if st == INFO else "Nếu máy dùng proxy công ty: đặt biến người dùng HTTPS_PROXY, hoặc nhờ IT mở địa chỉ này. Giọng AI lỗi thì dùng ghi âm thật.")

    # 8. Dung lượng
    try:
        free = shutil.disk_usage(Path.cwd()).free / 1e9
        add("Dung lượng trống", OK if free >= 3 else WARN, f"{free:.1f} GB", "" if free >= 3 else "Cần khoảng 3–5 GB (Chrome render, cache).")
    except Exception:  # noqa: BLE001
        pass

    # 9. HyperFrames bản ghim (chậm lần đầu)
    if a.full and which("npx"):
        rc, out = run(f"{hf} --version" if IS_WIN else hf.split() + ["--version"], timeout=300)
        got = (re.findall(r"\d+\.\d+\.\d+", out) or ["?"])[-1]
        add(f"HyperFrames {hf_ver}", OK if rc == 0 and got == hf_ver else FAIL, f"chạy được: {got}" if rc == 0 else out.strip()[-200:],
            "" if rc == 0 else "Kiểm mạng tới registry.npmjs.org; không dùng npm -g với quyền admin.")
        rc, out = run(f"{hf} browser ensure" if IS_WIN else hf.split() + ["browser", "ensure"], timeout=600)
        add("Chrome để render", OK if rc == 0 else FAIL, out.strip().splitlines()[-1][:120] if out.strip() else "",
            "" if rc == 0 else "HyperFrames tự tải Chrome vào thư mục người dùng; nếu bị chặn thì nhờ IT mở storage.googleapis.com.")
    elif not a.full:
        add(f"HyperFrames {hf_ver}", INFO, f"bỏ qua (chạy --full để kiểm). Luôn gọi: {hf} <lệnh>")

    fails = [r for r in results if r["trang_thai"] == FAIL]
    if a.json:
        print(json.dumps({"ok": not fails, "hyperframes_cmd": hf, "ket_qua": results}, ensure_ascii=False, indent=1))
    else:
        w = max(len(r["muc"]) for r in results)
        for r in results:
            print(f"[{r['trang_thai']:^9}] {r['muc']:<{w}}  {r['chi_tiet']}")
            if r["cach_sua"]:
                print(f"{'':12}{'':<{w}}  → {r['cach_sua']}")
        print()
        print("KẾT LUẬN:", "SẴN SÀNG" if not fails else f"CÒN {len(fails)} LỖI, xem dòng '→' để sửa (đều không cần quyền admin)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
