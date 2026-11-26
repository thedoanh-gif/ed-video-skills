# Bộ phong cách và font để người dùng chọn

Người dùng chọn **một mã phong cách** (TH, P1–P6) và **một mã font** (F1–F8) ở bước Input.

| File | Nội dung |
|---|---|
| `styles.json` | 7 phong cách: tên, hợp với, nhạc gợi ý, hình, chuyển động, font nên ghép, tình trạng, nội dung mẫu |
| `fonts.json` | 8 font: tên, hợp với, nguồn, file, `adjust` (cân cỡ chữ theo DINRoundOT) |
| `<phong-cach>/theme.css` | Giao diện cho 7 khung của `th-default/blocks/` (P5 không có: dùng kit `dark-studio`) |
| `fonts/` | Font giấy phép mở đi kèm (xem `fonts/README.md`) |
| `preview/chon-phong-cach.jpg` | **Ảnh gửi người dùng** để chọn phong cách |
| `preview/chon-font.jpg` | **Ảnh gửi người dùng** để chọn font |
| `preview/bang-<phong-cach>.jpg` | Đủ 7 khung của một phong cách, gửi khi người dùng muốn xem kỹ |

| Mã | Phong cách | Hợp với | Nhạc | Font nên ghép |
|---|---|---|---|---|
| TH | TH BlueGold (mặc định) | Chính sách, đào tạo, truyền thông chính thức | calm | F1, F3 |
| P1 | Năng lượng | Sự kiện, phong trào, kêu gọi tham gia | bright | F2, F1 |
| P2 | Tươi mát | Sức khỏe, phúc lợi, môi trường | calm | F5, F1 |
| P3 | Nắng sớm | Kỹ năng, mẹo làm việc, Coffee Monday | bright | F1, F3 |
| P4 | Kẹo ngọt | Văn hóa, gắn kết, ngày lễ | bright | F6, F2 |
| P5 | Dark Studio | Công nghệ, AI, hướng dẫn phần mềm, báo cáo số liệu | focus | F1, F4 |
| P6 | Nhiều màu | Giới thiệu, hướng dẫn vui, truyền thông trẻ | bright | F2, F4 |

Font: F1 DINRoundOT (mặc định, nội bộ) · F2 Montserrat · F3 Segoe UI (Windows) · F4 Roboto · F5 Open Sans · F6 Josefin Sans · F7 Roboto Slab · F8 Constantia (Windows).

## Áp vào dự án
```bash
<python> <skill>/assets/styles/tao_mau.py --ap-dung P1 --font F2 --hf <du-an>/hf
```
Lệnh chép font vào `hf/assets/fonts/` và ghi `hf/assets/phong-cach.css`.

**TH, P1–P4, P6** (khung `th-default/blocks/`):
1. Dán toàn bộ `phong-cach.css` vào `<style>` của `index.html`, **sau** khối `:root` của `frame.md` (để ghi đè màu, font).
2. Mỗi thẻ gắn khung thêm class `sb sb-<ten-ngan>`: `title-card` → `sb sb-title` · `big-number` → `sb sb-number` · `process-steps` → `sb sb-steps` · `compare` → `sb sb-compare` · `three-points` → `sb sb-points` · `key-message` → `sb sb-message` · `cta-outro` → `sb sb-outro`.
3. Đổi phong cách hoặc font thì chạy lại lệnh và thay khối CSS đã dán.

**P5 Dark Studio**: chỉ cần chạy lệnh (khi chọn font khác F1), rồi chạy `build.py`; `engine/comp.py` tự chèn `phong-cach.css` vào mọi cảnh. Chữ nhãn kiểu mono giữ nguyên. Dự án đã chép `engine/` cũ thì chép lại `comp.py` mới.

## Giới hạn
- Giao diện mới dựng và kiểm ở khổ **16:9**. Khổ dọc hoặc vuông phải dựng lại bố cục và kiểm riêng.
- P1–P4, P6 mới kiểm trên 7 khung với nội dung mẫu, chưa dùng cho video dài: xem kỹ ở pilot.
- Chỉ 7 khung dựng sẵn có giao diện riêng. Cảnh viết mới lấy token màu, hình khối của `theme.css`.
- Chữ dài hơn mẫu hoặc font rộng (F2, F7) cần chạy cổng QC và xem khung.

## Dựng lại ảnh mẫu, thêm phong cách hoặc font
- `<python> <skill>/assets/styles/tao_mau.py` (tất cả) · `... --chon-font` (ảnh so font). Ảnh vào `preview/`. Xóa các thư mục PNG sau khi xem xong, giữ file `.jpg`.
- Thêm font: kiểm đủ chữ có dấu tiếng Việt và giấy phép trước, thêm vào `fonts.json`. Đã loại: Lato, Bahnschrift (thiếu chữ).
- Thêm phong cách: thư mục mới có `theme.css` (selector `#root .sb-<ten-ngan>`), thêm vào `styles.json`, dựng ảnh, chạy `<hf> check`.
