---
name: ed-video-style-library
description: Phân tích kho video mẫu (MP4 + transcript) để rút chuẩn đầu ra về nhịp, cấu trúc, bố cục, màu, motion; viết Style Bible và tạo Series Kit mới.
---

# ED_Video Kit: Style Library

Biến "tôi muốn làm video giống thế này" thành **chuẩn viết ra được, đo được**, để mọi video sau đối chiếu theo.

**Dành cho người quản kit** (phòng Đào tạo), làm một lần khi lập chuẩn hoặc lập series mới. CBNV làm video hằng ngày không cần dùng skill này: họ chỉ cần chọn Series Kit có sẵn trong `ed-video-studio`.

## Đầu vào
- Video mẫu trong `TH-Video/01_library/` (mỗi file ≤ khoảng 400 MB). Nên có transcript `.vtt/.srt` cùng tên (tải từ YouTube hoặc Teams). Không có thì tạo bằng `npx hyperframes transcribe` (xem ed-video-studio `references/voice-to-srt.md`).
- `STYLE-BIBLE.md` hiện tại (nếu có) để **cập nhật**, không viết lại từ đầu.

## Gọi Python (`<python>`)
Trong bộ skill này, `<python>` là lệnh Python 3 chạy được trên máy. Xác định một lần ở đầu phiên rồi dùng xuyên suốt:
- **macOS/Linux**: `python3`.
- **Windows**: thử lần lượt `py -3`, `python`, rồi `%LOCALAPPDATA%\Programs\Python\Python3*\python.exe` (gọi bằng đường dẫn đầy đủ; trong PowerShell đặt `&` phía trước). Không dùng `python3`: trên Windows thường không có. `python` báo "Python was not found" tức là lối tắt Microsoft Store, bỏ qua và thử lệnh kế tiếp. Chỉ nhận lệnh nào chạy `--version` ra Python 3.
- **Windows**: đặt `PYTHONUTF8=1` trước khi chạy script (PowerShell: `$env:PYTHONUTF8='1'`) để không lỗi chữ tiếng Việt.
- Cài thư viện bằng `<python> -m pip install ...`.

## Quy trình

### 1. Đo (máy làm)
```bash
<python> <skill>/scripts/analyze_reference.py "01_library/<video>.mp4" --captions "01_library/<video>.vtt" --out "02_style-bible/analysis/<ten-ngan>"
```
Script cho ra: thời lượng, **nhịp thay đổi hình** (đây mới là số đo đúng cho video motion, vì loại video này ít khi cắt cảnh hẳn), số lần cắt cảnh, bảng màu, tốc độ đọc trên đoạn có transcript, contact sheet theo phút và theo shot.

### 2. Nhìn (agent làm, **bắt buộc xem ảnh**)
Mở **tất cả** contact sheet. Với mỗi video, ghi lại:
- **Cấu trúc**: hook, lời hứa, menu, các phần, kết (kèm mốc thời gian)
- **Danh tính phần**: nhãn chương ở đâu, nền có đổi theo phần không
- **Bố cục và hệ thiết kế**: nền, panel/khung, bo góc, bóng, lưới, vị trí tiêu đề
- **Chữ**: font tiêu đề và nội dung (serif/sans/mono), cách tô màu từ khóa, số chữ mỗi khung
- **Motion**: kiểu vào cảnh, dựng dần, chuyển cảnh, phóng to vào chi tiết, stamp
- **Người dẫn**: giọng thuần / nhân vật / người thật + lower third / face-cam
- **Thiết bị kể chuyện**: giao diện giả lập, so sánh ✓/✗, ẩn dụ hình ảnh
Chữ nhỏ quá không đọc được thì cắt khung ở độ phân giải gốc (`ffmpeg -ss <t> -frames:v 1`) rồi ghép 2×2 để đọc.

### 3. Bóc chuẩn mà video **tự trình bày**
Nhiều video mẫu là bài giảng (về motion, thiết kế, quy trình làm video). Khi đó, **chữ trên màn hình và transcript chính là chuẩn**: nguyên tắc, so sánh tệ/tốt, checklist, danh sách lỗi hay gặp. Đọc hết các khung có chữ, diễn đạt lại bằng lời của mình (không chép nguyên văn), rồi chuyển thành **luật có thể kiểm tra**. Chuẩn quan trọng thì đưa vào `ed-video-studio/references/quality-standards.md` (hoặc đề xuất người dùng cập nhật file đó), và thêm vào rubric review nếu kiểm được.

### 4. Tổng hợp thành Style Bible
Theo `references/style-bible-template.md`:
- **Chuẩn chung** = điểm lặp lại ở nhiều video mẫu. Điểm chỉ có ở một video = đặc trưng của một **bộ phong cách**.
- Mỗi chuẩn phải kiểm được (có con số hoặc có dấu hiệu nhìn thấy). "Đẹp, hiện đại" không phải là chuẩn.
- Số đo của mẫu ≠ chuẩn TH. Điều chỉnh cho người xem nội bộ (ví dụ tốc độ đọc chậm hơn video YouTube) và **ghi lý do**.
- Tăng `version` và ghi ngày. Ghi rõ những gì đã thay đổi so với bản trước.

### 5. Duyệt
Gửi người dùng: 10 chuẩn chính, các bộ phong cách tìm được, và những điểm tự điều chỉnh cho TH. **Chờ duyệt** rồi mới ghi đè `STYLE-BIBLE.md` (trước khi duyệt thì lưu thành `STYLE-BIBLE.draft.md`).

### 6. (Tùy chọn) Tạo Series Kit
Khi người dùng muốn lập series mới, đi theo ed-video-studio `references/series-kit-spec.md`: chép `th-default`, chọn bộ phong cách, chuyển sang màu TH, chốt người dẫn và voice profile.

## Lưu ý bản quyền
Video mẫu chỉ dùng để học **nguyên tắc**. Không sao chép nhân vật, logo, hình minh họa, nhạc hay câu chữ của video mẫu vào video TH. Nhân vật dẫn chuyện phải do TH tự thiết kế.
