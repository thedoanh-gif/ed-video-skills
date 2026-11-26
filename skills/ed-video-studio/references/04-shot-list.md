# Bước 4: Shot list, chọn khung cảnh và điền nội dung

Mục tiêu: biến kịch bản thành một **timeline đủ chi tiết để dựng mà không phải đoán**. Mỗi cảnh chọn một khung có sẵn trong `blocks/` của Series Kit rồi điền nội dung và mốc giây. Bước này không cần người dùng duyệt: nhịp sẽ được duyệt trên pilot thật ở bước 5.

## 1. Có mốc thời gian thật trước
- Đã có giọng đọc (file ghi âm hoặc ElevenLabs) → chạy `voice-to-srt.md` để có `audio/narration.words.json`. Mọi mốc thời gian đều **lấy từ giọng thật**.
- Chưa có giọng → ước lượng theo tốc độ đọc trong Series Kit (mặc định 180 từ/phút), đánh dấu `ƯỚC LƯỢNG` và căn lại khi có giọng. **Không render thật** khi các mốc còn là ước lượng.

## 2. Viết `shot-list.md` (mẫu: `assets/templates/shot-list.md`)
Mỗi dòng là một shot:

| Cột | Ý nghĩa |
|---|---|
| `id` | `c02-s05` (chương 2, shot 5) |
| `start–end` | giây, lấy theo từ đầu và từ cuối của câu tương ứng |
| `lời` | đoạn lời đọc trong shot |
| `khung` | tên khung trong `blocks/` (title-card, big-number, three-points, compare, process-steps, key-message, cta-outro) hoặc `MỚI: <mô tả>` nếu không khung nào hợp |
| `biến` | nội dung điền vào khung, đúng tên biến trong README của `blocks/` (vd `title`, `items`, `times`) |
| `trên màn hình` | chữ hiển thị (≤ 8 từ), icon, ảnh, số liệu |
| `motion` | phần tử nào vào/ra lúc nào, **neo vào từ khóa** ("số 30% đếm lên khi đọc tới *ba mươi phần trăm*") |
| `âm thanh` | SFX, nhạc lên/xuống |
| `asset` | file cần dùng, kèm trạng thái: có sẵn / cần vẽ / cần người dùng gửi |

### Spec cảnh: đủ 7 mục (quality-standards mục C)
Shot dùng khung có sẵn thì khung đã lo phần nền, bố cục, easing; chỉ cần điền biến và mốc giây. Shot `MỚI` thì phải đủ: **thời lượng · nền · bố cục và vị trí vật thể chính · thứ tự xuất hiện kèm mốc từ lời · kiểu chuyển động + easing · trọng tâm (sáng/lùi) · điều cấm**. Viết theo kiểu "Cách 2" (cụ thể, đo được), không viết "đẹp, hiện đại". Chuyển cảnh được mô tả bằng **logic thị giác** (con số phóng lớn, icon mở bung, góc máy lướt sang…).

### Luật nhịp
- Đổi trạng thái hình **trung bình 4–6 giây/lần, 8–10 lần/phút** (Style Bible mục 1). Khung không có người nói thì không đứng yên quá 10 giây.
- Chữ trên màn hình xuất hiện **cùng lúc hoặc trễ hơn 0,2 giây** so với lúc giọng nói tới ý đó, không được sớm hơn.
- Mỗi chương kết thúc bằng một nhịp "thở" 0,5–1 giây trước thẻ chuyển chương.
- Lời và chữ không lặp nguyên văn nhau: lời giải thích, chữ chốt từ khóa.

## 3. Mốc giây cho biến `times`
Mỗi khung có biến `times` (danh sách giây, tính từ đầu cảnh, ngăn bằng `|`). Lấy từ words.json: giây của từ khóa trừ giây bắt đầu cảnh. Ví dụ cảnh bắt đầu ở 42,0s, giọng đọc tới "thứ nhất" ở 43,1s, "thứ hai" ở 44,9s → `times` = `0.2|1.1|2.9`. Chữ hiện **cùng lúc hoặc trễ tối đa 0,2 giây** so với lời, không sớm hơn.

## 4. Danh sách việc người dùng cần làm
Cuối `shot-list.md` liệt kê mọi asset có trạng thái "cần người dùng gửi", ví dụ logo PNG nền trong suốt, ảnh sản phẩm, file giọng ElevenLabs của chương 3.

Nếu có asset "cần người dùng gửi" (logo, ảnh) mà chưa có, báo người dùng một lần, ngắn gọn, rồi tiếp tục dựng phần không phụ thuộc vào asset đó. Không dừng chờ ở bước này.
