# Chuẩn bị lời đọc: `script-voice.txt` (dùng cho ElevenLabs, giọng AI `tts_vi.py` và người đọc)

File này chỉ chứa **lời sẽ được đọc**, chia theo chương. Dùng cho ElevenLabs, cho người đọc, và làm đầu vào `--script` để căn phụ đề.

## Định dạng
```
### CH01 – Hook
Bạn có bao giờ mở LMS ra, nhìn danh sách khóa học… rồi đóng lại không?
[nghỉ]
Mình cũng từng vậy.

### CH02 – Hứa
...
```
- Mỗi chương một khối `### CHxx`. Người dùng tạo giọng **theo từng chương** để sửa chương nào chỉ phải tạo lại chương đó.
- `[nghỉ]` = ngắt khoảng 0,7 giây. Trong ElevenLabs có thể thay bằng thẻ break (`<break time="0.7s" />`) nếu model đang dùng hỗ trợ, hoặc xuống dòng hay dấu "…". Kiểm tra trên ElevenLabs trước khi dùng hàng loạt.

## Chuẩn hóa cách đọc (tiếng Việt)
| Dạng viết | Ghi trong file đọc |
|---|---|
| Số: 30%, 1.200, 2027 | "ba mươi phần trăm", "một nghìn hai trăm", "năm hai không hai bảy" (hoặc "hai nghìn không trăm hai mươi bảy" theo kit) |
| Viết tắt: TH, LMS, AOP, AI | Theo cách đọc ở `glossary.txt` của series (ví dụ "tê hát", "en em ét", "ây ai") |
| Ký hiệu: →, /, & | Viết thành chữ: "dẫn tới", "hoặc", "và" |
| Tiếng Anh | Giữ từ phổ biến (e-learning, deadline). Từ hiếm thì thay bằng tiếng Việt |
**Lưu ý:** `script.md` (bản hiển thị) vẫn viết dạng chuẩn (30%, TH). Chỉ `script-voice.txt` viết theo cách đọc. `to_srt.py --script` dùng **bản hiển thị** của lời (`script.md`, cột lời) để phụ đề hiện "30%" thay vì "ba mươi phần trăm". Khi xuất, tạo thêm `script-display.txt` (chỉ lời, dạng chuẩn) cho mục đích này.

## Giọng AI do agent tạo
Cùng file này chạy thẳng: `<python> <ed-video-studio>/scripts/tts_vi.py script-voice.txt --out audio/ --voice <theo Series Kit>`. `[nghỉ]` được đổi thành khoảng lặng 0,7 giây. Nghe thử chương 1 trước, sai cách đọc thì sửa chữ trong file rồi tạo lại riêng chương đó.

## Hướng dẫn người dùng tạo giọng ElevenLabs (gửi kèm)
1. Mở ElevenLabs → Text to Speech → chọn **voice ID trong Series Kit** (không chọn giọng khác).
2. Đặt thông số đúng như Series Kit (stability, similarity, style, speed).
3. Dán từng khối `### CHxx`, tạo giọng, tải về đặt tên `ch01.mp3`, `ch02.mp3`… rồi gửi lại.
4. Nghe lại: chỗ nào đọc sai thì báo, mình sửa cách viết trong `script-voice.txt` rồi bạn tạo lại riêng chương đó.
