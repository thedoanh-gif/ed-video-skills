# -*- coding: utf-8 -*-
"""CH08-CH10: tính ứng dụng, phản hồi học viên, điểm hài lòng."""
from comp import D, X, YEL, BLUE, GREEN, PINK, INK, MUTE, vn
from scene_parts import (DARK, PAPER, GRAY, SOFT, fit, cap, group, pill, block, typed, person, avatar,
                         star_d, check, arrow, stamp, lines, part_card)


# ------------------------------------------------------------------ CH08
def scene_ch08(c):
    n = len(c.lines)
    ap_lines = list(range(2, n - 3))          # 3 dòng nếu chưa đạt mục tiêu, 2 dòng nếu đã đạt
    t1, t2, t3 = c.L(1) - .15, c.L(2) - .15, c.L(-3) - .15
    part_card(c, 0.05, t1, 3, "Ứng dụng và phản hồi", "Học xong, dùng được đến đâu?", t_title=.2, t_sub=.45)
    # b. bài kiểm tra
    c.open_scene(t1, t2)
    c.enter(block(c, 240, 190, 640, 700, PAPER, 28), t1 + .1, "left")
    c.enter(c.text(300, 230, "Bài kiểm tra sau khóa", 48, color=DARK), t1 + .25, "fade")
    for k in range(5):
        y = 350 + k * 88
        c.enter(block(c, 300, y, 52, 52, "rgba(14,17,22,.12)", 12), t1 + .3 + k * .08, "pop", .3)
        c.grow(block(c, 384, y + 12, [420, 360, 440, 330, 400][k], 28, "rgba(14,17,22,.22)", 14), t1 + .35 + k * .08, .35)
        check(c, 300, y - 6, 58, t1 + .7 + k * .22, "#047857", 10)
    pct = D["ty_le_dat"]
    tn = c.L(1) + .1
    c.count(970, 250, pct, tn, 280, GREEN, 1.2, 0, "%", 760, "center", 160)
    c.enter(c.text(970, 556, "học viên đạt bài kiểm tra", 56, w=760, align="center"), tn + .5, "up")
    stamp(c, 570, 740, 280, 120, "ĐẠT", tn + 1.5, "#047857", 76, PAPER)
    diff = round(pct - D["ty_le_dat_muc_tieu"], 1)
    label = f"Cao hơn mục tiêu {vn(diff)} điểm" if diff > 0 else ("Đúng mục tiêu" if diff == 0 else f"Thấp hơn mục tiêu {vn(-diff)} điểm")
    td = c.L(1, 1)
    c.enter(pill(c, 1000, 700, 700, 86, label, GREEN if diff >= 0 else PINK, size=44), td, "slam")
    c.cue(td, "pop")
    c.close_scene()
    # c. đường Học → Làm
    c.open_scene(t2, t3)
    ap, goal = D["ap_dung"], D["ap_dung_muc_tieu"]
    below = ap < goal
    c.enter(c.text(192, 190, "Áp dụng vào công việc sau 3 tháng", 72), t2 + .1, "left")
    x0, w = 330, 1260
    xa, xg = x0 + int(w * ap / 100), x0 + int(w * goal / 100)
    c.enter(block(c, x0, 600, w, 70, "rgba(255,255,255,.12)", 35), t2 + .15, "fade")
    c.enter(c.text(192, 612, "HỌC", 44, color=MUTE), t2 + .2, "left")
    c.enter(c.text(1612, 612, "LÀM", 44, color=INK), t2 + .3, "fade")
    tf = c.L(2, 1) if below else c.L(2) + .8
    c.grow(block(c, x0, 600, xa - x0, 70, GREEN, 35), tf, 1.5)
    c.count(xa - 250, 310, ap, tf, 160, GREEN, 1.5, 0, "%", 500, "center", 100)
    walker = person(c, x0 - 30, 490, 76, INK)
    c.enter(walker, t2 + .35, "pop")
    c.to(walker, tf, {"x": xa - x0}, 1.5, "power2.out")
    c.cue(tf, "swipe")
    tg = c.L(ap_lines[1]) + .15
    with group(c) as flag:
        block(c, xg - 4, 560, 8, 200, YEL, 4)
        pill(c, xg - 180, 770, 360, 74, f"Mục tiêu {vn(goal)}%", YEL, size=40)
    c.enter(flag, tg, "up", .45)
    c.cue(tg, "pop")
    if below:
        th = c.L(ap_lines[2])
        gap = block(c, xa, 600, max(10, xg - xa), 70, PINK, 6)
        c.enter(gap, th, "fade", .3)
        for k in range(3):
            c.to(gap, th + .35 + k * .5, {"opacity": .35}, .22)
            c.to(gap, th + .6 + k * .5, {"opacity": 1}, .22)
        c.enter(c.text(192, 860 - 570, "Học xong: mới nửa đường", 56, color=PINK), th + .2, "left")
        c.to(walker, th + .9, {"x": xa - x0 + 26}, .5, "sine.inOut")
    c.close_scene()
    # d. ba cách học
    c.open_scene(t3, c.dur)
    c.enter(c.text(192, 190, "Cách học tạo khác biệt", 80), t3 + .1, "left")
    h = X["ap_dung_theo_hinh_thuc"]
    times = [c.L(-2) + .35, c.L(-1) + .25, c.L(-1, 1) + .25]
    for k, it in enumerate(h):
        y = 350 + k * 180
        col = [YEL, BLUE, GRAY][k]
        with group(c) as row:
            c.box(192, y, 1536, 150, cls="card")
            c.text(232, y + 48, it["ten"], fit(it["ten"], 46, 400), w=420)
            block(c, 670, y + 52, 860, 46, "rgba(255,255,255,.10)", 23)
            bw = int(860 * it["ty_le"] / 100)
            c.grow(block(c, 670, y + 52, bw, 46, col, 23), times[k], 1.0)
            dot = person(c, 646, y + 34, 56, INK)
            c.to(dot, times[k], {"x": bw}, 1.0, "power2.out")
            c.count(1545, y + 38, it["ty_le"], times[k], 68, col if k < 2 else INK, 1.0, 0, "%", 170, "right", 44)
        c.enter(row, t3 + .2 + k * .15, "up", .4)
        c.cue(times[k], "pop")
    best = c.box(192, 350, 1536, 150, style=f"border:6px solid {YEL};border-radius:26px")
    c.enter(best, times[2] + 1.2, "fade", .3)
    c.close_scene()


# ------------------------------------------------------------------ CH09
def _role(i):
    s = D[f"y_kien_{i}_nguoi"]
    return cap(s[4:] if s.lower().startswith("một ") else s)


def _bubble(c, x, y, w, h, i, t0, t_quote, t_end, tail, color):
    c.enter(c.box(x, y, w, h, style=f"background:{PAPER};border-radius:44px"), t0, "pop", .5)
    tx, ty = {"left": (x - 36, y + h - 130), "right": (x + w - 36, y + h - 130), "bottom": (x + 190, y + h - 36)}[tail]
    c.enter(block(c, tx + 4, ty, 66, 66, PAPER, 10, "transform:rotate(45deg)"), t0 + .1, "fade", .2)
    q = D[f"y_kien_{i}_noi_dung"].rstrip(".")
    size = 66 if len(q) <= 50 else (58 if len(q) <= 90 else 48)
    el = typed(c, x + 60, y + 52, f"“{q}.”", size, w - 120, DARK)
    c.type(el, t_quote, max(.8, (t_end - t_quote) * .85))
    c.enter(pill(c, x + 60, y + h - 104, 560, 68, _role(i), color, size=fit(_role(i), 38, 500)), t_quote - .4, "left")


def scene_ch09(c):
    t1, t2, t3 = (c.L(i) - .15 for i in (1, 2, 3))
    # a. chồng phiếu
    c.open_scene(0.05, t1)
    c.enter(c.text(192, 250, "Học viên<br>nói gì?", 110), .2, "left")
    tn = c.L(0, 1) + .5
    for k in range(9):
        y = 720 - k * 54
        x = 1120 + (k * 37) % 60 - 30
        sheet = c.box(x, y, 480, 150, style=f"background:{PAPER};border-radius:18px;border:3px solid #C7CEDB;transform-origin:center")
        c.enter(sheet, .35 + k * .27, "up", .35)
        if k == 8:
            for j in range(5):
                s = c.svg(x + 70 + j * 72, y + 44, 60, 60, f'<path d="{star_d(60)}" fill="{YEL}"/>')
                c.enter(s, .35 + k * .27 + .3 + j * .1, "pop", .3)
    c.count(192, 570, D["so_phieu"], tn, 200, YEL, 1.2, 0)
    c.enter(c.text(192, 790, "phiếu phản hồi", 64), tn + .4, "up")
    c.cue(tn, "pop")
    c.close_scene()
    # b. kinh doanh: bảng báo giá
    c.open_scene(t1, t2)
    q = c.L(1, 1)
    c.enter(block(c, 192, 260, 520, 600, PAPER, 26), t1 + .1, "left")
    c.enter(c.text(234, 294, "BÁO GIÁ", 52, color=DARK), t1 + .25, "fade")
    for k, w in enumerate([300, 260, 330, 240]):
        y = 400 + k * 74
        c.grow(block(c, 236, y, w, 24, "rgba(14,17,22,.22)", 12), q + .2 + k * .4, .3)
        c.grow(block(c, 590, y, 80, 24, BLUE, 12), q + .35 + k * .4, .25)
    c.cue(q + .2, "tick")
    c.enter(pill(c, 236, 730, 434, 84, "Đã gửi khách ✓", GREEN, size=42), q + 1.4, "slam")
    _bubble(c, 820, 290, 900, 380, 1, t1 + .2, q, t2 - .2, "left", BLUE)
    c.enter(avatar(c, 840, 720, 150, BLUE), t1 + .3, "pop")
    c.cue(t1 + .2, "pop")
    c.close_scene()
    # c. sản xuất: dây chuyền
    c.open_scene(t2, t3)
    q = c.L(2, 1)
    _bubble(c, 192, 260, 980, 420, 2, t2 + .2, q, t3 - .2, "right", YEL)
    c.enter(avatar(c, 1230, 500, 150, YEL), t2 + .3, "pop")
    c.enter(block(c, 192, 830, 1536, 44, "#52606F", 22), t2 + .15, "up")
    for k in range(9):
        c.enter(block(c, 214 + k * 180, 838, 28, 28, DARK, 14), t2 + .2, "fade")
    for k in range(5):
        box_ = block(c, 192 + k * 250, 750, 110, 80, "#C9975B", 10, "border:4px solid #8A6436")
        c.tw(box_, t2, {"x": 0}, {"x": 250, "duration": t3 - t2, "ease": "none"})
    tm = q + (t3 - q) * .6
    c.enter(pill(c, 1260, 250, 440, 150, "+ giờ<br>thực hành", GREEN, size=52), tm, "slam")
    c.cue(t2 + .2, "pop")
    c.cue(tm, "stamp")
    c.close_scene()
    # d. văn phòng: bài học chia nhỏ
    c.open_scene(t3, c.dur)
    q = c.L(3, 1)
    _bubble(c, 192, 210, 1180, 360, 3, t3 + .2, q, c.dur - .5, "bottom", GREEN)
    c.enter(avatar(c, 1480, 330, 200, GREEN), t3 + .3, "pop")
    long = block(c, 192, 740, 1536, 96, GRAY, 20)
    c.grow(long, t3 + .3, .6)
    c.enter(c.text(192, 660, "Bài trực tuyến", 44, color=MUTE), t3 + .35, "fade")
    ts = q + (c.dur - q) * .55
    c.to(long, ts, {"opacity": 0}, .25)
    for k in range(5):
        part = pill(c, 192 + k * 312, 740, 288, 96, f"Phần {k + 1}", BLUE, size=42)
        c.enter(part, ts + k * .12, "pop", .35)
    c.cue(ts, "swipe")
    c.close_scene()


# ------------------------------------------------------------------ CH10
def scene_ch10(c):
    t1, t2 = c.L(1) - .15, c.L(3) - .15
    # a. sao
    c.open_scene(0.05, t1)
    score = X["hai_long"]
    c.enter(c.text(192, 190, "Điểm hài lòng chung", 84), .15, "left")
    for k in range(5):
        x = 360 + k * 250
        frac = max(0, min(1, score - k))
        c.enter(c.svg(x, 360, 200, 200, f'<path d="{star_d(200)}" fill="rgba(255,255,255,.14)"/>'), .25 + k * .08, "pop", .35)
        if frac > 0:
            s = c.box(x, 360, int(200 * frac), 200,
                      f'<svg width="200" height="200" viewBox="0 0 200 200" style="display:block"><path d="{star_d(200)}" fill="{YEL}"/></svg>',
                      style="overflow:hidden")
            c.enter(s, c.L(0) + .5 + k * .24, "fade", .25)
    tn = c.L(0) + .8
    c.count(560, 620, score, tn, 220, YEL, 1.1, 1, "/5", 800, "center", 100)
    prev = D["hai_long_nam_truoc"]
    word = f"Tăng từ {vn(prev)}" if score > prev else (f"Giảm từ {vn(prev)}" if score < prev else "Bằng năm trước")
    td = c.L(0, 1)
    c.enter(pill(c, 1320, 690, 390, 88, word, GREEN if score >= prev else PINK, size=44), td, "slam")
    c.cue(tn, "pop")
    c.cue(td, "stamp")
    c.close_scene()
    # b. bốn tiêu chí
    c.open_scene(t1, t2)
    c.enter(c.text(192, 190, "Theo từng tiêu chí (thang 5)", 76), t1 + .1, "left")
    tc = X["tieu_chi"]
    rows = []
    for k, it in enumerate(tc):
        y = 340 + k * 140
        with group(c) as row:
            card = c.box(192, y, 1536, 112, cls="card")
            c.text(236, y + 30, it["ten"], 46)
            block(c, 720, y + 38, 800, 36, "rgba(255,255,255,.10)", 18)
            bar = block(c, 720, y + 38, int(800 * it["diem"] / 5), 36, GRAY, 18)
            c.grow(bar, t1 + .3 + k * .12, .7)
            c.count(1530, y + 24, it["diem"], t1 + .3 + k * .12, 60, INK, .7, 1, "", 170, "right")
        c.enter(row, t1 + .2 + k * .1, "up", .4)
        rows.append((row, card, bar))
    for idx, line, col, tag in [(0, 1, YEL, "CAO NHẤT"), (len(tc) - 1, 2, BLUE, "THẤP NHẤT")]:
        t = max(c.L(line) + .1, t1 + .75)
        row, card, bar = rows[idx]
        c.to(card, t, {"borderColor": col, "backgroundColor": "rgba(255,255,255,.13)"}, .3)
        c.to(bar, t, {"backgroundColor": col}, .3)
        c.to(row, t, {"x": 16}, .35, "back.out(3)")
        c.enter(pill(c, 500, 340 + idx * 140 + 32, 192, 48, tag, col, size=28), t + .15, "slam")
        c.cue(t, "pop")
    for idx in range(1, len(tc) - 1):
        c.to(rows[idx][0], c.L(2) + .3, {"opacity": .4}, .4)
    c.close_scene()
    # c. ba điều thích nhất
    c.open_scene(t2, c.dur)
    c.enter(c.text(192, 190, "Học viên thích nhất", 84), t2 + .1, "left")
    c.enter(block(c, 192, 330, 1536, 560, "#7A5632", 30, "border:12px solid #5A3E22"), t2 + .15, "up")
    icons = [
        f'<rect x="20" y="60" width="140" height="100" rx="16" fill="{BLUE}"/><path d="M62 60 V38 Q62 26 74 26 H106 Q118 26 118 38 V60" fill="none" stroke="{BLUE}" stroke-width="14"/><rect x="20" y="96" width="140" height="12" fill="{DARK}" opacity=".25"/>',
        f'<path d="M14 34 H130 Q146 34 146 50 V104 Q146 120 130 120 H70 L34 152 V120 H30 Q14 120 14 104 Z" fill="#047857"/><circle cx="52" cy="77" r="9" fill="{PAPER}"/><circle cx="80" cy="77" r="9" fill="{PAPER}"/><circle cx="108" cy="77" r="9" fill="{PAPER}"/>',
        f'<rect x="24" y="30" width="132" height="132" rx="20" fill="{YEL}"/><path d="M52 98 L80 126 L130 70" fill="none" stroke="{DARK}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>',
    ]
    for k in range(3):
        x = 250 + k * 490
        label = D[f"thich_{k + 1}_nhan"]
        t = c.L(4 + k) - .05
        with group(c, f"transform-origin:{x + 220}px 615px") as note:
            c.box(x, 400, 440, 430, style=f"background:{PAPER};border-radius:20px;transform:rotate({[-2.5, 1.5, -1][k]}deg)")
            block(c, x + 198, 380, 44, 44, PINK, 22)
            c.svg(x + 130, 460, 180, 180, icons[k])
            c.text(x + 30, 680, label, fit(label, 52, 400, .5), w=380, color=DARK, align="center")
        c.enter(note, t, "pop", .5)
        c.cue(t, "pop")
    c.close_scene()
