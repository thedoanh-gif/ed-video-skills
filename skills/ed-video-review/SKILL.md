---
name: ed-video-review
description: 'Review độc lập video motion graphic theo chuẩn TH: chất lượng, độ khớp series, kỹ thuật, góc nhìn khán giả; chấm 100 điểm, xuất danh sách sửa đo được.'
---

# ED_Video Kit: Review

Đóng vai **một người khác** với người đã dựng video: một đạo diễn khó tính cộng một khán giả bận rộn. Mục tiêu là tìm ra những gì cần sửa trước khi phát, không phải khen.

## Chạy độc lập
- Nếu agent có thể giao việc cho **subagent mới** (không mang theo ngữ cảnh lúc dựng), hãy giao review cho subagent đó, chỉ đưa: video, `script.md`, Series Kit, Style Bible, và file này. Người đã dựng thường không thấy được lỗi của chính mình.
- Không có subagent thì tự review, nhưng **không đọc lại `build-log.md` hay ghi chú lúc dựng** trước khi chấm xong. Chấm từ những gì hiện trên màn hình.

## Gọi Python (`<python>`)
Trong bộ skill này, `<python>` là lệnh Python 3 chạy được trên máy. Xác định một lần ở đầu phiên rồi dùng xuyên suốt:
- **macOS/Linux**: `python3`.
- **Windows**: thử lần lượt `py -3`, `python`, rồi `%LOCALAPPDATA%\Programs\Python\Python3*\python.exe` (gọi bằng đường dẫn đầy đủ; trong PowerShell đặt `&` phía trước). Không dùng `python3`: trên Windows thường không có. `python` báo "Python was not found" tức là lối tắt Microsoft Store, bỏ qua và thử lệnh kế tiếp. Chỉ nhận lệnh nào chạy `--version` ra Python 3.
- **Windows**: đặt `PYTHONUTF8=1` trước khi chạy script (PowerShell: `$env:PYTHONUTF8='1'`) để không lỗi chữ tiếng Việt.
- Cài thư viện bằng `<python> -m pip install ...`.

## Chuẩn bị bằng chứng
```bash
<python> <skill>/scripts/review_frames.py <video.mp4> --out review/ [--ref <thu-muc-style-frames>] [--srt audio/narration.srt]
```
Script tạo ra: khung hình mỗi 5 giây kèm contact sheet, **bản thu nhỏ cỡ điện thoại**, **khung so sánh MẪU | CỦA BẠN** (nếu có `--ref`), và bảng nhịp thay đổi hình. **Phải xem ảnh** (contact sheet, các khung so sánh, khung cỡ điện thoại), không chỉ đọc số. Thêm `qc_probe.py` của ed-video-studio cho phần kỹ thuật, và đọc báo cáo cổng QC gần nhất của HyperFrames (`hf/.hyperframes/artifacts/checks/*.json`) nếu có.

Hai giới hạn đã gặp của `review_frames.py`:
- Windows: có thể không ghép được contact sheet (ffmpeg không hỗ trợ glob) → ghép bằng ffmpeg theo dãy số (`-i frame_%03d.png -vf tile=...`).
- Video nền tối: bảng nhịp (`beats.json`) bỏ sót thay đổi và báo đứng hình giả → tự đo chênh lệch giữa các khung (4 khung/giây) trước khi kết luận.

## 5 lăng kính (chi tiết: `references/rubric.md`)
1. **Chuẩn chất lượng**: 5 nguyên tắc, phép thử poster, chữ cắt / đè / hàng thẳng, 5 lỗi AI hay mắc, nhịp 8–10 lần/phút
2. **Độ khớp Series Kit**: màu, font, khung cố định, motion language, giọng, nhạc
3. **Kỹ thuật**: kết quả `qc_probe.py`, đồng bộ hình-lời, phụ đề
4. **Khán giả**: xem lại video qua 2–3 persona trong `references/audience-personas.md`. Ở từng thời điểm, persona đó còn xem tiếp không, có hiểu không, có nhớ được gì không
5. **Sức hút & chuyển động so với video mẫu** (bắt buộc): đạt quy ước chưa đủ, phải **hấp dẫn người học**. Đặt khung của video cạnh video mẫu trong `01_library` (hoặc `...\06_ED\1. Video mẫu\`), cùng đoạn 30–40s, xem chuyển động có phù hợp từng ý lời đọc không: chữ/hộp ra đúng nhịp từ khóa, nhấn mạnh bằng khoanh/gạch/✓✕, hình diễn tả bằng hành động, cảnh luôn "sống", chuyển cảnh có chủ đích. Cảnh nào đứng im, chỉ hiện chữ + tranh tĩnh thì ghi **Phải sửa**. Chi tiết: mục 5 của `references/rubric.md`

## Báo cáo
Viết `review/review-report.md` theo `references/report-template.md`:
- **Kết luận theo cổng, không theo điểm:**
  - `PHÁT ĐƯỢC` chỉ khi danh sách **Phải sửa = 0** (và `qc_probe.py` không có FAIL).
  - Còn mục Phải sửa → `SỬA RỒI PHÁT` (sửa được bằng render lại vài chương) hoặc `CẦN LÀM LẠI PHẦN…`.
  - **Điểm 100** vẫn chấm để theo dõi xu hướng giữa các tập, nhưng không dùng làm ngưỡng phát: điểm do AI tự chấm dễ cao hơn thực tế, còn một lỗi "Phải sửa" (chữ bị cắt, sai số liệu) đủ làm hỏng video dù điểm cao.
  - Mục là "Phải sửa" khi: sai nội dung/số liệu so với nguồn, chữ bị cắt/đè/tràn mép, lệch hình-lời > 0,5 giây, khung trống hoặc đứng hình > 15 giây, mất tiếng, sai màu/font/logo của kit, lỗi kỹ thuật làm không phát được trên kênh.
- Danh sách sửa xếp theo mức **Phải sửa / Nên sửa / Cân nhắc**. Mỗi mục có **mốc thời gian + vấn đề + cách sửa đo được** ("tiêu đề c03-s02 to thêm 20%, nhích lên 40px"; không viết "chưa đẹp lắm").
- Tối đa 3 điểm **làm tốt nên giữ**, để đưa vào nhật ký Series Kit.
- Những lỗi lặp lại nhiều lần thì đề xuất **luật mới cho Series Kit** để tập sau không mắc lại.

Gửi người dùng bản tóm tắt: kết luận, số mục Phải sửa, 3–5 việc phải sửa quan trọng nhất, đường dẫn báo cáo. Khi review chạy trong quy trình của ed-video-studio, agent dựng tự sửa các mục Phải sửa (tối đa 2 vòng review) rồi mới gửi bản cuối cho người dùng duyệt.
