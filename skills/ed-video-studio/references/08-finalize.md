# Bước 8: Hoàn thiện

## 1. Sửa theo review
- Đọc `review/review-report.md`. Sửa hết lỗi mức **Phải sửa**. Lỗi mức **Nên sửa** thì sửa nếu chỉ phải render lại ít chương. Những lỗi không sửa thì liệt kê cho người dùng quyết định.
- Chỉ render lại các chương bị ảnh hưởng, rồi ghép lại bằng `join_chapters.py`.

## 2. Xuất theo kênh
| Preset | Kích thước | Giới hạn | Ghi chú |
|---|---|---|---|
| `lms` | 1920×1080 | < 600 MB/video | Kèm .srt rời |
| `teams` | 1920×1080 | gọn nhẹ | Phát qua email hoặc chat |
| `zalo` | 1080×1920 (dọc) hoặc 1080×1080 | càng nhẹ càng tốt | Phụ đề in vào hình. Gửi dạng File để giữ chất lượng |
| `screen` | 1920×1080 | — | Màn hình sảnh thường **không có tiếng**: phụ đề in vào hình, ý chính phải đọc được không cần nghe |
| `youtube` | 1920×1080 | — | Kèm .srt, thumbnail |
Khổ dọc **dựng lại bố cục** (đổi composition), không cắt từ khổ ngang.
Muốn bản nhẹ hơn thì encode lại file cuối (ví dụ `-crf 23..28`), không cần render lại.

## 3. Kiểm tra kỹ thuật lần cuối
```bash
<python> <skill>/scripts/qc_probe.py final/<ten>.mp4 --preset lms --srt final/<ten>.srt
```
Phải hết **FAIL** mới giao. Cảnh báo "khoảng lặng" ở đầu hoặc cuối video thường nghĩa là **chưa có nhạc**.

**Trước khi xin duyệt bản cuối:**
- Đủ thành phần đã chốt ở brief (nhạc, logo, phụ đề). Thiếu gì thì nói ngay trong tin xin duyệt, kèm cách bổ sung.
- Mở HyperFrames Studio cho người dùng xem.
- Chỉ đổi âm thanh sau khi đã render: không render lại hình, chỉ trộn lại rồi ghép (`ffmpeg -i <video> -i <mix.wav> -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -movflags +faststart <ra.mp4>`), lưu thành file riêng cho người dùng nghe so sánh, chốt rồi mới đặt làm bản chính.
- Bản chính phải **cùng tên với file `.srt`**.

## 4. Giao
Thư mục `final/` gồm:
- `yymmdd_ten-video.mp4`, `yymmdd_ten-video.srt`
- `thumbnail.png` (chụp lại khung `title` hoặc một khung đẹp nhất, 1280×720)
- `credits.txt`: nguồn nhạc, ảnh, giọng (ElevenLabs voice ID hoặc tên người đọc)
Tin nhắn giao: 2–3 dòng (đã làm gì, file nào, điểm nào người dùng cần tự kiểm tra), không kể lại các bước.

## 5. Ghi bài học vào Series Kit (bắt buộc)
Thêm một dòng vào mục "Nhật ký series" trong `series-kit.md`: những gì làm tốt nên giữ, lỗi review lặp lại, thông số đã đổi (bộ lọc giọng, âm lượng nhạc…). Thay đổi làm lệch kit (màu, motion, khung cố định mới) thì **hỏi người dùng trước** khi sửa kit. Kit là thứ giữ các tập giống nhau.
