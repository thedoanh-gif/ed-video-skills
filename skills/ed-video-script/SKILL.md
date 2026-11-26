---
name: ed-video-script
description: 'Viết kịch bản video chuẩn TH (lời đọc + ý hình), mặc định ~5 phút: hook, hứa, menu, các phần, tổng kết; kèm bản lời cho giọng AI, ElevenLabs hoặc người đọc.'
---

# ED_Video Kit: Script

Biến brief và tài liệu nguồn thành **kịch bản 2 cột** (lời / ý hình) đúng chuẩn Style Bible và giọng văn của series.

## Đầu vào
- `brief.md`. Nếu gọi riêng mà chưa có brief thì hỏi nhanh: thông điệp chính, người xem, thời lượng, giọng đọc.
- Tài liệu nguồn (chính sách, slide, ghi chú…)
- `STYLE-BIBLE.md` (mục 1, 2, 5) và `series-kit.md` (mục voice profile, giọng văn), nếu có

## Quy trình
1. **Rút lõi**: đọc tài liệu, viết 1 câu thông điệp và tối đa 3–5 ý chính. Thừa ý thì **đề xuất bỏ hoặc chia tập**, không nhồi.
2. **Dàn ý theo khung chuẩn** (`references/structure-5min.md`): chia thời lượng và số từ cho từng phần.
3. **Viết lời** theo `references/voice-writing.md`. Mỗi đoạn lời đi kèm cột ý hình: loại cảnh + thứ hiện trên màn hình (≤ 5–8 từ). Ưu tiên loại cảnh có khung dựng sẵn trong Series Kit (`title-card`, `big-number`, `three-points`, `compare`, `process-steps`, `key-message`, `cta-outro`), vì dựng nhanh và ít lỗi hơn.
4. **Tự kiểm** (checklist bên dưới), rồi sửa.
5. **Xuất 3 file**:
   - `script.md`: bảng đầy đủ (mẫu: `assets/script-template.md`)
   - `script-voice.txt`: chỉ có lời, đã chuẩn hóa cách đọc (`references/elevenlabs-format.md`). Dùng cho ElevenLabs, giọng AI (`tts_vi.py`) hoặc người đọc
   - `script-display.txt`: chỉ có lời, viết dạng chuẩn (30%, TH). Dùng cho `to_srt.py --script` để phụ đề hiển thị đúng
6. **Gửi duyệt (một lần cho cả brief và kịch bản)**. Tin nhắn gửi người dùng có 2 phần:
   - **Brief 5 dòng**: thông điệp chính · người xem · thời lượng + số từ · giọng đọc · kênh phát. Cộng các giả định agent tự quyết (nếu có), mỗi giả định một dòng.
   - **Kịch bản tóm tắt**: hook (1 câu), menu các phần, câu kêu gọi cuối, các chỗ `[CẦN XÁC NHẬN]`, và đường dẫn tới `script.md`.
   Hỏi: "Brief và kịch bản này đã đúng ý chưa? Muốn sửa ý, giọng văn hay độ dài?" Đây là điểm duyệt 1/3 của quy trình: sau khi duyệt mới tạo giọng đọc, vì đổi một chữ sau đó là phải căn lại thời gian cả video.

## Checklist tự kiểm
- [ ] Hook trong 20 giây đầu, có tình huống hoặc câu hỏi cụ thể, không mở bằng "Xin chào, hôm nay chúng ta sẽ…"
- [ ] Có câu hứa ("xem xong bạn sẽ…") và menu đánh số (video dưới 4 phút được bỏ menu)
- [ ] Mỗi phần: mở bằng câu hỏi hoặc tình huống, có ví dụ đời thường, có so sánh hoặc demo, kết bằng câu chốt
- [ ] Tổng số từ trong khoảng của Style Bible (5 phút ≈ 850–950 từ). Ghi rõ số từ và thời lượng ước tính
- [ ] Câu ≤ 20 từ. Không có câu văn hành chính ("nhằm nâng cao", "góp phần thúc đẩy", "trong bối cảnh…")
- [ ] Chữ trên màn hình không lặp nguyên văn lời
- [ ] Số liệu, tên chính sách, điều khoản **đúng theo tài liệu nguồn**. Chỗ nào chưa có nguồn thì đánh dấu `[CẦN XÁC NHẬN]`
- [ ] Có một lời kêu gọi cụ thể ở cuối (làm gì, ở đâu, khi nào)

## Gọi Python (`<python>`)
Trong bộ skill này, `<python>` là lệnh Python 3 chạy được trên máy. Xác định một lần ở đầu phiên rồi dùng xuyên suốt:
- **macOS/Linux**: `python3`.
- **Windows**: thử lần lượt `py -3`, `python`, rồi `%LOCALAPPDATA%\Programs\Python\Python3*\python.exe` (gọi bằng đường dẫn đầy đủ; trong PowerShell đặt `&` phía trước). Không dùng `python3`: trên Windows thường không có. `python` báo "Python was not found" tức là lối tắt Microsoft Store, bỏ qua và thử lệnh kế tiếp. Chỉ nhận lệnh nào chạy `--version` ra Python 3.
- **Windows**: đặt `PYTHONUTF8=1` trước khi chạy script (PowerShell: `$env:PYTHONUTF8='1'`) để không lỗi chữ tiếng Việt.
- Cài thư viện bằng `<python> -m pip install ...`.

## Gọi riêng
Skill dùng được cả ngoài video: lời MC, voice-over cho slide, kịch bản podcast nội bộ. Khi đó bỏ cột ý hình nếu không cần, vẫn giữ giọng văn và checklist.
