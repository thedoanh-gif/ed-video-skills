# -*- coding: utf-8 -*-
"""Mảnh hình dùng lại giữa các cảnh."""
from contextlib import contextmanager
from html import escape

from comp import YEL, BLUE, GREEN, PINK, INK, MUTE

DARK = "#0E1116"
PAPER = "#F5F7FA"
GRAY = "#8794AD"
SOFT = "rgba(255,255,255,.10)"


def fit(s, size, width, k=0.52):
    """Thu cỡ chữ khi dòng dữ liệu dài hơn bề rộng cho phép."""
    return min(size, int(width / (k * max(1, len(s)))))


def cap(s):
    return s[:1].upper() + s[1:]


def items(s):
    return [x.strip() for x in s.split("|") if x.strip()]


@contextmanager
def group(c, extra=""):
    """Nhóm phần tử để chuyển động cùng lúc. Tọa độ con vẫn tính theo khung 1920×1080."""
    i = c.uid()
    c.html.append(f'<div id="{i}" class="scene" style="{extra}">')
    yield i
    c.html.append("</div>")


def pill(c, x, y, w, h, label, bg=GREEN, fg=DARK, size=40):
    return c.box(x, y, w, h, label, "pill", f"background:{bg};color:{fg};font-size:{size}px")


def block(c, x, y, w, h, color, radius=12, extra=""):
    return c.box(x, y, w, h, style=f"background:{color};border-radius:{radius}px;{extra}")


def typed(c, x, y, text, size, width, color=INK, weight=700):
    """Chữ chuẩn bị cho hiệu ứng gõ (gọi c.type(id, t, dur))."""
    spans = "".join(f'<span class="ch">{escape(ch)}</span>' for ch in text)
    return c.text(x, y, spans, size, w=width, color=color, weight=weight)


def person(c, x, y, size, color="rgba(255,255,255,.22)"):
    h = int(size * 1.26)
    body = (f'<circle cx="{size / 2}" cy="{size * .28}" r="{size * .26}" fill="currentColor"/>'
            f'<path d="M{size * .06} {h} C{size * .06} {h * .46} {size * .94} {h * .46} {size * .94} {h} Z" fill="currentColor"/>')
    return c.svg(x, y, size, h, body, f"color:{color}")


def avatar(c, x, y, d, color):
    inner = (f'<circle cx="{d / 2}" cy="{d / 2}" r="{d / 2}" fill="{color}"/>'
             f'<circle cx="{d / 2}" cy="{d * .38}" r="{d * .17}" fill="{DARK}"/>'
             f'<path d="M{d * .2} {d * .83} C{d * .22} {d * .52} {d * .78} {d * .52} {d * .8} {d * .83} Q{d / 2} {d * 1.01} {d * .2} {d * .83} Z" fill="{DARK}"/>')
    return c.svg(x, y, d, d, inner)


def star_d(size):
    pts = [(.5, .04), (.62, .36), (.97, .38), (.69, .6), (.79, .94), (.5, .75), (.21, .94), (.31, .6), (.03, .38), (.38, .36)]
    return "M" + " L".join(f"{a * size:.1f} {b * size:.1f}" for a, b in pts) + " Z"


def check(c, x, y, s, t, color=GREEN, sw=8, dur=.3):
    return c.path(x, y, s, s, f"M{s * .1} {s * .55} L{s * .4} {s * .83} L{s * .92} {s * .18}", t, color, sw, dur)


def cross(c, x, y, s, t, color=PINK, sw=14, dur=.35):
    return c.path(x, y, s, s, f"M{s * .12} {s * .12} L{s * .88} {s * .88} M{s * .88} {s * .12} L{s * .12} {s * .88}", t, color, sw, dur)


def arrow(c, x, y, length, t, color=BLUE, sw=10, dur=.45):
    return c.path(x, y, length, 60, f"M4 30 L{length - 8} 30 M{length - 40} 4 L{length - 6} 30 L{length - 40} 56", t, color, sw, dur)


def stamp(c, x, y, w, h, label, t, color=GREEN, size=64, bg="rgba(14,17,22,.78)"):
    i = c.box(x, y, w, h, label, "pill",
              f"border:8px solid {color};color:{color};font-size:{size}px;border-radius:20px;background:{bg}")
    c.enter(i, t, "slam", .45)
    c.cue(t, "stamp")
    return i


def lines(c, x, y, widths, t, color="rgba(255,255,255,.22)", h=18, gap=40, step=.08):
    """Các dòng chữ giả (thanh ngang) mọc lần lượt."""
    out = []
    for k, w in enumerate(widths):
        i = block(c, x, y + k * gap, w, h, color, h // 2)
        c.grow(i, t + k * step, .35)
        out.append(i)
    return out


def part_card(c, t0, t1, no, title, sub=None, t_title=None, t_sub=None):
    """Thẻ mở phần: số lớn mờ, tên phần, gạch chân."""
    c.open_scene(t0, t1)
    c.enter(c.text(1130, 190, f"0{no}", 480, color="rgba(255,255,255,.08)"), t0 + .05, "right", .7)
    c.enter(c.text(192, 330, f"PHẦN {no}", 56, color=YEL), t0 + .1, "left")
    tt = t0 + .25 if t_title is None else t_title
    size = fit(title, 128, 1300)
    c.enter(c.text(192, 420, title, size), tt, "up")
    c.path(196, 590, 640, 30, "M4 20 Q160 4 320 18 T636 14", tt + .45, YEL, 12, .5)
    if sub:
        c.enter(c.text(192, 660, sub, fit(sub, 60, 1400), color=MUTE), tt + .6 if t_sub is None else t_sub, "up")
    c.cue(t0 + .05, "whoosh")
    c.close_scene()
