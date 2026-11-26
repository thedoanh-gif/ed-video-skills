#!/usr/bin/env python3
"""Voice -> SRT.  Turn word timings into a clean Vietnamese SRT.

Input (any of):
  - JSON from `npx -y hyperframes@0.9.84 transcribe` or Whisper (segments[].words[], words[], or a flat list
    of {word|text, start, end})
  - .vtt / .srt (YouTube or Teams captions)

Optional --script FILE: the approved script text. Words are then taken from the script and only
the timing comes from the transcript (fixes Whisper's Vietnamese spelling / names).

Optional --glossary FILE: lines "sai => đúng" applied when no script is given.

Output: SRT with max 42 chars/line, max 2 lines, 1-6 s per cue, breaks at punctuation.
Also writes <out>.words.json (word list with times) for the motion timeline,
and <out>.unsure.txt listing low-confidence cues to check by hand.

Usage:
  python3 to_srt.py transcript.json -o narration.srt [--script script.txt] [--glossary terms.txt]
"""
import argparse, difflib, json, re, sys, unicodedata
from pathlib import Path

MAX_LINE, MAX_LINES, MIN_DUR, MAX_DUR = 42, 2, 1.0, 6.0


def nfc(s):
    return unicodedata.normalize("NFC", s)


def ts_to_s(t):
    t = t.strip().replace(",", ".")
    parts = t.split(":")
    parts = [float(p) for p in parts]
    while len(parts) < 3:
        parts.insert(0, 0.0)
    h, m, s = parts
    return h * 3600 + m * 60 + s


def s_to_srt(t):
    t = max(0.0, t)
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# ---------- readers ----------
def words_from_json(data):
    words = []

    def add(w):
        text = w.get("word", w.get("text", "")).strip()
        if not text:
            return
        st = w.get("start", w.get("start_time", w.get("from")))
        en = w.get("end", w.get("end_time", w.get("to")))
        if st is None or en is None:
            return
        words.append({"w": nfc(text), "s": float(st), "e": float(en),
                      "p": float(w.get("probability", w.get("confidence", 1.0)) or 1.0)})

    if isinstance(data, dict):
        if "segments" in data:
            for seg in data["segments"]:
                if seg.get("words"):
                    for w in seg["words"]:
                        add(w)
                else:  # segment-level only: spread words evenly
                    toks = seg.get("text", "").split()
                    if toks:
                        d = (seg["end"] - seg["start"]) / len(toks)
                        for i, tk in enumerate(toks):
                            add({"word": tk, "start": seg["start"] + i * d, "end": seg["start"] + (i + 1) * d})
        elif "words" in data:
            for w in data["words"]:
                add(w)
        else:
            raise SystemExit("JSON không có 'segments' hay 'words' – mở file xem cấu trúc rồi chỉnh reader.")
    elif isinstance(data, list):
        for w in data:
            add(w)
    return words


def words_from_captions(text):
    """VTT/SRT -> words spread evenly inside each cue. Dedupes YouTube rolling captions."""
    cues = []
    blocks = re.split(r"\n\s*\n", text.replace("\r", ""))
    for b in blocks:
        m = re.search(r"([\d:.,]+)\s*-->\s*([\d:.,]+)", b)
        if not m:
            continue
        st, en = ts_to_s(m.group(1)), ts_to_s(m.group(2))
        lines = b[m.end():].strip().split("\n")
        body = " ".join(l for l in lines if l.strip())
        body = re.sub(r"<[^>]+>", "", body)  # YouTube word tags
        body = re.sub(r"\s+", " ", body).strip()
        if body:
            cues.append((st, en, nfc(body)))
    # YouTube auto-captions repeat the tail of the previous cue; drop the longest overlap
    words, prev = [], []
    for st, en, body in cues:
        toks = body.split()
        k = 0
        for n in range(min(len(prev), len(toks)), 0, -1):
            if prev[-n:] == toks[:n]:
                k = n
                break
        new = toks[k:]
        prev = toks
        if not new or en <= st:
            continue
        d = (en - st) / len(new)
        for i, tk in enumerate(new):
            words.append({"w": tk, "s": st + i * d, "e": st + (i + 1) * d, "p": 1.0})
    return words


# ---------- fixing text ----------
def norm_token(t):
    return re.sub(r"[^\w]", "", t.lower())


def align_to_script(words, script_text):
    """Keep timing from `words`, take spelling/punctuation from the script."""
    sw = nfc(script_text).split()
    a = [norm_token(w["w"]) for w in words]
    b = [norm_token(t) for t in sw]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                w = dict(words[i1 + k]); w["w"] = sw[j1 + k]; w["p"] = 1.0; out.append(w)
        elif j2 > j1:  # replace / insert: spread script words over the transcript span
            conf = 0.8 if i2 > i1 else 0.5  # replace = timing known; insert = timing guessed
            if i2 > i1:
                st, en = words[i1]["s"], words[i2 - 1]["e"]
            else:
                st = out[-1]["e"] if out else (words[i1]["s"] if i1 < len(words) else 0)
                en = words[i1]["s"] if i1 < len(words) else st + 0.3 * (j2 - j1)
                en = max(en, st + 0.2 * (j2 - j1))
            d = (en - st) / (j2 - j1)
            for k in range(j2 - j1):
                out.append({"w": sw[j1 + k], "s": st + k * d, "e": st + (k + 1) * d, "p": conf})
        # delete: transcript words not in script (fillers "ờ", "à") are dropped
    ratio = sm.ratio()
    return out, ratio


def apply_glossary(words, path):
    rules = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if "=>" in line:
            bad, good = [nfc(x.strip()) for x in line.split("=>", 1)]
            if bad:
                rules.append((bad, good))
    text = " ".join(w["w"] for w in words)
    for bad, good in rules:
        text = re.sub(rf"(?<!\w){re.escape(bad)}(?!\w)", good, text, flags=re.IGNORECASE)
    toks = text.split()
    if len(toks) == len(words):
        for w, t in zip(words, toks):
            w["w"] = t
        return words
    # token count changed: rebuild by spreading over full span
    st, en = words[0]["s"], words[-1]["e"]
    d = (en - st) / len(toks)
    return [{"w": t, "s": st + i * d, "e": st + (i + 1) * d, "p": 0.9} for i, t in enumerate(toks)]


# ---------- cueing ----------
def wrap(text):
    if len(text) <= MAX_LINE:
        return [text]
    toks, best = text.split(), None
    for i in range(1, len(toks)):
        l1, l2 = " ".join(toks[:i]), " ".join(toks[i:])
        score = max(len(l1), len(l2)) + (0 if l1.endswith((",", ".", "?", "!", ":")) else 3)
        if best is None or score < best[0]:
            best = (score, [l1, l2])
    return best[1]


def build_cues(words):
    cues, cur = [], []

    def flush():
        if cur:
            cues.append(list(cur)); cur.clear()

    for i, w in enumerate(words):
        cur.append(w)
        text = " ".join(x["w"] for x in cur)
        dur = cur[-1]["e"] - cur[0]["s"]
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap = (nxt["s"] - w["e"]) if nxt else 99
        end_sentence = w["w"].endswith((".", "?", "!", "…"))
        soft = w["w"].endswith((",", ";", ":"))
        nxt_len = len(text) + 1 + (len(nxt["w"]) if nxt else 0)
        if (end_sentence and dur >= MIN_DUR) or gap > 0.6 or dur >= MAX_DUR \
           or nxt_len > MAX_LINE * MAX_LINES or (soft and len(text) > MAX_LINE):
            flush()
    flush()
    out = []
    for c in cues:
        st, en = c[0]["s"], c[-1]["e"]
        if en - st < MIN_DUR:
            en = st + MIN_DUR
        out.append({"s": st, "e": en, "text": " ".join(x["w"] for x in c),
                    "p": min(x["p"] for x in c)})
    for a, b in zip(out, out[1:]):  # no overlaps
        if a["e"] > b["s"] - 0.04:
            a["e"] = max(a["s"] + 0.3, b["s"] - 0.04)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--script")
    ap.add_argument("--glossary")
    ap.add_argument("--offset", type=float, default=0.0, help="dịch toàn bộ thời gian (giây)")
    a = ap.parse_args()

    src = Path(a.input)
    raw = src.read_text(encoding="utf-8-sig")
    if src.suffix.lower() == ".json":
        words = words_from_json(json.loads(raw))
    else:
        words = words_from_captions(raw)
    if not words:
        sys.exit("Không đọc được từ nào từ file đầu vào.")

    note = ""
    if a.script:
        script = Path(a.script).read_text(encoding="utf-8")
        script = re.sub(r"\[[^\]]*\]|<[^>]+>", " ", script)  # drop [pause]/<break> tags
        words, ratio = align_to_script(words, script)
        note = f"khớp kịch bản: {ratio:.0%}"
        if ratio < 0.6:
            print(f"CẢNH BÁO: transcript chỉ khớp {ratio:.0%} với kịch bản – giọng đọc có thể đã lệch kịch bản.", file=sys.stderr)
    elif a.glossary:
        words = apply_glossary(words, a.glossary)

    for w in words:
        w["s"] += a.offset; w["e"] += a.offset

    cues = build_cues(words)
    out = Path(a.out)
    with out.open("w", encoding="utf-8") as f:
        for i, c in enumerate(cues, 1):
            f.write(f"{i}\n{s_to_srt(c['s'])} --> {s_to_srt(c['e'])}\n" + "\n".join(wrap(c["text"])) + "\n\n")
    out.with_suffix(".words.json").write_text(
        json.dumps([{"word": w["w"], "start": round(w["s"], 3), "end": round(w["e"], 3)} for w in words],
                   ensure_ascii=False, indent=0), encoding="utf-8")
    unsure = [f"#{i} {s_to_srt(c['s'])}  {c['text']}" for i, c in enumerate(cues, 1) if c["p"] < 0.6]
    out.with_suffix(".unsure.txt").write_text("\n".join(unsure) or "(không có)", encoding="utf-8")
    print(f"OK: {len(cues)} cue, {len(words)} từ, dài {cues[-1]['e']:.1f}s. {note} Cần kiểm tra tay: {len(unsure)} cue.")


if __name__ == "__main__":
    main()
