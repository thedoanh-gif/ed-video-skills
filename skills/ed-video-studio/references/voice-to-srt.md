# Voice → SRT (module dùng trong quy trình, gọi riêng cũng được)

Dùng khi cần: (a) mốc thời gian từng từ để canh motion (bước 4–6), (b) phụ đề SRT cho video, (c) chỉ làm phụ đề cho một bản ghi.

## 1. Lấy transcript
| Đầu vào | Cách làm |
|---|---|
| Đã có .vtt/.srt (YouTube, Teams) | Dùng thẳng, bỏ qua bước nhận dạng giọng |
| File âm thanh hoặc video | `<hf> transcribe <file>`. Xem `--help` để chọn **model lớn** (large-v3 hoặc turbo) và **ngôn ngữ `vi`**. Model nhỏ nghe tiếng Việt kém |

- Video thì tách tiếng trước: `ffmpeg -i in.mp4 -vn -ac 1 -ar 16000 audio/voice.wav`.
- Lần đầu dùng sẽ tải model (1,5–3 GB). Máy không có GPU thì xử lý 5 phút âm thanh có thể mất vài phút. Báo người dùng trước.
- Mở file JSON đầu ra, xem có `words` hoặc `segments[].words` với `start/end` hay không. `to_srt.py` đọc được các dạng phổ biến. Nếu cấu trúc khác thì sửa hàm `words_from_json`.

## 2. Chuyển sang SRT
```bash
# Có kịch bản đã duyệt (ElevenLabs hoặc người đọc theo kịch bản): chữ lấy từ kịch bản, chỉ lấy thời gian từ transcript
<python> <skill>/scripts/to_srt.py transcript.json -o audio/narration.srt --script script-display.txt

# Không có kịch bản (ghi âm tự do): sửa theo bảng thuật ngữ của series
<python> <skill>/scripts/to_srt.py transcript.json -o audio/narration.srt --glossary <series-kit>/glossary.txt
```
Kết quả gồm:
- `narration.srt`: phụ đề (≤ 42 ký tự/dòng, ≤ 2 dòng, 1–6s/khung, ngắt theo dấu câu)
- `narration.words.json`: thời gian từng từ, dùng để canh motion
- `narration.unsure.txt`: các khung cần người kiểm tra bằng tay

Script báo "khớp kịch bản < 60%" nghĩa là người đọc đã nói lệch kịch bản nhiều. Hỏi người dùng nên dùng lời thực tế hay đọc lại.

## 3. AI rà lại (không có kịch bản)
Đọc toàn bộ SRT rồi sửa:
- Lỗi dấu, từ nghe nhầm, tên riêng, thuật ngữ, số liệu (đối chiếu với tài liệu nội dung nếu có)
- Bỏ từ đệm ("ờ", "à", "thì là") trong phụ đề. Lời nói giữ nguyên.
- **Không** đổi nghĩa, **không** viết lại câu cho hay hơn
- Chỗ nào không chắc thì giữ nguyên và ghi vào `unsure.txt`
Lỗi nào lặp lại thì thêm vào `glossary.txt` của series.

## 4. Giao
Gửi `.srt` kèm danh sách các khung chưa chắc (nếu có) để người dùng kiểm tra trong 1–2 phút. Đưa phụ đề vào video có 2 cách:
- **Phụ đề rời** (.srt tải lên LMS hoặc YouTube): mặc định, người xem tự bật hoặc tắt.
- **Phụ đề in thẳng vào hình**: chỉ khi kênh phát không hỗ trợ phụ đề rời (Zalo, màn hình sảnh). Khi đó dựng thành lớp chữ trong HyperFrames theo font và token của kit, hoặc encode lại bằng ffmpeg `subtitles=` với font DINRoundOT.
