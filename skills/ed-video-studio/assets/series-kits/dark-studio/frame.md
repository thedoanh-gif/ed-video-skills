# frame.md: Design tokens Dark Studio · Nắng sớm

Giá trị lấy từ bản được duyệt. Mã dùng chúng nằm trong `engine/comp.py` (sửa ở đó nếu đổi).

## Color
| Token | Giá trị | Dùng cho |
|---|---|---|
| nền ngoài | `#0E1116` | Nền video, chữ trên khối màu sáng |
| `INK` | `#F5F7FA` | Chữ chính, phiếu giấy |
| `MUTE` | `#AEB8CC` | Chữ phụ, nhãn mono |
| xám so sánh | `#8794AD` | Cột "năm trước", "kế hoạch" |
| `YEL` | `#F59E0B` | Nhấn chính, nhãn phần, gạch tay, nhãn giả lập |
| `BLUE` | `#60A5FA` | Dữ liệu năm nay, công cụ, đường nối |
| `GREEN` | `#34D399` | Đạt, tăng, dấu ✓ |
| `PINK` | `#FB7185` | Thiếu, vượt ngân sách, cấm, dấu ✕ |
| màu thứ năm | `#A78BFA` | Chỉ khi cần đủ 5 mục |

Khung theo phần (chuyển sắc 160°, trên → dưới):
| Khóa | Trên | Dưới | Dùng cho |
|---|---|---|---|
| `mo` | `#1E2A44` | `#141D33` | Mở đầu, tổng kết |
| `p1` | `#1B2C4D` | `#121C34` | Phần 1 |
| `p2` | `#34251A` | `#221811` | Phần 2 |
| `p3` | `#17342C` | `#0F231E` | Phần 3 |
| `p4` | `#2B2046` | `#1C152F` | Phần 4 |

## Typography
- **DINRoundOT** (`fonts/`), Bold cho tiêu đề và số, Medium cho dòng phụ. Chỉ dùng nội bộ TH.
- Người dùng chọn font khác (F2–F8): `assets/styles/tao_mau.py --ap-dung P5 --font <ma> --hf <du-an>/hf` rồi chạy `build.py`; `engine/comp.py` tự chèn.
- Nhãn chương và chân khung: Consolas (`local()`, máy Windows có sẵn), 28px, letter-spacing .14em.
| Vai trò | Cỡ (1920×1080) |
|---|---|
| Số lớn | 270–330 |
| Tên phần | 128–190 |
| Tiêu đề cảnh | 84–96 |
| Dòng chính trong thẻ | 40–70 |
| Nhãn nhỏ | ≥ 28 |

## Shape và bố cục
- Khung lớn: trái 64, trên 48, 1792×984, bo 40, viền trắng 10%.
- Thẻ: nền trắng 6,5%, viền 2px trắng 13%, bo 26. Pill bo tròn hẳn. Không dùng bóng đặc.
- Vùng nội dung: x 192–1728, y 190–890. Nhãn chương (192, 112). Chân khung (192, 934). Nhãn trạng thái: phải 192, trên 108.
- Quầng sáng: tròn 1100px, xanh 16%, trôi chậm suốt cảnh.
