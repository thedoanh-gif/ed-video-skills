# -*- coding: utf-8 -*-
"""Đọc du-lieu.txt -> kiểm tra số -> sinh script.md, script-voice.txt,
script-display.txt và data.json (dùng khi dựng hình).
Chạy:  py -3 gen_script.py
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------- đọc dữ liệu
def is_text(k):
    return (k in {"moc_du_lieu", "don_vi", "nhan_gia_lap"}
            or k.endswith(("_ten", "_ket_qua", "_noi_dung", "_nguoi_noi", "_luu_y", "_nhan"))
            and not k.startswith("hl_")
            or k.startswith(("hanh_dong_", "thich_", "cai_thien_"))
            or re.fullmatch(r"y_kien_\d_nguoi", k) is not None)


def parse_num(key, raw):
    s = raw.replace(" ", "")
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", s):
        s = s.replace(".", "")
    s = s.replace(",", ".")
    try:
        v = float(s)
    except ValueError:
        sys.exit(f"LỖI: '{key} = {raw}' không phải là số.")
    return int(v) if v.is_integer() else v


def load():
    d = {}
    for line in (ROOT / "du-lieu.txt").read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            sys.exit(f"LỖI: dòng thiếu dấu '=': {line}")
        k, v = (x.strip() for x in line.split("=", 1))
        d[k] = v if is_text(k) else parse_num(k, v)
    return d


# ------------------------------------------------------------- định dạng số
def vn(x, nd=1):
    """Kiểu hiển thị Việt Nam: 18.600 · 34,5 · 4"""
    x = round(float(x), nd)
    if x.is_integer():
        return f"{int(x):,}".replace(",", ".")
    a, b = f"{x:,.{nd}f}".split(".")
    return a.replace(",", ".") + "," + b


DIG = "không một hai ba bốn năm sáu bảy tám chín".split()


def _under_1000(num, full):
    h, t, u = num // 100, num // 10 % 10, num % 10
    w = []
    if h or full:
        w += [DIG[h], "trăm"]
    if t > 1:
        w += [DIG[t], "mươi"]
    elif t == 1:
        w.append("mười")
    elif u and (h or full):
        w.append("linh")
    if u:
        if u == 1 and t > 1:
            w.append("mốt")
        elif u == 5 and t:
            w.append("lăm")
        elif u == 4 and t > 1:
            w.append("tư")
        else:
            w.append(DIG[u])
    return w


def words_int(num):
    if num == 0:
        return "không"
    groups, w = [], []
    while num:
        groups.append(num % 1000)
        num //= 1000
    units = ["", "nghìn", "triệu", "tỷ"]
    for i in range(len(groups) - 1, -1, -1):
        if not groups[i]:
            continue
        w += _under_1000(groups[i], bool(w))
        if units[i]:
            w.append(units[i])
    return " ".join(w)


def words(x, nd=1):
    x = round(float(x), nd)
    if x.is_integer():
        return words_int(int(x))
    a, b = f"{x:.{nd}f}".split(".")
    tail = " ".join(DIG[int(c)] for c in b) if b.startswith("0") else words_int(int(b))
    return f"{words_int(int(a))} phẩy {tail}"


# Trong lời, số được đánh dấu {n:giá_trị} (số), {p:giá_trị} (phần trăm), {y:năm}.
# Bản hiển thị ra "92%", bản đọc ra "chín mươi hai phần trăm".
def n(x):
    return "{n:%s}" % x


def p(x):
    return "{p:%s}" % round(x)


def y(x):
    """Năm: không có dấu phân hàng nghìn."""
    return "{y:%s}" % x


def render(t, voice):
    def rep(m):
        kind, val = m[1], float(m[2])
        if kind == "y":
            return words_int(int(val)) if voice else str(int(val))
        if kind == "p":
            return f"{words(val, 0)} phần trăm" if voice else f"{vn(val, 0)}%"
        return words(val) if voice else vn(val)
    t = re.sub(r"\{([npy]):([-\d.]+)\}", rep, t)
    # viết hoa chữ đầu câu (kể cả khi câu bắt đầu bằng số đọc thành chữ)
    return re.sub(r"(^|[.?!]\s+|\n)([a-zà-ỹđ])", lambda m: m[1] + m[2].upper(), t)


def cmp_plan(actual, plan):
    r = actual / plan * 100
    if round(r) > 100:
        return f"vượt kế hoạch {p(r - 100)}"
    if round(r) == 100:
        return "đúng kế hoạch"
    return f"đạt {p(r)} kế hoạch"


def trend(now, before):
    if now > before:
        return "tăng"
    if now < before:
        return "giảm"
    return "giữ nguyên"


def vs_target(v, target):
    if v > target:
        return f"cao hơn mục tiêu {n(round(v - target, 1))} điểm"
    if v == target:
        return "đúng bằng mục tiêu"
    return f"thấp hơn mục tiêu {n(round(target - v, 1))} điểm"


def tien(ty):
    return f"{n(round(ty * 1000))} triệu đồng" if ty < 0.95 else f"{n(round(ty, 1))} tỷ đồng"


# ---------------------------------------------------------------- tính toán
D = load()
Y = D["nam"]
ns = Y + 1
X = {}

units = [("Văn phòng", "vp"), ("Kinh doanh", "kd"), ("Sản xuất", "sx")]
X["tong_nhan_su"] = sum(D[f"{k}_nhan_su"] for _, k in units)
X["tong_tham_gia"] = sum(D[f"{k}_tham_gia"] for _, k in units)
X["ty_le_tham_gia"] = X["tong_tham_gia"] / X["tong_nhan_su"] * 100
X["gio_tb"] = round(sum(D[f"{k}_gio"] * D[f"{k}_nhan_su"] for _, k in units) / X["tong_nhan_su"], 1)
X["khoi"] = [{"ten": t, "ma": k,
              "ty_le": round(D[f"{k}_tham_gia"] / D[f"{k}_nhan_su"] * 100),
              "gio": D[f"{k}_gio"]} for t, k in units]
low = min(X["khoi"], key=lambda u: u["ty_le"])
X["khoi_thap_nhat"] = low
X["sx_ty_le"] = X["khoi"][2]["ty_le"]
X["tang_luot_hoc"] = (D["luot_hoc"] / D["luot_hoc_nam_truoc"] - 1) * 100
X["ngan_sach_ty_le"] = D["ngan_sach_thuc_hien"] / D["ngan_sach_ke_hoach"] * 100
X["chi_phi_moi_nguoi_trieu"] = round(D["ngan_sach_thuc_hien"] * 1000 / X["tong_tham_gia"], 1)
X["tang_ngan_sach_nam_sau"] = (D["ngan_sach_nam_sau"] / D["ngan_sach_thuc_hien"] - 1) * 100

NHOM = [("Chuyên môn", "nhom_chuyen_mon", "chuyên môn nghiệp vụ"),
        ("An toàn – chất lượng", "nhom_an_toan", "an toàn và chất lượng"),
        ("Kỹ năng mềm", "nhom_ky_nang", "kỹ năng mềm"),
        ("Quản lý", "nhom_quan_ly", "quản lý, lãnh đạo"),
        ("Hội nhập", "nhom_hoi_nhap", "hội nhập")]
X["nhom"] = sorted([{"ten": a, "ty_le": D[k], "doc": c} for a, k, c in NHOM], key=lambda i: -i["ty_le"])
g = X["nhom"]

HT = [("Kèm cặp tại chỗ", "kem_cap", "kèm cặp tại chỗ"),
      ("Trực tiếp", "truc_tiep", "học trực tiếp"),
      ("Trực tuyến", "truc_tuyen", "học trực tuyến")]
X["ap_dung_theo_hinh_thuc"] = sorted(
    [{"ten": a, "ty_le": D[f"ap_dung_{k}"], "doc": c} for a, k, c in HT], key=lambda i: -i["ty_le"])
h = X["ap_dung_theo_hinh_thuc"]

CP = [("Giảng viên, đối tác", "cp_giang_vien", "giảng viên và đối tác"),
      ("Tổ chức lớp", "cp_to_chuc", "tổ chức lớp"),
      ("Nền tảng, học liệu", "cp_hoc_lieu", "nền tảng và học liệu"),
      ("Khác", "cp_khac", "các khoản khác")]
X["chi_phi"] = [{"ten": a, "ty_le": D[k], "doc": c} for a, k, c in CP]
cp_max = max(X["chi_phi"], key=lambda i: i["ty_le"])

TC = [("Giảng viên", "hl_giang_vien", "giảng viên"),
      ("Nội dung", "hl_noi_dung", "nội dung"),
      ("Tổ chức", "hl_to_chuc", "công tác tổ chức"),
      ("Tài liệu", "hl_tai_lieu", "tài liệu")]
X["tieu_chi"] = sorted([{"ten": a, "diem": D[k], "doc": c} for a, k, c in TC], key=lambda i: -i["diem"])
tc = X["tieu_chi"]
X["hai_long"] = round(sum(D[k] for _, k, _ in TC) / len(TC), 1)

# ---------------------------------------------------------------- kiểm tra số
errors = []
for _, k in units:
    if D[f"{k}_tham_gia"] > D[f"{k}_nhan_su"]:
        errors.append(f"{k}: số tham gia lớn hơn số nhân sự")
for label, keys in [("Cơ cấu nhóm", [k for _, k, _ in NHOM]),
                    ("Cơ cấu chi phí", [k for _, k, _ in CP])]:
    s = sum(D[k] for k in keys)
    if abs(s - 100) > 0.01:
        errors.append(f"{label}: tổng đang là {vn(s)}%, phải bằng 100%")
for _, k, _ in TC:
    if not 0 <= D[k] <= 5:
        errors.append(f"{k}: điểm phải từ 0 đến 5")
if errors:
    sys.exit("LỖI DỮ LIỆU:\n- " + "\n- ".join(errors))

warn = []
if D["ap_dung"] >= D["muc_tieu_ap_dung"]:
    warn.append("Tỷ lệ áp dụng đã đạt mục tiêu năm sau: xem lại CH12.")
if D["ai_hang_tuan"] >= D["muc_tieu_ai"]:
    warn.append("Tỷ lệ dùng AI đã đạt mục tiêu năm sau: xem lại CH12.")
if X["sx_ty_le"] != low["ty_le"]:
    warn.append(f"Khối tham gia thấp nhất giờ là {low['ten']}, không phải Sản xuất: xem lại cải thiện và CH12.")
if X["sx_ty_le"] >= D["muc_tieu_san_xuat"]:
    warn.append("Khối Sản xuất đã đạt mục tiêu năm sau: xem lại CH12.")
if X["gio_tb"] <= D["gio_tb_nam_truoc"]:
    warn.append("Giờ học không tăng so với năm trước: xem lại câu tổng kết CH13.")
if tc[-1]["diem"] >= tc[0]["diem"]:
    warn.append("Các tiêu chí hài lòng bằng điểm nhau: xem lại CH10.")

# ------------------------------------------------------------------- lời đọc
t_luot = trend(D["luot_hoc"], D["luot_hoc_nam_truoc"])
muot = (f"{t_luot} {p(abs(X['tang_luot_hoc']))} so với năm trước"
        if t_luot != "giữ nguyên" else "bằng năm trước")
t_hl = trend(X["hai_long"], D["hai_long_nam_truoc"])
hl = (f"{t_hl} từ {n(D['hai_long_nam_truoc'])}" if t_hl != "giữ nguyên" else "bằng năm trước")

chenh_ns = D["ngan_sach_ke_hoach"] - D["ngan_sach_thuc_hien"]
if chenh_ns > 0.05:
    ns_cau = f"thấp hơn kế hoạch {tien(chenh_ns)}"
elif chenh_ns < -0.05:
    ns_cau = f"vượt kế hoạch {tien(-chenh_ns)}"
else:
    ns_cau = "đúng bằng kế hoạch"

t_ns = trend(D["ngan_sach_nam_sau"], D["ngan_sach_thuc_hien"])
ns_sau = (f"{t_ns} {p(abs(X['tang_ngan_sach_nam_sau']))} so với năm nay"
          if t_ns != "giữ nguyên" else "bằng năm nay")

if D["ap_dung"] < D["ap_dung_muc_tieu"]:
    ap_cau = f"""Nhưng sau ba tháng, chỉ {p(D['ap_dung'])} học viên áp dụng được vào công việc.
Mục tiêu là {p(D['ap_dung_muc_tieu'])}.
[nghỉ]
Học xong mới đi được nửa đường."""
else:
    ap_cau = f"""Sau ba tháng, {p(D['ap_dung'])} học viên áp dụng được vào công việc.
Con số này {vs_target(D['ap_dung'], D['ap_dung_muc_tieu'])}."""

_ngay = X["gio_tb"] / 8  # ngày làm việc 8 giờ
ngay_cau = (f"{words_int(int(_ngay))} ngày" if _ngay == int(_ngay)
            else f"hơn {words_int(int(_ngay))} ngày" if _ngay > 1 else "chưa đầy một ngày")


def ct(i):
    return f"{D[f'ct{i}_ten']}, {n(D[f'ct{i}_nguoi'])} người học: {D[f'ct{i}_ket_qua']}."


def yk(i):
    return f"{D[f'y_kien_{i}_nguoi']} chia sẻ: “{D[f'y_kien_{i}_noi_dung']}.”"


# (mã, tên, lời, ý hình)
C = [
("CH01", "Mở đầu",
f"""Một năm, mỗi người trong {D['don_vi']} dành {n(X['gio_tb'])} giờ để học.
Nghĩa là {ngay_cau} làm việc.
[nghỉ]
Nhưng sau những giờ học đó, điều gì thực sự thay đổi?""",
f"Panel tối: tờ lịch lật, các ô ngày làm việc sáng lên → số \"{vn(X['gio_tb'])} giờ\" phóng lớn → bàn làm việc trước/sau, dấu hỏi vàng khoanh nét tay"),

("CH02", "Nội dung hôm nay",
f"""Mình cùng nhìn lại qua bốn phần.
Một, bức tranh chung.
Hai, chương trình trọng điểm về tư duy và AI.
Ba, tính ứng dụng và tiếng nói học viên.
Bốn, điểm cần cải thiện và kế hoạch năm {y(ns)}.""",
"`menu`: 4 thẻ số lớn 4 màu dựng lần lượt theo lời, thẻ đang đọc sáng, thẻ khác mờ"),

("CH03", "Phần 1 – Quy mô",
f"""Trước hết là quy mô. {D['don_vi']} đã tổ chức {n(D['so_lop_thuc_hien'])} lớp, {cmp_plan(D['so_lop_thuc_hien'], D['so_lop_ke_hoach'])}.
Có {n(D['luot_hoc'])} lượt học, {muot}.
{p(X['ty_le_tham_gia'])} nhân sự đã tham gia ít nhất một khóa.
Riêng khối {low['ten'].lower()} đạt {p(low['ty_le'])}, thấp nhất trong ba khối.""",
f"Panel navy, nhãn P1: lịch lớp đầy dần \"{vn(D['so_lop_thuc_hien'])} lớp\" → cột lượt học {Y-1}/{Y} → lưới 100 hình người sáng {round(X['ty_le_tham_gia'])} → 3 cửa sổ khối, khối thấp nhất viền vàng"),

("CH04", "Phần 1 – Nội dung và ngân sách",
f"""Nhiều giờ học nhất thuộc về {g[0]['doc']}, rồi đến {g[1]['doc']}.
Về ngân sách, {D['don_vi']} đã dùng {n(D['ngan_sach_thuc_hien'])} tỷ đồng, {ns_cau}.
Khoản lớn nhất là {cp_max['doc']}, chiếm {p(cp_max['ty_le'])}.
Bình quân mỗi người tham gia khoảng {n(X['chi_phi_moi_nguoi_trieu'])} triệu đồng.""",
f"5 thanh cơ cấu nội dung, 2 thanh đầu sáng → cột Kế hoạch / Đã dùng \"{round(X['ngan_sach_ty_le'])}%\" → thanh chi phí 4 khúc → thẻ học viên gắn giá \"{vn(X['chi_phi_moi_nguoi_trieu'])} triệu\""),

("CH05", "Phần 2 – Chương trình Tư duy",
f"""Trọng điểm đầu tiên là {D['td_ten'].lower()}.
Đã có {n(D['td_nguoi'])} người tham gia.
Người học luyện cách {D['td_noi_dung']}.
{p(D['td_ap_dung'])} học viên đã dùng công cụ của khóa vào công việc.
Thay đổi dễ thấy: {D['td_ket_qua']}.""",
f"Panel nâu, nhãn P2 · TƯ DUY: bảng trắng 3 bước Vấn đề → Nguyên nhân → Thử nhỏ vẽ dần theo lời → vòng \"{D['td_ap_dung']}%\" → phòng họp, bong bóng \"Lỗi của ai?\" bị gạch, thay bằng \"Vì sao?\""),

("CH06", "Phần 2 – Chương trình AI",
f"""Trọng điểm thứ hai: {D['ai_ten'][0].lower() + D['ai_ten'][1:]}, với {n(D['ai_nguoi'])} người học.
Người học thực hành {D['ai_noi_dung']}.
Sau ba tháng, {p(D['ai_hang_tuan'])} đang dùng AI hằng tuần.
Họ tự đánh giá tiết kiệm khoảng {n(D['ai_gio_tiet_kiem'])} giờ mỗi tuần.
Nhưng nhớ nhé: {D['ai_luu_y']}.
AI viết nháp, còn bạn chịu trách nhiệm kiểm tra.""",
f"Nhãn P2 · AI: cửa sổ chat gõ yêu cầu thật \"Tóm tắt báo cáo này thành 5 ý\", trả lời hiện dần → email và báo cáo nháp → đồng hồ lùi \"{vn(D['ai_gio_tiet_kiem'])} giờ/tuần\" (ghi \"tự đánh giá\") → ổ khóa chặn file nội bộ → con người đóng dấu ĐÃ KIỂM TRA"),

("CH07", "Phần 2 – Chương trình khác",
f"""Ba chương trình khác cũng để lại dấu ấn.
{ct(1)}
{ct(2)}
{ct(3)}""",
f"3 thẻ trượt vào lần lượt: balo ngày đầu ({D['ct1_nguoi']}), bảng họp đội ({D['ct2_nguoi']}), mũ bảo hộ đầu ca ({D['ct3_nguoi']})"),

("CH08", "Phần 3 – Tính ứng dụng",
f"""Học xong, dùng được đến đâu?
{p(D['ty_le_dat'])} học viên đạt bài kiểm tra, {vs_target(D['ty_le_dat'], D['ty_le_dat_muc_tieu'])}.
{ap_cau}
Cách học tạo ra khác biệt.
Với {h[0]['doc']}, tỷ lệ áp dụng là {p(h[0]['ty_le'])}.
Với {h[1]['doc']} là {p(h[1]['ty_le'])}, còn {h[2]['doc']} là {p(h[2]['ty_le'])}.""",
f"Panel xanh rêu, nhãn P3: bài kiểm tra đóng dấu ĐẠT \"{D['ty_le_dat']}%\" → đường Học → Làm dừng ở {D['ap_dung']}%, vạch mục tiêu {D['ap_dung_muc_tieu']}% → 3 làn so sánh theo cách học"),

("CH09", "Phần 3 – Phản hồi học viên",
f"""Học viên nói gì? Mình có {n(D['so_phieu'])} phiếu phản hồi.
{yk(1)}
{yk(2)}
{yk(3)}""",
f"Chồng phiếu đếm lên \"{vn(D['so_phieu'])}\" → 3 bong bóng thoại lời thật, mỗi bong bóng cạnh một nhân vật đúng bối cảnh (bàn bán hàng, dây chuyền, bàn văn phòng)"),

("CH10", "Phần 3 – Điểm hài lòng",
f"""Điểm hài lòng chung đạt {n(X['hai_long'])} trên thang năm, {hl}.
Cao nhất là {tc[0]['doc']}, đạt {n(tc[0]['diem'])}.
Thấp nhất là {tc[-1]['doc']}, ở mức {n(tc[-1]['diem'])}.
Học viên thích nhất ba điều.
{D['thich_1']}.
{D['thich_2']}.
Và {D['thich_3']}.""",
f"5 sao tô dần \"{vn(X['hai_long'])}/5\" → 4 thanh tiêu chí, cao nhất viền vàng, thấp nhất viền xanh → 3 thẻ \"thích nhất\" ghim lên bảng"),

("CH11", "Phần 4 – Điểm cần cải thiện",
f"""Vậy cần cải thiện điều gì?
Một, {D['cai_thien_1']}.
Hai, {D['cai_thien_2']}.
Ba, {D['cai_thien_3']}.
Cả ba đều nhắm tới một mục tiêu: học xong là làm được.""",
"Panel tím than, nhãn P4: 3 hàng Hiện tại → Mong muốn: giờ thực hành dài ra, đồng hồ ca khớp lịch lớp, tài liệu dày gấp lại thành 1 trang"),

("CH12", f"Phần 4 – Kế hoạch {ns}",
f"""Năm {y(ns)} có ba ưu tiên.
Một, nâng tỷ lệ áp dụng từ {p(D['ap_dung'])} lên {p(D['muc_tieu_ap_dung'])}.
Cách làm: {D['hanh_dong_ap_dung']}.
Hai, tăng tỷ lệ dùng AI hằng tuần từ {p(D['ai_hang_tuan'])} lên {p(D['muc_tieu_ai'])}.
Cách làm: {D['hanh_dong_ai']}.
Ba, đưa khối sản xuất từ {p(X['sx_ty_le'])} tham gia lên {p(D['muc_tieu_san_xuat'])}.
Cách làm: {D['hanh_dong_san_xuat']}.
Mục tiêu giờ học là {n(D['muc_tieu_gio'])} giờ mỗi người.
Ngân sách dự kiến {n(D['ngan_sach_nam_sau'])} tỷ đồng, {ns_sau}.""",
f"`process-steps` 3 bậc: {D['ap_dung']}→{D['muc_tieu_ap_dung']} (phiếu bài tập có chữ ký quản lý), {D['ai_hang_tuan']}→{D['muc_tieu_ai']} (nhóm cùng nhìn màn hình chat), {X['sx_ty_le']}→{D['muc_tieu_san_xuat']} (lớp ngắn cạnh dây chuyền) → 2 thẻ nguồn lực"),

("CH13", "Tổng kết + CTA",
f"""Tóm lại, năm {y(Y)} mọi người học nhiều hơn.
Tư duy và AI mở ra cách làm mới.
Việc tiếp theo là biến điều đã học thành điều đã làm.
Nếu bạn là quản lý, hãy chọn một kỹ năng cho đội mình, rồi hẹn xem lại sau {n(30)} ngày.
Nếu bạn là học viên, hãy áp dụng một điều ngay hôm nay.""",
"`three-points`: Học nhiều hơn · Tư duy + AI · Học → Làm → `cta-outro`: lịch khoanh ngày +30, \"Chọn 1 kỹ năng\""),
]

# ------------------------------------------------------------------- xuất file
WPM = 190  # đo từ giọng HoaiMy +12% ở hai tập trước: 185–193 từ/phút
wc = lambda t: len(re.findall(r"\w+", t.replace("[nghỉ]", "")))
rows, voice, disp, tot, speech, longs = [], [], [], 0, 0, []
for code, name, text, visual in C:
    v, s = render(text, True), render(text, False)
    sec = wc(v) / WPM * 60 + 0.7 * text.count("[nghỉ]")
    tot += wc(v)
    speech += sec
    clean = s.replace("[nghỉ]\n", "")
    longs += [(code, x) for x in re.split(r"(?<=[.?!”])\s+", clean) if wc(x) > 22]
    voice.append(f"### {code} – {name}\n{v}")
    disp.append(f"### {code} – {name}\n{clean}")
    rows.append(f"| {code} {name} | {s.replace(chr(10), '<br>')} | {visual} | {sec:.0f} |")

dur = speech + 4 + 3
fm = f"{int(dur // 60)}:{int(dur % 60):02d}"
(ROOT / "script-voice.txt").write_text("\n\n".join(voice) + "\n", encoding="utf-8")
(ROOT / "script-display.txt").write_text("\n\n".join(disp) + "\n", encoding="utf-8")
(ROOT / "data.json").write_text(
    json.dumps({"nhap": D, "tinh": X}, ensure_ascii=False, indent=2), encoding="utf-8")

label = ("Mọi cảnh có số liệu hoặc ý kiến học viên mang nhãn nhỏ **\"NỘI DUNG GIẢ LẬP\"**."
         if D["nhan_gia_lap"].lower().startswith("c") else "Nhãn nội dung giả lập: **đang tắt**.")
md = f"""# KỊCH BẢN: Báo cáo đào tạo {Y}

> **Toàn bộ nội dung là giả lập.** File này sinh tự động từ `du-lieu.txt`: muốn sửa hãy sửa ở đó rồi chạy `gen_script.py`.

## Brief 5 dòng (duyệt cùng kịch bản)
1. **Thông điệp:** Năm {Y} học nhiều hơn, tư duy và AI mở cách làm mới; việc tiếp theo là biến điều đã học thành điều đã làm.
2. **Người xem:** Quản lý các đơn vị và toàn bộ CBNV.
3. **Thời lượng ước tính:** {fm} (tính cả intro 4s, outro 3s) · **Số từ đọc:** {tot}
4. **Giọng:** giọng AI nữ HoaiMy (rate +12%).
5. **Kênh phát:** LMS / Teams, 16:9, 1920×1080.

**Phong cách:** Dark Studio, nhấn tông Nắng sớm · không logo · nhạc nền do người dùng tải.

## Menu
1. Bức tranh chung · 2. Chương trình trọng điểm: Tư duy và AI · 3. Ứng dụng và phản hồi · 4. Cải thiện và kế hoạch {ns}

## Kịch bản

| Phần | Lời đọc | Ý hình (loại cảnh · trên màn hình) | ~giây |
|---|---|---|---|
| Intro | — | `title-card`: "Báo cáo đào tạo {Y}" · "Số liệu đến {D['moc_du_lieu']}" | 4 |
""" + "\n".join(rows) + f"""

{label}

## Cần xác nhận
- Toàn bộ số liệu, tên chương trình, ý kiến học viên, điểm cần cải thiện, mục tiêu và hành động năm {ns} là **giả lập**, chưa có nguồn. Thay bằng nội dung thật trước khi phát hành.
- Ý kiến học viên thật cần được người nói đồng ý trước khi đưa vào video.
"""
(ROOT / "script.md").write_text(md, encoding="utf-8")

print(f"Xong: {tot} từ đọc, ước tính {fm}")
for code, x in longs:
    print(f"Câu dài ({wc(x)} từ) {code}: {x}")
for w in warn:
    print("CẢNH BÁO:", w)
