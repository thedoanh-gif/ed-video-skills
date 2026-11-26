# -*- coding: utf-8 -*-
"""Sinh phụ đề SRT cho cả video: chữ lấy từ script-display.txt, giờ lấy từ giọng đọc.
Chạy sau build.py:  py -3 make_srt.py [đường-dẫn.srt]
Mỗi dòng lời hiển thị khớp một dòng lời đọc; trong dòng, cắt theo dấu câu, tối đa 2 dòng x 42 ký tự."""
import re, sys
from pathlib import Path

from comp import ROOT, Comp, TAIL, media_dur
import json

MAX = 42
# cặp chữ không nên tách sang hai dòng hoặc hai phụ đề
GHEP = {w.strip() for w in """trọng điểm|nội bộ|tham gia|học viên|trực tuyến|trực tiếp|công cụ|giảng viên|chuyên môn|
nghiệp vụ|thực hành|công ty|sản xuất|tư duy|áp dụng|mục tiêu|phản hồi|chia sẻ|công việc|kế hoạch|chất lượng|an toàn|nhân sự|
nhân viên|vấn đề|nguyên nhân|giải pháp|yêu cầu|tài liệu|báo cáo|đào tạo|hằng tuần|hằng tháng|chương trình|người học|quản lý|
kỹ năng|đối tác|dữ liệu|kiểm tra|trách nhiệm|bình quân|thời gian|ngân sách|phòng ban|đầu tuần|vận hành|sát việc|giữa giờ|tỷ đồng|triệu đồng""".split("|")}


def penalty(a, b):
    """Điểm phạt khi ngắt giữa chữ cuối a và chữ đầu b."""
    x, y = a.split()[-1], b.split()[0]
    if x[-1] in ",.:;?!”":
        return 0
    p = 6
    if f"{x} {y}".lower().strip("“”.,:;?!") in GHEP:
        p += 30
    if x[-1].isdigit() or x[-1] == "%" and y == "điểm":
        p += 20
    return p


def display_lines():
    out, cur = {}, None
    for line in (ROOT / "script-display.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("###"):
            cur = line.split()[1].lower()
            out[cur] = []
        elif cur and line:
            out[cur].append(line)
    return out


def wrap(text):
    if len(text) <= MAX:
        return [text]
    toks = text.split()
    best = None
    for i in range(1, len(toks)):
        a, b = " ".join(toks[:i]), " ".join(toks[i:])
        score = max(len(a), len(b)) + penalty(a, b)
        if max(len(a), len(b)) <= MAX and (best is None or score < best[0]):
            best = (score, [a, b])
    return best[1] if best else None


def pieces(text):
    """Chia một dòng hiển thị thành các đoạn vừa 2 dòng phụ đề, ưu tiên cắt ở dấu câu."""
    parts = re.split(r"(?<=[,:;.?!”])\s+", text)
    out = []
    for part in parts:
        merged = wrap(out[-1] + " " + part) if out else None
        clean = merged and (len(merged) == 1 or penalty(*merged) == 0)
        if clean and not re.search(r"[.?!”]$", out[-1]):
            out[-1] += " " + part
        elif wrap(part):
            out.append(part)
        else:                       # đoạn không dấu câu quá dài: cắt đôi dần
            toks = part.split()
            chunk = ""
            for i, t in enumerate(toks):
                if chunk and not wrap(chunk + " " + t):
                    words = chunk.split()
                    carry = []
                    while len(words) > 1 and penalty(" ".join(words), " ".join(carry + toks[i:])) > 6:
                        carry.insert(0, words.pop())
                    out.append(" ".join(words))
                    chunk = " ".join(carry + [t])
                else:
                    chunk = (chunk + " " + t).strip()
            out.append(chunk)
    i = 0                           # gộp mẩu quá ngắn ("Một,", "Học xong,") với mẩu kế bên
    while i < len(out):
        if len(out[i]) < 15 and len(out) > 1:
            j = i if i + 1 < len(out) else i - 1
            if wrap(out[j] + " " + out[j + 1]):
                out[j:j + 2] = [out[j] + " " + out[j + 1]]
                i = j
                continue
        i += 1
    return out


def ts(t):
    ms = int(round(max(0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "final" / "phu-de.srt"
    timing = json.loads((ROOT / "timing.json").read_text(encoding="utf-8"))
    shown = display_lines()
    cues = []
    for ch in timing["chapters"]:
        cid, start = ch["id"], ch["start"]
        c = Comp(cid, media_dur(ROOT / "audio" / f"{cid}.mp3") + TAIL, "mo", "")
        lines = shown[cid]
        if len(lines) != len(c.lines):
            raise SystemExit(f"LỖI: {cid} lệch số dòng giữa lời hiển thị và lời đọc")
        firsts = [segs[0] for segs in c.lines] + [len(c.words)]
        for k, text in enumerate(lines):
            a, b = firsts[k], firsts[k + 1]
            t0, t1 = c.words[a]["start"], c.words[b - 1]["end"]
            ps = pieces(text)
            # giờ bắt đầu mỗi đoạn: ưu tiên mốc đoạn lời (dấu câu) gần vị trí tương đối nhất
            total = sum(len(p) for p in ps)
            starts, done = [], 0
            for i, p in enumerate(ps):
                guess = t0 + (t1 - t0) * done / total
                if i:
                    marks = [c.words[j]["start"] for j in c.lines[k]]
                    near = min(marks, key=lambda m: abs(m - guess))
                    if abs(near - guess) < .6 and near > starts[-1] + .5:
                        guess = near
                    else:           # bám vào đầu một từ
                        guess = min((w["start"] for w in c.words[a:b]), key=lambda m: abs(m - guess))
                starts.append(guess)
                done += len(p)
            for i, p in enumerate(ps):
                end = starts[i + 1] if i + 1 < len(ps) else t1 + .25
                cues.append([start + starts[i], start + end, "\n".join(wrap(p))])
    for i in range(len(cues) - 1):
        cues[i][1] = min(cues[i][1], cues[i + 1][0] - .01)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(cues, 1)), encoding="utf-8")
    short = [i + 1 for i, (a, b, _) in enumerate(cues) if b - a < 1.0]
    long_ = [i + 1 for i, (a, b, _) in enumerate(cues) if b - a > 6.0]
    print(f"{len(cues)} phụ đề -> {dest}")
    print("Ngắn dưới 1 giây:", short, "| Dài hơn 6 giây:", long_)


if __name__ == "__main__":
    main()
