# Bảng màu của các phong cách

Người dùng chọn **phong cách** (TH, P1–P6) bằng ảnh `styles/preview/chon-phong-cach.jpg`; màu đi theo phong cách. Font chọn riêng (F1–F8, `styles/fonts.json`). Phong cách đã chọn giữ nguyên cho cả series.

Khi dựng, giá trị trong `styles/<phong-cach>/theme.css` là chuẩn (một số sắc độ đã chỉnh đậm hơn bảng dưới để đủ tương phản). Bảng dưới dùng để nhận diện màu và làm **bảng màu riêng**: lấy phong cách TH rồi thay token trong `frame.md` (`--bg`, `--ink`, `--primary`, `--accent`…).

| Mã | Tên | Nền `--bg` | Chữ `--ink` | Chính `--primary` | Nhấn `--accent` | **Chữ nhấn** `--accent-text` | Nền phụ `--bg-alt` | Hợp với |
|---|---|---|---|---|---|---|---|---|
| **TH** | TH BlueGold (mặc định) | `#F7F0E2` | `#27364A` | `#2F5D9F` | `#B88A2D` | `#9D6F1D` | `#EAF2FC` | Chính sách, đào tạo, truyền thông chính thức |
| **P1** | Năng lượng (cam san hô + xanh ngọc) | `#FFF8F0` | `#1F2937` | `#FF6B4A` | `#14B8A6` | `#E0482A` | `#FFE4DA` | Sự kiện, phong trào, kêu gọi tham gia |
| **P2** | Tươi mát (xanh bạc hà + xanh trời) | `#F2FBF8` | `#12343B` | `#10B981` | `#3B82F6` | `#047857` | `#D1FAE5` | Sức khỏe, phúc lợi, môi trường |
| **P3** | Nắng sớm (vàng nắng + xanh navy) | `#FFFBEA` | `#1E2A44` | `#2563EB` | `#F59E0B` | `#B45309` | `#FEF3C7` | Kỹ năng, mẹo làm việc, Coffee Monday |
| **P4** | Kẹo ngọt (hồng + tím) | `#FFF5FA` | `#2D1B3D` | `#8B5CF6` | `#EC4899` | `#BE185D` | `#FCE7F3` | Văn hóa, gắn kết, ngày lễ |
| **P5** | Dark Studio (theo video mẫu M1) | `#0E1116` (panel `#18202B`) | `#F5F7FA` | `#4F8CFF` | `#FFC542` | `#FFC542` | `#1E2A3A` | Công nghệ, AI, công cụ, hướng dẫn phần mềm |
| **P6** | Nhiều màu (vui tươi, theo video mẫu M2) | `#FFF6E4` | `#23252E` | `#63B3F5` | `#FFC23C` | `#D8432B` | `#FFE9B0` | Giới thiệu, hướng dẫn vui, truyền thông trẻ |

**P6** dùng thêm khối xanh lá `#67CB84`, tím `#AF92F5`, san hô `#FF7A62`; nền chương `#FFE9B0`, `#DDF0FF`, `#DDF6E0`. Chữ trên khối màu luôn dùng `--ink`. P6 là ngoại lệ của luật 2 màu nhấn: mỗi khối một màu, nhưng chữ nhấn chỉ một màu.

**Dark Studio · Nắng sớm** (người dùng đã duyệt, có kit `dark-studio`): nền tối của P5 với khung đổi màu theo phần, nhấn `#F59E0B` `#60A5FA` `#34D399` `#FB7185`; giá trị đầy đủ ở `series-kits/dark-studio/frame.md`.

**Nhạc gợi ý:** TH, P2 → `calm` · P1, P3, P4, P6 → `bright` · P5 → `focus`.

**Quy tắc màu:** `--accent` và `--primary` dùng cho **hình khối, gạch chân, icon, thanh biểu đồ**. **Từ khóa dạng chữ** dùng `--accent-text`, vì màu nhấn tươi trên nền sáng không đủ tương phản để đọc (đã kiểm: ≥ 3.8:1, đạt cho chữ ≥ 48px).

Màu phụ cho danh sách nhiều mục (thẻ số 1–5), dùng theo thứ tự:
- Nền sáng (TH, P1–P4): `#2F5D9F` · `#B88A2D` · `#14B8A6` · `#FF6B4A` · `#8B5CF6`
- Nền tối (P5): `#4F8CFF` · `#FFC542` · `#36D399` · `#FF5C8A` · `#A78BFA`

## Bảng màu tùy chỉnh
Người dùng có thể đưa mã màu riêng (ví dụ màu của một chương trình). Agent kiểm tra:
- Độ tương phản chữ/nền ≥ 4.5:1 (chữ thường) và ≥ 3:1 (chữ ≥ 48px)
- Tối đa 2 màu nhấn, cộng với màu nền và màu chữ
Không đạt thì đề xuất chỉnh lại sắc độ, giữ tông màu người dùng muốn.

## Gửi lựa chọn cho người dùng
Gửi ảnh chọn phong cách và ảnh chọn font, hỏi hai mã (SKILL.md, "Khi bắt đầu"). Người dùng đưa bảng màu riêng thì dựng nhanh một khung `title` để họ nhìn rồi chốt.
