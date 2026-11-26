# -*- coding: utf-8 -*-
"""Cập nhật các skill ed-video-* đã cài, lấy từ thư mục repo vừa tải về.

  py -3 cap-nhat.py --xem    chỉ xem có gì thay đổi, không ghi file nào
  py -3 cap-nhat.py          sao lưu file sắp bị ghi đè rồi cập nhật

Không xóa gì trên máy: font bạn tự chép, series kit và file bạn tự thêm được giữ nguyên.
File bạn đã sửa mà bản mới cũng có thì bị ghi đè, bản của bạn nằm trong thư mục sao lưu.
"""
import argparse, datetime, re, shutil, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SOURCE = Path(__file__).resolve().parent / "skills"
TEXT = {".md", ".py", ".json", ".txt", ".css", ".html", ".js", ".bat"}
HEADING = re.compile(r"^## (\S+) · (\S+) · (.+)$", re.M)


def releases(skills):
    """Các mục trong CHANGELOG.md, mới nhất trước: [(bản, ngày, tên, nội dung)]."""
    f = skills / "ed-video-studio" / "CHANGELOG.md"
    if not f.is_file():
        return []
    parts = HEADING.split(f.read_text(encoding="utf-8-sig").replace("\r\n", "\n"))
    return [tuple(x.strip() for x in parts[i:i + 4]) for i in range(1, len(parts), 4)]


def number(version):
    return tuple(int(x) for x in re.findall(r"\d+", version))


def same(a, b):
    x, y = a.read_bytes(), b.read_bytes()
    if a.suffix.lower() in TEXT:          # khác kiểu xuống dòng không tính là thay đổi
        x, y = x.replace(b"\r\n", b"\n"), y.replace(b"\r\n", b"\n")
    return x == y


def main():
    ap = argparse.ArgumentParser(description="Cập nhật skill ed-video-*")
    ap.add_argument("--xem", action="store_true", help="chỉ xem, không ghi file")
    ap.add_argument("--dich", type=Path, default=Path.home() / ".claude" / "skills", help="thư mục skill trên máy")
    args = ap.parse_args()
    if not SOURCE.is_dir():
        sys.exit(f"Không thấy {SOURCE}. Chạy script này trong thư mục repo đã giải nén.")
    if not (args.dich / "ed-video-studio").is_dir():
        sys.exit(f"Máy chưa cài ed-video-studio trong {args.dich}. Cài mới theo skills/ed-video-studio/CAI-DAT.md.")

    new, changed = [], []
    for f in sorted(SOURCE.rglob("*")):
        if not f.is_file() or "__pycache__" in f.parts:
            continue
        rel = f.relative_to(SOURCE)
        target = args.dich / rel
        if not target.exists():
            new.append(rel)
        elif not same(f, target):
            changed.append(rel)

    have, latest = releases(args.dich), releases(SOURCE)
    old = have[0][0] if have else None
    print(f"Bản trên máy : {old or 'chưa ghi số bản (trước 1.4)'}")
    print(f"Bản vừa tải  : {latest[0][0] if latest else '?'}")
    if old and latest and number(old) > number(latest[0][0]):
        sys.exit("Bản trên máy mới hơn bản vừa tải. Dừng lại, không ghi gì.")
    for version, date, title, body in latest:
        if not old or number(version) > number(old):
            print(f"\n[{version} · {date}] {title}\n{body}")
    if not new and not changed:
        print("\nMáy đang giống bản vừa tải, không cần cập nhật.")
        return
    for label, items in (("Thêm mới", new), ("Ghi đè (có sao lưu)", changed)):
        print(f"\n{label}: {len(items)} file")
        for rel in items:
            print("  " + rel.as_posix())
    if args.xem:
        print("\nChưa ghi gì. Chạy lại không có --xem để cập nhật.")
        return

    # sao lưu nằm ngoài thư mục skills để Claude Code không nạp thành skill trùng
    backup = args.dich.parent / "skills-backup" / f"ed-video-{datetime.datetime.now():%Y%m%d-%H%M%S}"
    for rel in changed:
        (backup / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(args.dich / rel, backup / rel)
    for rel in new + changed:
        (args.dich / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / rel, args.dich / rel)
    print(f"\nĐã cập nhật {len(new) + len(changed)} file.")
    if changed:
        print(f"Bản cũ của file bị ghi đè: {backup}")
    old_names = sorted(p.name for p in args.dich.glob("th-video-*"))
    if old_names:
        print("Còn skill tên cũ trên máy (không tự xóa): " + ", ".join(old_names))
    print("Mở phiên Claude Code mới để dùng bản mới.")


if __name__ == "__main__":
    main()
