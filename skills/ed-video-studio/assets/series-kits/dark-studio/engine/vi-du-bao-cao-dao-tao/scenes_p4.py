# -*- coding: utf-8 -*-
"""CH11-CH13 và outro: cải thiện, kế hoạch năm sau, tổng kết."""
from comp import D, X, Y, YEL, BLUE, GREEN, PINK, INK, MUTE, vn
from scene_parts import (DARK, PAPER, GRAY, SOFT, fit, cap, group, pill, block, person, avatar,
                         check, arrow, stamp, lines, part_card)


# ------------------------------------------------------------------ CH11
def scene_ch11(c):
    t1, t4 = c.L(1) - .15, c.L(4) - .15
    part_card(c, 0.05, t1, 4, "Cải thiện và kế hoạch", "Cần cải thiện điều gì?", t_title=.2, t_sub=.45)
    # b. ba hàng Hiện tại -> Mong muốn
    c.open_scene(t1, t4)
    c.enter(c.text(900, 188, "HIỆN TẠI", 34, w=300, color=MUTE, align="center"), t1 + .2, "fade")
    c.enter(c.text(1380, 188, "MONG MUỐN", 34, w=300, color=PINK, align="center"), t1 + .3, "fade")
    for k in range(3):
        y = 250 + k * 220
        t = c.L(k + 1) - .05
        tw = c.L(k + 1, 1) + .9
        with group(c) as row:
            c.box(192, y, 1536, 200, cls="card")
            pill(c, 226, y + 56, 88, 88, str(k + 1), PINK, size=50)
            label = D[f"cai_thien_{k + 1}_nhan"]
            c.text(344, y + 70, label, fit(label, 50, 480, .5), w=500)
            arrow(c, 1235, y + 70, 110, tw - .35, MUTE, 8, .35)
            if k == 0:      # giờ thực hành dài ra
                block(c, 880, y + 74, 250, 52, "rgba(255,255,255,.18)", 14)
                block(c, 1138, y + 74, 70, 52, GRAY, 14)
                block(c, 1370, y + 74, 130, 52, "rgba(255,255,255,.18)", 14)
                g = block(c, 1508, y + 74, 190, 52, GREEN, 14)
                c.grow(g, tw, .8)
                c.text(1510, y + 140, "thực hành", 30, w=190, color=GREEN, align="center")
            elif k == 1:    # lớp học xếp vào khe giữa các ca
                for x0 in (880, 1370):
                    block(c, x0, y + 50, 130, 100, "rgba(255,255,255,.18)", 14)
                    block(c, x0 + 200, y + 50, 130, 100, "rgba(255,255,255,.18)", 14)
                    c.text(x0, y + 82, "Ca 1", 30, w=130, color=MUTE, align="center")
                    c.text(x0 + 200, y + 82, "Ca 2", 30, w=130, color=MUTE, align="center")
                pill(c, 950, y + 20, 130, 52, "Lớp", PINK, size=30)
                fix = pill(c, 1500, y + 12, 70, 52, "Lớp", GREEN, size=28)
                c.tw(fix, tw, {"opacity": 0, "y": -50}, {"opacity": 1, "y": 62, "duration": .7, "ease": "back.out(1.8)"})
            else:           # tài liệu dày gấp lại thành 1 trang
                for j in range(6):
                    block(c, 960 + j * 9, y + 130 - j * 18, 150, 36, PAPER, 6, "border:3px solid #8794AD")
                page = block(c, 1455, y + 30, 120, 140, PAPER, 12)
                c.enter(page, tw, "pop", .45)
                c.grow(block(c, 1475, y + 60, 80, 12, GREEN, 6), tw + .25, .3)
                c.grow(block(c, 1475, y + 90, 64, 12, "#8794AD", 6), tw + .35, .3)
                c.grow(block(c, 1475, y + 120, 74, 12, "#8794AD", 6), tw + .45, .3)
        c.enter(row, t, "up", .45)
        c.cue(t, "pop")
        if k < 2:
            c.to(row, c.L(k + 2) - .1, {"opacity": .5}, .35)
            c.to(row, t4 - .9, {"opacity": 1}, .35)
    c.close_scene()
    # c. một mục tiêu
    c.open_scene(t4, c.dur)
    c.enter(c.text(192, 250, "Một mục tiêu chung", 72, w=1536, color=MUTE, align="center"), t4 + .15, "up")
    tg = c.L(4, 1)
    c.enter(c.text(192, 400, "Học xong là làm được", 132, w=1536, align="center"), tg, "pop", .6)
    c.path(640, 570, 640, 30, "M4 20 Q160 4 320 18 T636 14", tg + .6, PINK, 14, .5)
    c.enter(pill(c, 450, 700, 300, 110, "HỌC", SOFT, INK, 56), tg + .2, "left")
    arrow(c, 800, 725, 320, tg + .8, GREEN, 14, .6)
    c.enter(pill(c, 1170, 700, 300, 110, "LÀM", GREEN, DARK, 56), tg + 1.35, "slam")
    c.cue(tg, "pop")
    c.cue(tg + 1.35, "stamp")
    c.close_scene()


# ------------------------------------------------------------------ CH12
def scene_ch12(c):
    t1, t3, t5, t7 = (c.L(i) - .15 for i in (1, 3, 5, 7))
    ns = Y + 1
    # a. ba ưu tiên
    c.open_scene(0.05, t1)
    c.enter(c.text(192, 230, f"Ba ưu tiên {ns}", 120), .2, "left")
    for k, (name, col) in enumerate([("Áp dụng", GREEN), ("AI hằng tuần", BLUE), ("Khối sản xuất", YEL)]):
        h = 200 + k * 110
        x = 300 + k * 460
        with group(c) as step:
            block(c, x, 880 - h, 400, h, col, 24)
            c.text(x, 880 - h + 30, str(k + 1), 96, w=400, color=DARK, align="center")
            c.text(x, 880 - h + 140, name, 40, w=400, color=DARK, align="center")
        c.enter(step, c.L(0) + .9 + k * .35, "up", .45)
        c.cue(c.L(0) + .9 + k * .35, "pop")
    c.close_scene()

    goals = [
        ("Tỷ lệ áp dụng", D["ap_dung"], D["muc_tieu_ap_dung"], GREEN, D["hanh_dong_ap_dung_nhan"]),
        ("Dùng AI hằng tuần", D["ai_hang_tuan"], D["muc_tieu_ai"], BLUE, D["hanh_dong_ai_nhan"]),
        ("Khối sản xuất tham gia", X["sx_ty_le"], D["muc_tieu_san_xuat"], YEL, D["hanh_dong_san_xuat_nhan"]),
    ]
    spans = [(t1, t3), (t3, t5), (t5, t7)]
    for k, ((name, now, goal, col, action), (a, b)) in enumerate(zip(goals, spans)):
        line = 1 + 2 * k
        c.open_scene(a, b)
        for j in range(3):       # thanh định vị 3 ưu tiên
            on = j == k
            i = pill(c, 192 + j * 190, 180, 170, 64, f"Ưu tiên {j + 1}" if on else str(j + 1),
                     col if on else SOFT, DARK if on else MUTE, 30)
        c.enter(c.text(192, 290, name, fit(name, 76, 800, .5)), a + .1, "left")
        tfrom = c.A("từ", c.L(line)) + .15
        tto = c.A("lên", c.L(line)) + .2
        c.count(192, 430, now, tfrom, 170, MUTE, .7, 0, "%", None, "left", 100)
        arrow(c, 530, 490, 130, tto - .25, INK, 12, .3)
        c.count(700, 400, goal, tto, 220, col, .9, 0, "%", None, "left", 130)
        block(c, 192, 680, 880, 40, "rgba(255,255,255,.12)", 20)
        c.grow(block(c, 192, 680, int(880 * now / 100), 40, GRAY, 20), tfrom, .7)
        ext = block(c, 192 + int(880 * now / 100), 680, max(8, int(880 * (goal - now) / 100)), 40, col, 8)
        c.grow(ext, tto + .3, .6)
        th = c.L(line + 1, 1) - .1
        c.enter(c.box(192, 770, 880, 130, cls="card", style=f"border-color:{col}"), th - .35, "up", .4)
        c.enter(c.text(220, 790, "CÁCH LÀM", 28, color=col), th - .25, "fade")
        c.enter(c.text(220, 834, action, fit(action, 42, 820, .48)), th, "left")
        c.cue(tto, "pop")
        c.cue(th, "swipe")
        # hình minh họa bên phải
        c.enter(c.box(1140, 290, 588, 610, cls="card"), a + .2, "right")
        td = th + .5
        if k == 0:       # phiếu bài tập, quản lý ký
            c.enter(block(c, 1220, 340, 430, 510, PAPER, 22), a + .4, "up")
            c.enter(c.text(1260, 372, "Bài tập áp dụng", 44, color=DARK), a + .55, "fade")
            for j in range(3):
                y = 480 + j * 80
                c.enter(block(c, 1260, y, 46, 46, "rgba(14,17,22,.12)", 10), a + .6 + j * .1, "pop", .3)
                c.grow(block(c, 1330, y + 11, [270, 220, 250][j], 24, "rgba(14,17,22,.22)", 12), a + .65 + j * .1, .35)
                check(c, 1260, y - 6, 52, td + j * .45, "#047857", 10)
            c.enter(c.text(1260, 736, "Quản lý ký:", 36, color=DARK, weight=500), td + .6, "fade")
            c.path(1470, 710, 150, 90, "M8 62 C30 20 52 14 56 44 S60 84 84 52 S104 26 112 56 S130 66 144 34", td + 1.4, "#1D4ED8", 8, .9)
        elif k == 1:     # nhóm cùng nhìn màn hình
            c.enter(block(c, 1210, 340, 450, 290, PAPER, 22), a + .4, "up")
            c.enter(pill(c, 1370, 374, 260, 62, "Thử yêu cầu", BLUE, size=30), a + .8, "right")
            for j in range(3):
                c.grow(block(c, 1244, 470 + j * 46, [330, 280, 360][j], 22, "rgba(14,17,22,.22)", 11), td + j * .3, .4)
            for j, cl in enumerate([GREEN, YEL, PINK]):
                av = avatar(c, 1225 + j * 160, 680, 120, cl)
                c.enter(av, a + .6 + j * .15, "up")
                c.to(av, td + .9 + j * .2, {"y": -18}, .25, "power2.out")
                c.to(av, td + 1.2 + j * .2, {"y": 0}, .3, "power2.in")
            c.enter(pill(c, 1290, 826, 290, 54, "Mỗi tháng 1 buổi", YEL, size=28), td + .4, "pop")
        else:            # lớp ngắn cạnh dây chuyền
            factory = c.svg(1190, 340, 488, 260,
                            f'<path d="M10 250 V110 L130 180 V110 L250 180 V110 L370 180 V40 H440 V250 Z" fill="{GRAY}"/>'
                            + "".join(f'<rect x="{40 + j * 80}" y="200" width="44" height="34" rx="6" fill="{PAPER}"/>' for j in range(5)))
            c.enter(factory, a + .4, "up")
            c.enter(block(c, 1190, 630, 488, 30, "#52606F", 15), a + .5, "fade")
            for j in range(4):
                bx = block(c, 1196 + j * 112, 590, 60, 40, "#C9975B", 6)
                c.tw(bx, a, {"x": -20}, {"x": 80, "duration": b - a, "ease": "none"})
            c.enter(pill(c, 1210, 710, 448, 76, "Lớp ngắn theo ca", YEL, size=38), td, "slam")
            for j in range(3):
                c.enter(person(c, 1290 + j * 120, 802, 66, INK), td + .4 + j * .2, "up", .35)
        c.close_scene()
    # c. nguồn lực
    c.open_scene(t7, c.dur)
    c.enter(c.text(192, 190, f"Nguồn lực cho {ns}", 84), t7 + .1, "left")
    c.enter(c.box(192, 350, 740, 520, cls="card"), t7 + .15, "left")
    c.enter(c.text(232, 390, "Giờ học mỗi người", 48, color=MUTE), t7 + .3, "fade")
    tg = c.L(7) + 1.0
    c.count(192, 490, D["muc_tieu_gio"], tg, 240, YEL, 1.0, 1, "", 740, "center")
    c.enter(c.text(192, 760, f"{Y}: {vn(X['gio_tb'])} giờ", 48, w=740, align="center"), tg + .6, "up")
    t8 = c.L(8)
    c.enter(c.box(988, 350, 740, 520, cls="card"), t8 - .15, "right")
    c.enter(c.text(1028, 390, "Ngân sách dự kiến", 48, color=MUTE), t8, "fade")
    c.count(988, 500, D["ngan_sach_nam_sau"], t8 + 1.0, 220, BLUE, 1.0, 1, " tỷ", 740, "center", 100)
    pct = round(X["tang_ngan_sach_nam_sau"])
    label = f"+{pct}% so với {Y}" if pct > 0 else (f"{pct}% so với {Y}" if pct < 0 else f"Bằng {Y}")
    ti = c.L(8, 1)
    c.enter(pill(c, 1148, 750, 420, 82, label, GREEN if pct >= 0 else PINK, size=42), ti, "slam")
    c.cue(tg, "pop")
    c.cue(ti, "stamp")
    c.close_scene()


# ------------------------------------------------------------------ CH13
def scene_ch13(c):
    t3 = c.L(3) - .15
    # a. ba ý chốt
    c.open_scene(0.05, t3)
    c.enter(c.text(192, 190, "Tóm lại", 96), .15, "left")
    for k, (title, col) in enumerate([("Học nhiều hơn", BLUE), ("Tư duy + AI", YEL), ("Học thành làm", GREEN)]):
        x = 192 + k * 524
        t = max(c.L(k) + .1, .8)
        with group(c) as grp:
            c.box(x, 350, 488, 520, cls="card", style=f"border-top:12px solid {col}")
            c.text(x, 760, title, 56, w=488, align="center")
            if k == 0:
                for j, (yr, val) in enumerate([(Y - 1, D["gio_tb_nam_truoc"]), (Y, X["gio_tb"])]):
                    h = int(250 * val / max(D["gio_tb_nam_truoc"], X["gio_tb"]))
                    bx = x + 90 + j * 180
                    c.grow(block(c, bx, 690 - h, 130, h, GRAY if j == 0 else col, 14), t + .5 + j * .35, .7, "y")
                    c.enter(c.text(bx - 20, 690 - h - 58, f"{vn(val)} giờ", 38, w=170, align="center"), t + .9 + j * .35, "fade")
                    c.text(bx - 20, 700, str(yr), 30, w=170, color=MUTE, align="center")
            elif k == 1:
                c.enter(pill(c, x + 80, 450, 330, 80, "Vì sao?", YEL, size=42), t + .4, "left")
                c.enter(pill(c, x + 60, 570, 370, 80, "Tóm tắt giúp tôi", BLUE, size=38), t + .9, "right")
            else:
                c.enter(pill(c, x + 44, 520, 160, 84, "HỌC", SOFT, INK, 40), t + .4, "left")
                arrow(c, x + 210, 532, 80, t + .8, col, 10, .35)
                c.enter(pill(c, x + 292, 520, 160, 84, "LÀM", col, DARK, 40), t + 1.15, "slam")
        c.enter(grp, .35 + k * .12, "up", .4)
        c.to(grp, t, {"y": -20}, .35, "back.out(2.5)")
        if k < 2:
            c.to(grp, c.L(k + 1) - .05, {"y": 0, "opacity": .55}, .35)
        c.cue(t, "pop")
    c.close_scene()
    # b. hai lời kêu gọi
    c.open_scene(t3, c.dur)
    c.enter(c.text(192, 190, "Bắt đầu từ đâu?", 84), t3 + .1, "left")
    t4 = c.L(4) - .05
    with group(c) as mgr:
        c.box(192, 320, 780, 570, cls="card", style=f"border-color:{YEL}")
        pill(c, 232, 350, 320, 68, "Quản lý", YEL, size=38)
        c.text(232, 448, "Chọn 1 kỹ năng cho đội", 52)
        skills = ["Giải quyết vấn đề", "Dùng AI", "An toàn"]
        picked = None
        for j, s in enumerate(skills):
            i = pill(c, 232 + [0, 340, 530][j], 540, [320, 170, 170][j], 66, s, SOFT, INK, 30)
            picked = i if j == 0 else picked
        cal = []
        for j in range(14):
            r, col = divmod(j, 7)
            cal.append(c.box(232 + col * 100, 648 + r * 92, 84, 76, cls="card"))
        c.text(232, 840, "Hẹn xem lại sau 30 ngày", 34, color=MUTE)
    c.enter(mgr, c.L(3) - .05, "left")
    tp = c.L(3, 1) + .5
    cur = c.svg(560, 720, 60, 70, f'<path d="M6 4 L6 56 L20 43 L31 66 L43 60 L32 39 L52 38 Z" fill="{PAPER}" stroke="{DARK}" stroke-width="4"/>')
    c.enter(cur, c.L(3) + .6, "fade", .2)
    c.to(cur, tp - .6, {"x": -170, "y": -150}, .6, "power2.inOut")
    c.to(picked, tp, {"backgroundColor": YEL, "color": DARK, "scale": 1.06}, .25)
    c.cue(tp, "click")
    tc = c.L(3, 2) + .6
    c.to(cur, tc - .5, {"x": 316, "y": 62}, .5, "power2.inOut")
    c.enter(pill(c, 832, 740, 84, 76, "30", GREEN, size=40), tc, "slam")
    c.path(806, 718, 136, 120, "M70 8 C20 6 6 40 8 64 C12 100 50 114 82 108 C120 100 132 76 126 46 C118 14 90 6 56 12", tc + .35, GREEN, 8, .6)
    with group(c) as me:
        c.box(1004, 320, 724, 570, cls="card", style=f"border-color:{GREEN}")
        pill(c, 1044, 350, 320, 68, "Học viên", GREEN, size=38)
        c.text(1044, 448, "Áp dụng 1 điều", 52)
        c.box(1066, 580, 150, 150, style="border:8px solid rgba(255,255,255,.55);border-radius:28px")
        c.text(1260, 590, "Hôm nay", 110, color=GREEN)
        c.text(1260, 720, "một điều vừa học", 40, color=MUTE, weight=500)
    c.enter(me, t4, "right")
    tk = c.L(4, 1) + .9
    check(c, 1076, 570, 170, tk, GREEN, 22, .45)
    c.cue(tk, "chime")
    for j, grp in enumerate((mgr, me)):      # nhắc lại hai lời mời trong lúc chờ hết câu
        c.to(grp, tk + .9 + j * .5, {"y": -18}, .35, "back.out(2)")
        c.to(grp, tk + 1.6 + j * .5, {"y": 0}, .35)
    c.close_scene()


# ------------------------------------------------------------------ OUTRO
def scene_outro(c):
    c.open_scene(0.05, None)
    c.enter(c.text(192, 300, "Học xong là làm được", 124, w=1536, align="center"), .15, "up")
    c.path(640, 462, 640, 30, "M4 20 Q160 4 320 18 T636 14", .6, YEL, 14, .5)
    c.enter(c.text(192, 560, "Cảm ơn đã theo dõi", 64, w=1536, align="center", color=MUTE), .8, "up")
    c.enter(c.text(192, 700, f"Báo cáo đào tạo {Y}", 52, w=1536, align="center", color=BLUE), 1.1, "fade")
    c.close_scene()
    c.cue(.15, "whoosh")
