---
series: dark-studio
display_name: Dark Studio · Nắng sớm
style_base: Motion graphic nền tối, theo bản "Báo cáo đào tạo 2026" người dùng duyệt ngày 26/11/2026
version: 1.0
---

# Series Kit: Dark Studio · Nắng sớm

Phong cách người dùng đã xem bản thật và **ưng phần hình**. Hợp với: báo cáo, số liệu, AI, công cụ, kỹ năng; xem trên LMS, Teams, máy tính. Ảnh mẫu: `styleframes/` (so khung của tập mới với các ảnh này).

## 0. Lựa chọn của series
| Mục | Lựa chọn |
|---|---|
| Bảng màu | P5 Dark Studio + màu nhấn Nắng sớm (`frame.md`) |
| Giọng đọc | giọng AI `vi-VN-HoaiMyNeural`, rate `+12%` |
| Nhạc nền | AI tạo `calm`, 100 bpm, seed 7 (`audio/theme.mp3`), **giữ một mức suốt video** |
| SFX | AI tạo (`audio/sfx/`) |
| Nhân vật | không dùng (chỉ hình người giản lược khi nói về con người) |
| Logo | không logo (có thì để trong `brand/`) |

Người dùng muốn đổi mục nào ở tập mới thì làm theo, và ghi vào nhật ký.

## 1. Danh tính hình ảnh
- Nền ngoài gần đen, bên trong là **một khung bo tròn lớn** có chuyển sắc, kèm quầng sáng xanh trôi rất chậm.
- **Màu khung đổi theo phần**: mở đầu và tổng kết xanh navy · phần 1 xanh đậm · phần 2 nâu · phần 3 xanh rêu · phần 4 tím. Người xem biết mình đang ở đâu.
- Góc trên trái: nhãn chương chữ mono (`P2 · AI`). Góc dưới trái: 3 ô màu + tên video. Góc trên phải: nhãn trạng thái nếu cần (`NỘI DUNG GIẢ LẬP`).
- Chữ trắng Bold, cỡ lớn, nhiều khoảng trống. Nhấn bằng vàng; so sánh bằng xám với xanh dương; đạt bằng xanh lá; thiếu, cấm, cảnh báo bằng hồng.

## 2. Người dẫn
Giọng thuần, không có hình người dẫn.

## 3. Cảnh: mỗi ý một cảnh có hành động
Không dùng "chữ + icon đứng cạnh". Các kiểu đã dùng và được duyệt (mã mẫu trong `engine/vi-du-bao-cao-dao-tao/`):
| Ý cần nói | Cảnh |
|---|---|
| Mở phần | Số phần rất lớn mờ bên phải, "PHẦN n" vàng, tên phần, gạch tay vàng (`part_card`) |
| Một số lớn | Số đếm lên cỡ 270–330 + hình quy đổi (lịch, thẻ ngày, 100 hình người) |
| So năm trước / kế hoạch | Cột hoặc thanh mọc lên + con dấu `+20%` |
| Cơ cấu theo nhóm | 3 thẻ vòng tỷ lệ, làm mờ các thẻ còn lại khi nêu nhóm thấp nhất |
| Quy trình | Bảng trắng, mũi tên, các bước hiện theo lời |
| Dùng công cụ AI | Cửa sổ chat gõ yêu cầu thật, trả lời hiện dần |
| Điều không được làm | Ổ khóa chặn tài liệu, dấu ✕ vẽ ra |
| Đạt yêu cầu | Phiếu giấy trắng, dấu ✓ lần lượt, đóng dấu "ĐẠT" |
| Ý kiến học viên | Bong bóng trích lời thật + vai người nói + nhãn ý chính |
| Tổng kết, kêu gọi | 3 thẻ ý chính có hình nhỏ; thẻ việc làm theo từng vai |

## 4. Khung cố định
| Khung | Thời lượng | Mô tả |
|---|---|---|
| `intro` | 4s | Nhãn đơn vị, tên video, năm hoặc số tập cỡ lớn màu vàng, thẻ biểu đồ |
| `part_card` | theo lời | Thẻ mở phần |
| `outro` | 3,4s | Khung kết, có nhạc |

## 5. Motion language
Dùng đúng các kiểu trong `engine/comp.py`: `up` (nổi lên) · `pop` · `left`/`right` · `fade` · `slam` (đóng dấu, kèm SFX stamp) · `grow` (cột, thanh mọc) · `count` (đếm số) · `path`/`ring` (vẽ nét, vẽ vòng) · gõ chữ. Chuyển cảnh: mờ dần 0,22s, cảnh cũ nâng nhẹ. Phần tử vào đúng lúc từ khóa được đọc.

## 6. Voice profile
- `vi-VN-HoaiMyNeural` · rate `+12%` · pitch `+0Hz` (người dùng đã duyệt tốc độ này ở pilot).
- Chương nhiều số đọc tới khoảng 230 từ/phút: giới hạn khoảng 4 số mỗi chương, hoặc giảm rate cho chương đó.
- Xưng "mình – bạn", câu ngắn, mỗi phần mở bằng một câu hỏi.

## 7. Âm thanh
- Nhạc: `audio/theme.mp3`, **một mức từ đầu đến cuối** (mặc định của `mix_audio.py`, khoảng -36 LUFS, thấp hơn giọng khoảng 20 dB). Không tự hạ theo giọng.
- SFX: whoosh (mở phần), pop (phần tử vào), swipe, stamp (đóng dấu), tick, click, chime (kết).
- Video đích khoảng -16 LUFS, true peak ≤ -1 dBTP.

## 8. Xuất file
1920×1080, 30 fps, H.264 yuv420p, AAC. Kèm `.srt` cùng tên với video. Phát chủ yếu trên điện thoại thì tăng chữ nhãn từ 28px lên ≥ 36px.

## 9. Nhật ký series
| Tập | Ngày | Bài học / thay đổi kit |
|---|---|---|
| 261126_bao-cao-dao-tao-2026 | 2026-11-26 | Lập kit từ tập này. Người dùng ưng phần hình; muốn nhạc đều; muốn xem Studio trước khi chốt. |
