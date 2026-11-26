# -*- coding: utf-8 -*-
"""Dựng ảnh mẫu cho từng phong cách bằng chính 7 khung cảnh của th-default + theme.css của phong cách.

  py -3 tao_mau.py                 dựng tất cả; ảnh vào preview/ (trong skill) hoặc ../anh/ (trong dự án)
  py -3 tao_mau.py P1 P3           chỉ dựng vài phong cách
  py -3 tao_mau.py --out <thu-muc> đổi thư mục ảnh
  py -3 tao_mau.py --font F2 P1    dựng phong cách P1 bằng font F2 (xem fonts.json)
  py -3 tao_mau.py --chon-font     dựng ảnh chon-font.jpg so sánh các font
  py -3 tao_mau.py --ap-dung P1 --font F2 --hf <du-an>/hf
                                   áp phong cách + font vào một dự án video

Nhờ dựng bằng khung thật, ảnh mẫu đúng là hình video sẽ ra. P5 dùng khung thật của kit dark-studio.
Mọi nội dung trong ảnh là nội dung minh họa.
"""
import html, json, shutil, subprocess, sys, tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent if (HERE.parent / "series-kits").exists() else Path.home() / ".claude" / "skills" / "ed-video-studio" / "assets"
KIT = ASSETS / "series-kits" / "th-default"
DARK = ASSETS / "series-kits" / "dark-studio" / "styleframes"
HF = "hyperframes@" + str(json.loads((ASSETS / "kit.lock.json").read_text(encoding="utf-8")).get("hyperframes", "0.9.84"))
BLOCKS = ["title-card", "big-number", "process-steps", "compare", "three-points", "key-message", "cta-outro"]
SHORT = {"title-card": "title", "big-number": "number", "process-steps": "steps", "compare": "compare",
         "three-points": "points", "key-message": "message", "cta-outro": "outro"}
MAIN = BLOCKS[:4]          # 4 khung hiện trên trang hướng dẫn
SEC = 5                    # mỗi khung 5 giây (không vượt thời lượng gốc của khung ngắn nhất), chụp ở giây 4,6

CATALOG = json.loads((HERE / "styles.json").read_text(encoding="utf-8"))
FONTS = {f["code"]: f for f in json.loads((HERE / "fonts.json").read_text(encoding="utf-8"))}


def font_dir(f):
    if f["source"] == "kit":
        return KIT / "fonts"
    if f["source"] == "windows":
        return Path("C:/Windows/Fonts")
    return HERE / "fonts" / f["folder"]


def style_css(style, code, hf):
    """Chép font vào <hf>/assets/fonts, trả về CSS gồm giao diện phong cách + font đã chọn."""
    dest = hf / "assets" / "fonts"
    dest.mkdir(parents=True, exist_ok=True)
    f = FONTS[code]
    faces = ""
    for name, weight, slant in f["faces"]:
        src = font_dir(f) / name
        if not src.exists():
            raise SystemExit(f"Thiếu font {src}. Chọn font khác, không tự thay font ở bản cuối.")
        shutil.copy(src, dest / name)
        faces += (f"@font-face{{font-family:'TH-Display';font-weight:{weight};font-style:{slant};size-adjust:{f['adjust']}%;"
                  f"src:url('assets/fonts/{name}')}}\n")
    sdir = HERE / style["folder"]
    for extra in (sdir / "fonts").glob("*.ttf"):
        shutil.copy(extra, dest / extra.name)
    if style.get("frames"):      # Dark Studio: không có theme.css, chỉ đổi font
        return (f"/* Dark Studio · font {code} {f['name']} */\n{faces}"
                "#root{font-family:'TH-Display',sans-serif}\n#root *{font-variant-numeric:lining-nums}\n")
    theme = (sdir / "theme.css").read_text(encoding="utf-8")
    return (f"/* Phong cách {style['code']} · {style['name']} · font {code} {f['name']} */\n{faces}{theme}\n"
            ":root{--font-display:'TH-Display',sans-serif}\n#root *{font-variant-numeric:lining-nums}\n"
            ".sb{position:absolute;left:0;top:0;width:1920px;height:1080px}\n")


def variables(c):
    """Ghép nội dung minh họa của một phong cách vào biến của từng khung."""
    return {
        "title-card": dict(eyebrow=c["eyebrow"], title=c["title"], subtitle=c["subtitle"], number="01", times="0.1|0.3|0.6"),
        "big-number": dict(value=c["number"][0], suffix=c["number"][1], label=c["number"][2], note="Số liệu minh họa", times="0.2|1.0|1.4", count="1.0"),
        "process-steps": dict(heading=c["steps_head"], steps="|".join(c["steps"]), times="0.1|0.6|1.2|1.8|2.4|3.0"),
        "compare": dict(heading=c["compare_head"], left_title="Nên tránh", left_items="|".join(c["avoid"]),
                        right_title="Nên làm", right_items="|".join(c["do"]), times="0.1|0.6|1.8"),
        "three-points": dict(heading=c["points_head"], items="|".join(c["points"]), times="0.1|0.6|1.4|2.2"),
        "key-message": dict(message=c["message"], highlight=c["highlight"], by="Thông điệp minh họa", times="0.2|1.0|1.4"),
        "cta-outro": dict(title=c["outro"], action=c["action"], contact="Nội dung minh họa", times="0.1|0.3|0.8|1.2"),
    }


def project(style, work, code="F1"):
    (work / "compositions").mkdir(parents=True)
    (work / "assets" / "vendor").mkdir(parents=True)
    shutil.copy(ASSETS / "vendor" / "gsap.min.js", work / "assets" / "vendor")
    css = style_css(style, code, work)
    clips = ""
    vals = variables(style["content"])
    for i, name in enumerate(BLOCKS):
        shutil.copy(KIT / "blocks" / f"{name}.html", work / "compositions")
        v = html.escape(json.dumps(vals[name], ensure_ascii=False), quote=False).replace("'", "&#39;")
        clips += (f'<div id="s{i}" class="clip sb sb-{SHORT[name]}" data-composition-id="s{i}" data-composition-src="compositions/{name}.html" '
                  f"data-start=\"{i * SEC}\" data-duration=\"{SEC}\" data-track-index=\"0\" data-width=\"1920\" data-height=\"1080\" data-variable-values='{v}'></div>\n")
    total = SEC * len(BLOCKS)
    (work / "index.html").write_text(f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<script src="assets/vendor/gsap.min.js"></script>
<style>
html,body{{margin:0;width:1920px;height:1080px;overflow:hidden}}
#root{{position:relative;width:1920px;height:1080px;overflow:hidden}}
{css}</style></head><body>
<div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-start="0" data-duration="{total}">
{clips}</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>""", encoding="utf-8")


def render(style, out, code="F1", dest=None):
    dest = dest or out / style["folder"]
    dest.mkdir(parents=True, exist_ok=True)
    for old in dest.glob("*.png"):             # chỉ xóa ảnh cũ; OneDrive hay khóa việc xóa cả thư mục
        old.unlink()
    if style.get("frames"):                                   # dùng khung có sẵn của kit
        for i, name in enumerate(style["frames"], 1):
            shutil.copy(DARK / name, dest / f"{i:02d}-{name[3:]}")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "hf"
            project(style, work, code)
            shots = Path(tmp) / "shots"
            at = ",".join(f"{i * SEC + 4.6:.1f}" for i in range(len(BLOCKS)))
            r = subprocess.run(f'npx -y {HF} snapshot "{work}" --at {at} --no-end -o "{shots}"', shell=True,
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            pngs = sorted(shots.rglob("*.png"), key=lambda p: p.name)
            pngs = [p for p in pngs if "contact" not in p.name.lower() and "sheet" not in p.name.lower()]
            if len(pngs) != len(BLOCKS):
                print(r.stdout[-3000:], r.stderr[-3000:])
                raise SystemExit(f"{style['code']}: cần {len(BLOCKS)} ảnh, nhận {len(pngs)}: {[p.name for p in pngs]}")
            for i, (p, name) in enumerate(zip(pngs, BLOCKS), 1):
                shutil.copy(p, dest / f"{i:02d}-{SHORT[name]}.png")
    print("xong", style["code"], dest.name, len(list(dest.glob("*.png"))), "ảnh")


def font(size, weight="BOLD"):
    return ImageFont.truetype(str(KIT / "fonts" / f"DINROUNDOT-{weight}.otf"), size)


def wrap(d, text, width):
    lines = [""]
    for word in text.split():
        t = (lines[-1] + " " + word).strip()
        if d.textlength(t, font=font(30, "REGULAR")) > width:
            lines.append(word)
        else:
            lines[-1] = t
    return "\n".join(lines)


def sheet(style, out):
    """Bảng xem đủ khung của một phong cách (để kiểm tra)."""
    pngs = sorted((out / style["folder"]).glob("*.png"))
    w, h, p, top = 640, 360, 16, 76
    rows = (len(pngs) + 1) // 2
    img = Image.new("RGB", (w * 2 + p * 3, top + rows * (h + p)), "#5A5F69")
    ImageDraw.Draw(img).text((p, 16), f"{style['code']} · {style['name']}", font=font(44), fill="white")
    for i, f in enumerate(pngs):
        img.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS), (p + (i % 2) * (w + p), top + (i // 2) * (h + p)))
    img.save(out / f"bang-{style['folder']}.jpg", quality=90)


def picker(out):
    """Một ảnh duy nhất để người dùng chọn phong cách: mỗi hàng một phong cách, 2 khung."""
    w, h, p, lab, top = 640, 360, 20, 470, 130
    img = Image.new("RGB", (lab + 2 * (w + p) + p, top + len(CATALOG) * (h + p)), "#F4F5F7")
    d = ImageDraw.Draw(img)
    d.text((p * 2, 36), "Chọn phong cách cho video", font=font(58), fill="#1F2937")
    for r, s in enumerate(CATALOG):
        y = top + r * (h + p)
        pngs = sorted((out / s["folder"]).glob("*.png"))
        if len(pngs) < 2:
            continue
        d.rounded_rectangle((p, y, lab, y + h), 24, fill="white")
        d.text((p + 32, y + 28), s["code"], font=font(88), fill="#1F2937")
        d.text((p + 32, y + 134), s["name"], font=font(46), fill="#1F2937")
        d.text((p + 32, y + 198), wrap(d, s["fit"], lab - p - 56), font=font(30, "REGULAR"), fill="#55606F", spacing=8)
        for k, c in enumerate(s["swatch"]):
            d.rounded_rectangle((p + 32 + k * 62, y + h - 74, p + 80 + k * 62, y + h - 26), 12, fill=c, outline="#9CA3AF", width=2)
        for k, f in enumerate(pngs[:2]):
            img.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS), (lab + p + k * (w + p), y))
    img.save(out / "chon-phong-cach.jpg", quality=88)


def font_picker(out):
    """Ảnh so sánh font: cùng phong cách TH, mỗi hàng một font."""
    th = CATALOG[0]
    w, h, p, lab, top = 640, 360, 20, 470, 130
    img = Image.new("RGB", (lab + 2 * (w + p) + p, top + len(FONTS) * (h + p)), "#F4F5F7")
    d = ImageDraw.Draw(img)
    d.text((p * 2, 36), "Chọn font chữ cho video", font=font(58), fill="#1F2937")
    for r, (code, f) in enumerate(FONTS.items()):
        dest = out / "font" / code
        render(th, out, code, dest)
        y = top + r * (h + p)
        d.rounded_rectangle((p, y, lab, y + h), 24, fill="white")
        d.text((p + 32, y + 28), code, font=font(88), fill="#1F2937")
        d.text((p + 32, y + 134), f["name"], font=font(46), fill="#1F2937")
        d.text((p + 32, y + 204), wrap(d, f["fit"], lab - p - 56), font=font(30, "REGULAR"), fill="#55606F", spacing=8)
        for k, name in enumerate(["01-title.png", "05-points.png"]):
            img.paste(Image.open(dest / name).convert("RGB").resize((w, h), Image.LANCZOS), (lab + p + k * (w + p), y))
    img.save(out / "chon-font.jpg", quality=88)
    print("ảnh chọn font:", out / "chon-font.jpg")


def opt(args, name):
    if name not in args:
        return None
    i = args.index(name)
    value = args[i + 1]
    del args[i:i + 2]
    return value


def main():
    args = sys.argv[1:]
    code = opt(args, "--font") or "F1"
    target, hf = opt(args, "--ap-dung"), opt(args, "--hf")
    if target:
        style = next(s for s in CATALOG if s["code"] == target)
        hf = Path(hf).resolve()
        (hf / "assets").mkdir(parents=True, exist_ok=True)
        (hf / "assets" / "phong-cach.css").write_text(style_css(style, code, hf), encoding="utf-8")
        print("Đã ghi", hf / "assets" / "phong-cach.css")
        if style.get("frames"):
            print("Dark Studio: engine/comp.py tự chèn file này vào mọi cảnh khi chạy build.py.")
            return
        print("Dán nội dung file này vào <style> của index.html. Thẻ gắn mỗi khung thêm class:",
              ", ".join(f"{b} → sb sb-{SHORT[b]}" for b in BLOCKS))
        return
    in_skill = (HERE.parent / "series-kits").exists()
    o = opt(args, "--out")
    out = Path(o).resolve() if o else (HERE / "preview" if in_skill else HERE.parent / "anh")
    if "--chon-font" in args:
        out.mkdir(parents=True, exist_ok=True)
        font_picker(out)
        return
    out.mkdir(parents=True, exist_ok=True)
    todo = [s for s in CATALOG if not args or s["code"] in args]
    for s in todo:
        render(s, out, code)
        sheet(s, out)
    if all(len(list((out / s["folder"]).glob("*.png"))) >= 2 for s in CATALOG):   # đủ ảnh mới ghép lại bảng chọn
        picker(out)
        print("ảnh chọn phong cách:", out / "chon-phong-cach.jpg")
    else:
        print("Giữ nguyên chon-phong-cach.jpg: chạy tao_mau.py không kèm mã để dựng lại bảng chọn.")


if __name__ == "__main__":
    main()
