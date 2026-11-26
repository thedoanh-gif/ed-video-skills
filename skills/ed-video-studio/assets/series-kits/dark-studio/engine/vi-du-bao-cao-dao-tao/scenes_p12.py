# -*- coding: utf-8 -*-
"""CH04 (nội dung, ngân sách) và CH05-CH07 (phần 2: Tư duy, AI, chương trình khác).
Mốc giờ lấy theo c.L(dòng, đoạn) nên đổi số hoặc chữ rồi tạo lại giọng thì mốc tự dịch theo."""
from comp import D, X, Y, YEL, BLUE, GREEN, PINK, INK, MUTE, vn
from scene_parts import (DARK, PAPER, GRAY, SOFT, fit, cap, items, group, pill, block, typed, person, avatar,
                         check, cross, arrow, stamp, lines, part_card)

BROWNTXT = "#2A1D12"


def tien(ty):
    return f"{vn(round(ty * 1000), 0)} triệu" if ty < 0.95 else f"{vn(ty)} tỷ"


# ------------------------------------------------------------------ CH04
def scene_ch04(c):
    t1, t2, t3 = (c.L(i) - .15 for i in (1, 2, 3))
    # a. cơ cấu giờ học
    c.open_scene(0.05, t1)
    c.enter(c.text(192, 190, "Giờ học theo nhóm nội dung", 80), .15, "left")
    g = X["nhom"]
    top = max(i["ty_le"] for i in g)
    th = [c.L(0, 0) + 1.0, c.L(0, 1) + .25]
    for k, it in enumerate(g):
        y = 340 + k * 112
        with group(c) as row:
            c.text(192, y + 14, it["ten"], 42, w=470, weight=500)
            bw = int(880 * it["ty_le"] / top)
            bar = block(c, 680, y, bw, 76, GRAY, 16)
            c.grow(bar, .35 + k * .12, .7)
            c.enter(c.text(700 + bw, y + 12, f"{vn(it['ty_le'])}%", 48), .8 + k * .12, "fade")
        c.enter(row, .25 + k * .1, "left", .4)
        if k < 2:
            c.to(bar, th[k], {"backgroundColor": YEL if k == 0 else BLUE}, .3)
            c.to(row, th[k], {"x": 14}, .3, "back.out(3)")
            c.cue(th[k], "pop")
        else:
            c.to(row, th[1] + .7, {"opacity": .38}, .5)
    c.close_scene()
    # b. ngân sách
    c.open_scene(t1, t2)
    plan, act = D["ngan_sach_ke_hoach"], D["ngan_sach_thuc_hien"]
    big = max(plan, act)
    c.enter(c.text(192, 190, f"Ngân sách {Y} (đồng)", 80), t1 + .1, "left")
    tu = c.L(1, 1)
    for k, (name, val, col, t) in enumerate([("Kế hoạch", plan, GRAY, t1 + .35), ("Đã dùng", act, BLUE, tu)]):
        x = 270 + k * 340
        h = int(420 * val / big)
        c.grow(block(c, x, 790 - h, 240, h, col, 18), t, .9, "y")
        c.count(x - 40, 790 - h - 86, val, t, 64, INK, .9, 1, " tỷ", 320, "center", 44)
        c.enter(c.text(x - 30, 818, name, 42, w=300, align="center", color=MUTE), t, "fade")
    pct = round(X["ngan_sach_ty_le"])
    c.ring(1370, 480, 185, min(pct, 100), tu + .7, GREEN if pct <= 100 else PINK, 40, 1.1)
    c.count(1190, 420, pct, tu + .7, 130, INK, 1.1, 0, "%", 360, "center", 76)
    c.enter(c.text(1170, 704, "kế hoạch đã dùng", 40, w=400, align="center", color=MUTE), tu + 1.0, "fade")
    diff = plan - act
    label = f"Thấp hơn {tien(diff)}" if diff > .05 else (f"Vượt {tien(-diff)}" if diff < -.05 else "Đúng kế hoạch")
    td = c.L(1, 2)
    c.enter(pill(c, 1130, 782, 480, 80, label, GREEN if diff >= -.05 else PINK, size=42), td, "slam")
    c.cue(tu, "swipe")
    c.cue(td, "stamp")
    c.close_scene()
    # c. chi phí
    c.open_scene(t2, t3)
    c.enter(c.text(192, 190, "Chi phí đi đâu?", 84), t2 + .1, "left")
    cp = X["chi_phi"]
    mx = max(range(len(cp)), key=lambda k: cp[k]["ty_le"])
    cols = [YEL, BLUE, GREEN, "#A78BFA"]
    th = c.L(2, 1)
    x = 192.0
    for k, it in enumerate(cp):
        w = 1536 * it["ty_le"] / 100
        with group(c) as seg:
            c.grow(block(c, round(x) + 4, 360, max(8, round(w) - 8), 170, cols[k], 16), t2 + .3 + k * .22, .45)
        if k != mx:
            c.to(seg, th - .2, {"opacity": .35}, .4)
        else:
            c.to(seg, th - .2, {"y": -22}, .4, "back.out(2.5)")
        x += w
    for k, it in enumerate(cp):
        cx = 192 + k * 392
        with group(c) as grp:
            card = c.box(cx, 600, 360, 270, cls="card")
            block(c, cx + 32, 632, 44, 44, cols[k], 10)
            c.text(cx + 32, 700, it["ten"], fit(it["ten"], 36, 310, .5), w=320, weight=500)
            c.text(cx + 32, 770, f"{vn(it['ty_le'])}%", 76, color=cols[k])
        c.enter(grp, t2 + .45 + k * .22, "up", .45)
        if k == mx:
            c.to(card, th, {"borderColor": cols[k], "backgroundColor": "rgba(245,158,11,.16)"}, .3)
            c.to(grp, th, {"y": -18}, .35, "back.out(2.5)")
        else:
            c.to(grp, th, {"opacity": .45}, .4)
    c.cue(th, "pop")
    c.close_scene()
    # d. bình quân mỗi người
    c.open_scene(t3, c.dur)
    per = X["chi_phi_moi_nguoi_trieu"]
    c.enter(c.text(192, 190, "Bình quân mỗi người học", 84), t3 + .1, "left")
    c.enter(c.box(192, 360, 620, 500, cls="card"), t3 + .15, "left")
    c.enter(person(c, 392, 430, 220, BLUE), t3 + .35, "pop")
    c.enter(c.text(222, 760, "1 người tham gia", 44, w=560, align="center"), t3 + .55, "fade")
    c.path(792, 520, 200, 120, "M6 100 C60 20 130 20 192 56", t3 + .6, MUTE, 7, .5)
    tp = c.L(3) + 1.1
    tag = pill(c, 990, 420, 700, 250, "", YEL)
    c.enter(tag, tp - .15, "slam")
    c.count(990, 455, per, tp, 160, DARK, .9, 1, " triệu", 700, "center", 84)
    c.enter(c.text(990, 710, "đồng", 56, w=700, align="center"), tp + .3, "up")
    c.enter(c.text(990, 808, f"{vn(act)} tỷ ÷ {vn(X['tong_tham_gia'], 0)} người", 42, w=700, align="center", color=MUTE), tp + 1.0, "up")
    c.cue(tp, "pop")
    c.close_scene()


# ------------------------------------------------------------------ CH05  Tư duy
def scene_ch05(c):
    t1, t2, t3, t4 = (c.L(i) - .15 for i in (1, 2, 3, 4))
    part_card(c, 0.05, t1, 2, "Tư duy và AI", f"Trọng điểm 1: {D['td_ten']}", t_title=.25, t_sub=.5)
    # b. số người tham gia
    c.open_scene(t1, t2)
    tn = c.L(1) + .35
    c.count(192, 230, D["td_nguoi"], tn, 300, YEL, 1.1, 0, "", 1536, "center")
    c.enter(c.text(192, 548, "người tham gia khóa Tư duy", 60, w=1536, align="center"), t1 + .25, "up")
    for k in range(16):
        c.enter(person(c, 240 + k * 92, 700, 64, BLUE if k % 2 == 0 else YEL), tn + .1 + k * .07, "up", .35)
    c.cue(tn, "pop")
    c.close_scene()
    # c. bảng trắng ba bước
    c.open_scene(t2, t3)
    c.enter(c.text(192, 190, "Ba bước luyện tập", 80), t2 + .1, "left")
    c.enter(block(c, 192, 320, 1536, 560, PAPER, 30), t2 + .12, "up", .45)
    steps = items(D["td_buoc_nhan"])[:4]
    n = len(steps)
    w = 1536 // n
    for k, label in enumerate(steps):
        x = 192 + k * w
        t = c.L(2, k) + (.45 if k == 0 else 0)
        num = pill(c, x + w // 2 - 42, 362, 84, 84, str(k + 1), [BLUE, YEL, GREEN, PINK][k], size=48)
        c.enter(num, t, "pop")
        if k % 3 == 0:      # soi vấn đề
            c.path(x + w // 2 - 110, 480, 220, 210, "M95 20 a75 75 0 1 0 .1 0 M150 150 L205 200", t + .15, BROWNTXT, 12, .6)
            c.enter(c.text(x + w // 2 - 60, 520, "?", 100, w=90, color="#B45309", align="center"), t + .6, "pop")
        elif k % 3 == 1:    # rễ nguyên nhân
            c.path(x + w // 2 - 130, 480, 260, 210, "M130 10 L130 80 M130 80 L50 130 L30 195 M50 130 L90 195 M130 80 L210 130 L180 195 M210 130 L240 195", t + .15, BROWNTXT, 12, .8)
            c.enter(block(c, x + w // 2 + 32, 662, 36, 36, PINK, 18), t + 1.0, "pop")
        else:               # thử nhỏ: mầm cây
            c.path(x + w // 2 - 130, 480, 260, 210, "M60 195 L200 195 M130 195 L130 90 M130 120 C80 120 55 85 55 55 C100 50 130 75 130 120 M130 95 C140 50 170 30 215 30 C215 75 180 100 130 95", t + .15, "#047857", 12, .8)
        c.enter(c.text(x + 30, 730, label, 46, w=w - 60, color=BROWNTXT, align="center"), t + .35, "up")
        if k < n - 1:
            arrow(c, x + w - 62, 560, 124, c.L(2, k + 1) - .35, "#B45309", 10, .35)
        c.cue(t, "pop")
    c.close_scene()
    # d. đã dùng vào công việc
    c.open_scene(t3, t4)
    pct = D["td_ap_dung"]
    tr = c.L(3) + .1
    c.ring(520, 530, 250, pct, tr, YEL, 52, 1.4)
    c.count(300, 450, pct, tr, 180, INK, 1.4, 0, "%", 440, "center", 104)
    c.enter(c.text(920, 250, "học viên đã dùng<br>công cụ vào công việc", 60), tr + .5, "up")
    for k, label in enumerate(steps):
        y = 460 + k * 112
        c.enter(c.box(920, y, 780, 92, cls="card"), tr + .7 + k * .15, "right", .4)
        c.text(1030, y + 22, label, 42, weight=500)
        check(c, 950, y + 20, 52, tr + 1.7 + k * .55)
        c.cue(tr + 1.7 + k * .55, "tick")
    c.close_scene()
    # e. cuộc họp đổi câu hỏi
    c.open_scene(t4, c.dur)
    c.enter(c.text(192, 190, "Thay đổi trong cuộc họp", 80), t4 + .1, "left")
    c.enter(block(c, 430, 700, 1060, 130, "#5B4330", 65), t4 + .2, "up")
    for k, (x, y, col) in enumerate([(300, 690, BLUE), (640, 790, GREEN), (1150, 790, YEL), (1500, 690, PINK)]):
        c.enter(avatar(c, x, y, 120, col), t4 + .3 + k * .1, "pop")
    bad, good = D["td_truoc_nhan"], D["td_sau_nhan"]
    with group(c, "transform-origin:560px 470px") as old:
        c.box(250, 360, 620, 220, cls="card", style=f"border-color:{PINK}")
        c.text(250, 388, "TRƯỚC", 34, w=620, color=PINK, align="center")
        c.text(280, 458, f"“{bad}”", fit(bad, 72, 520), w=560, align="center")
    c.enter(old, t4 + .55, "pop")
    tg = c.L(4, 1) + 1.2
    with group(c, "transform-origin:1360px 470px") as new:
        c.box(1050, 360, 620, 220, cls="card", style=f"border-color:{GREEN};background:rgba(52,211,153,.18)")
        c.text(1050, 388, "BÂY GIỜ", 34, w=620, color=GREEN, align="center")
        c.text(1080, 458, f"“{good}”", fit(good, 84, 520), w=560, align="center")
    c.enter(new, tg, "pop", .55)
    ts = c.L(4, 2) + .35
    c.path(270, 450, 580, 110, "M8 86 C180 66 380 44 572 22", ts, PINK, 16, .4)
    c.to(old, ts + .3, {"opacity": .45}, .4)
    c.to(new, ts + .5, {"scale": 1.06, "transformOrigin": "1360px 470px"}, .4, "back.out(2)")
    c.cue(tg, "pop")
    c.cue(ts, "swipe")
    c.close_scene()


# ------------------------------------------------------------------ CH06  AI
def scene_ch06(c):
    t1, t2, t3, t4, t5 = (c.L(i) - .15 for i in (1, 2, 3, 4, 5))
    # a. tên chương trình
    c.open_scene(0.05, t1)
    c.enter(c.text(192, 300, "TRỌNG ĐIỂM 2", 52, color=YEL), .2, "left")
    name = D["ai_ten"]
    c.enter(c.text(192, 390, name, fit(name, 104, 1500)), c.L(0, 1), "up")
    tn = c.L(0, 2) + .25
    c.count(192, 580, D["ai_nguoi"], tn, 210, BLUE, 1.1, 0)
    c.enter(c.text(770, 660, "người học", 76), tn + .5, "left")
    c.cue(tn, "pop")
    c.close_scene()
    # b. cửa sổ chat
    c.open_scene(t1, t2)
    chips = items(D["ai_viec_nhan"])[:3]
    tc = [c.L(1, 0) + .8, c.L(1, 1), c.L(1, 2)]
    for k, label in enumerate(chips):
        i = pill(c, 192 + k * 522, 186, 492, 74, label, SOFT, INK, fit(label, 38, 440))
        c.enter(i, t1 + .15 + k * .08, "up", .35)
        c.to(i, tc[k], {"backgroundColor": BLUE, "color": DARK, "scale": 1.05}, .25)
    c.enter(c.box(192, 300, 900, 590, cls="card"), t1 + .2, "up")
    for k, col in enumerate([PINK, YEL, GREEN]):
        block(c, 224 + k * 40, 326, 22, 22, col, 11)
    c.text(360, 316, "Trợ lý AI", 34, color=MUTE, weight=500)
    ask = D["ai_yeu_cau_nhan"]
    c.enter(block(c, 330, 390, 730, 150, BLUE, 28), tc[0] - .2, "right", .35)
    i = typed(c, 366, 420, ask, 42, 660, DARK)
    c.type(i, tc[0], max(1.0, tc[1] - tc[0] - .5))
    c.cue(tc[0], "click")
    for k in range(5):
        y = 590 + k * 56
        c.enter(c.text(236, y - 14, f"{k + 1}.", 40, color=YEL), tc[1] + k * .22, "fade", .2)
        c.grow(block(c, 300, y, [640, 560, 690, 500, 600][k], 24, "rgba(255,255,255,.45)", 12), tc[1] + .05 + k * .22, .4)
    for k, (title, t) in enumerate([("Email nháp", tc[2]), ("Báo cáo nháp", tc[2] + .9)]):
        y = 300 + k * 305
        with group(c) as grp:
            block(c, 1150, y, 578, 285, PAPER, 24)
            c.text(1190, y + 26, title, 44, color=DARK)
            lines(c, 1190, y + 104, [490, 440, 470] if k == 0 else [200, 300, 250], t + .2, "rgba(14,17,22,.25)", 22, 54)
            if k == 1:
                for j, h in enumerate([70, 110, 150]):
                    c.grow(block(c, 1530 + j * 56, y + 250 - h, 38, h, BLUE, 8), t + .4 + j * .12, .4, "y")
        c.enter(grp, t, "right", .45)
        c.cue(t, "swipe")
    c.close_scene()
    # c. dùng hằng tuần
    c.open_scene(t2, t3)
    pct = D["ai_hang_tuan"]
    c.enter(c.text(192, 220, "Sau 3 tháng", 64, color=MUTE), t2 + .1, "left")
    tn = c.L(2, 1)
    c.count(192, 320, pct, tn, 300, YEL, 1.3, 0, "%", None, "left", 170)
    c.enter(c.text(192, 660, "đang dùng AI<br>hằng tuần", 76), tn + .7, "up")
    lit = round(pct / 5)
    for k in range(20):
        r, col = divmod(k, 5)
        p = person(c, 1040 + col * 136, 230 + r * 165, 100, "rgba(255,255,255,.16)")
        c.enter(p, t2 + .15 + k * .02, "fade", .2)
        if k < lit:
            c.to(p, tn + .1 + k * (1.3 / max(lit, 1)), {"color": BLUE}, .2)
    c.cue(tn, "pop")
    c.close_scene()
    # d. tiết kiệm giờ
    c.open_scene(t3, t4)
    hours = D["ai_gio_tiet_kiem"]
    c.enter(c.text(192, 190, "Thời gian tiết kiệm", 80), t3 + .1, "left")
    c.enter(c.box(250, 330, 540, 540, style=f"border:18px solid {BLUE};border-radius:50%;background:rgba(255,255,255,.05)"), t3 + .15, "pop")
    for k in range(12):
        block(c, 514, 360, 12, 44, MUTE, 6, f"transform-origin:6px 240px;transform:rotate({k * 30}deg)")
    hand = block(c, 510, 410, 20, 200, YEL, 10)
    minute = block(c, 512, 470, 16, 140, INK, 8)
    block(c, 490, 580, 60, 60, YEL, 30)
    for el, a, b in [(hand, 90, -270), (minute, 240, 120)]:
        c.tw(el, t3 + .25, {"rotation": a, "transformOrigin": "50% 100%"},
             {"rotation": b, "transformOrigin": "50% 100%", "duration": t4 - t3 - .8, "ease": "power1.inOut"})
    tn = c.L(3) + 1.5
    c.enter(c.text(900, 340, "khoảng", 56, color=MUTE), tn - .4, "fade")
    c.count(900, 420, hours, tn, 260, GREEN, .8, 1, "", None, "left")
    c.enter(c.text(900, 690, "giờ mỗi tuần", 84), tn - .5, "up")
    c.enter(pill(c, 900, 800, 600, 72, "Người học tự đánh giá", YEL, size=38), c.L(3) + .3, "slam")
    c.cue(tn, "pop")
    c.close_scene()
    # e. chặn dữ liệu nội bộ
    c.open_scene(t4, t5)
    c.enter(c.text(192, 190, "Nhớ nhé", 84, color=YEL), t4 + .1, "left")
    sec = D["ai_cam_nhan"]
    with group(c) as doc:
        block(c, 220, 380, 420, 430, PAPER, 24)
        pill(c, 260, 416, 340, 64, "NỘI BỘ", PINK, size=36)
        lines(c, 264, 520, [330, 280, 320, 240], t4 + .35, "rgba(14,17,22,.25)", 22, 52)
        c.text(240, 740, sec, fit(sec, 38, 380), w=380, color=DARK, align="center")
    c.enter(doc, t4 + .2, "left")
    c.enter(c.box(1260, 400, 440, 390, cls="card", style="border-style:dashed"), t4 + .4, "right")
    c.enter(c.text(1290, 500, "Công cụ<br>chưa được<br>cho phép", 58, w=380, align="center"), t4 + .55, "fade")
    tx = c.L(4, 1)
    c.path(660, 560, 240, 60, "M4 30 L232 30", tx + .15, MUTE, 12, .6)
    c.to(doc, tx + .15, {"x": 70}, .6)
    lock = c.svg(900, 440, 240, 290,
                 f'<path d="M56 130 V84 a64 64 0 0 1 128 0 V130" fill="none" stroke="{YEL}" stroke-width="26"/>'
                 f'<rect x="20" y="124" width="200" height="160" rx="28" fill="{YEL}"/>'
                 f'<circle cx="120" cy="188" r="24" fill="{DARK}"/><rect x="109" y="196" width="22" height="52" rx="8" fill="{DARK}"/>')
    c.enter(lock, tx + .75, "slam")
    c.to(doc, tx + 1.15, {"x": 0}, .45, "back.out(3)")
    cross(c, 1630, 355, 100, tx + 1.5, PINK, 20)
    c.enter(c.text(192, 840, "Không đưa vào công cụ chưa được phép", 52, w=1536, align="center", color=PINK), tx + .35, "up")
    c.cue(tx + .75, "stamp")
    c.close_scene()
    # f. người kiểm tra
    c.open_scene(t5, c.dur)
    tk = c.L(5, 1)
    c.enter(block(c, 260, 200, 760, 690, PAPER, 28), t5 + .1, "up")
    c.enter(c.text(320, 240, "Bản nháp do AI viết", 52, color=DARK), t5 + .25, "fade")
    for k in range(5):
        y = 360 + k * 90
        c.grow(block(c, 400, y, [540, 470, 560, 430, 500][k], 28, "rgba(14,17,22,.22)", 14), t5 + .35 + k * .12, .4)
        check(c, 316, y - 16, 56, tk + .2 + k * .28, "#047857", 10)
        c.cue(tk + .2 + k * .28, "tick")
    c.enter(avatar(c, 1250, 240, 260, BLUE), t5 + .45, "pop")
    c.enter(c.text(1090, 560, "AI viết nháp.<br>Bạn kiểm tra<br>và chịu trách nhiệm.", 62, w=580, align="center"), tk, "up")
    stamp(c, 470, 730, 500, 120, "ĐÃ KIỂM TRA", tk + 1.35, "#047857", 62, PAPER)
    c.close_scene()


# ------------------------------------------------------------------ CH07  chương trình khác
def _backpack(c, x, y):
    return c.svg(x, y, 220, 220,
                 f'<path d="M70 52 C70 4 150 4 150 52" fill="none" stroke="{BLUE}" stroke-width="16"/>'
                 f'<rect x="30" y="44" width="160" height="170" rx="46" fill="{BLUE}"/>'
                 f'<rect x="58" y="128" width="104" height="66" rx="18" fill="{DARK}" opacity=".35"/>'
                 f'<rect x="96" y="118" width="28" height="30" rx="8" fill="{YEL}"/>')


def _board(c, x, y):
    notes = "".join(f'<rect x="{26 + k * 62}" y="{58 + (k % 2) * 26}" width="46" height="46" rx="6" fill="{col}"/>'
                    for k, col in enumerate([YEL, GREEN, PINK]))
    return c.svg(x, y, 220, 220,
                 f'<rect x="8" y="22" width="204" height="150" rx="16" fill="{PAPER}"/>{notes}'
                 f'<path d="M30 150 H190" stroke="{DARK}" stroke-width="8" stroke-linecap="round" opacity=".35"/>'
                 f'<path d="M60 172 L44 214 M160 172 L176 214" stroke="{PAPER}" stroke-width="10" stroke-linecap="round"/>')


def _helmet(c, x, y):
    return c.svg(x, y, 220, 220,
                 f'<path d="M28 148 C28 20 192 20 192 148 Z" fill="{YEL}"/>'
                 f'<rect x="92" y="40" width="36" height="108" rx="12" fill="{DARK}" opacity=".18"/>'
                 f'<rect x="6" y="146" width="208" height="30" rx="15" fill="{YEL}"/>')


def scene_ch07(c):
    c.open_scene(0.05, c.dur)
    c.enter(c.text(192, 190, "Thêm ba chương trình", 80), .15, "left")
    for k, (draw, col) in enumerate([(_backpack, BLUE), (_board, GREEN), (_helmet, YEL)]):
        i = k + 1
        x = 192 + k * 524
        t = c.L(i)
        name, num, res = D[f"ct{i}_ten"], D[f"ct{i}_nguoi"], D[f"ct{i}_nhan"]
        c.enter(c.box(x, 320, 488, 570, cls="card", style="opacity:.45;border-style:dashed"), .5 + k * .15, "fade")
        with group(c) as grp:
            card = c.box(x, 320, 488, 570, cls="card", style="background:rgba(255,255,255,.09)")
            ic = draw(c, x + 134, 345)
            c.text(x + 20, 580, name, fit(name, 44, 440), w=448, align="center")
            c.count(x + 20, 648, num, t + .85, 96, col, .9, 0, "", 448, "center")
            c.text(x + 20, 752, "người học", 34, w=448, align="center", color=MUTE)
        c.enter(grp, t - .05, "up", .5)
        c.to(card, t + .2, {"borderColor": col}, .25)
        c.to(ic, t + .45, {"y": -16, "rotation": -6 if k % 2 == 0 else 6}, .35, "back.out(3)")
        c.to(ic, t + .85, {"y": 0, "rotation": 0}, .35)
        tr = c.L(i, -1)
        c.enter(pill(c, x + 24, 806, 440, 62, res, col, size=fit(res, 34, 400)), tr, "slam")
        if i < 3:
            nxt = c.L(i + 1) - .1
            c.to(grp, nxt, {"opacity": .5}, .35)
            c.to(grp, c.dur - 1.0, {"opacity": 1}, .4)
        c.cue(t, "pop")
    c.close_scene()
