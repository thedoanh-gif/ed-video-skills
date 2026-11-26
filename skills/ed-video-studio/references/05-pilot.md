# Bước 5: Pilot, dựng thật chương 1 rồi duyệt hình + nhịp

Mục tiêu: trước khi dựng cả 5 phút, người dùng **xem một đoạn video thật** (chương 1, hoặc 30 giây đầu nếu chương 1 dài) ở chất lượng gần với bản cuối: đúng màu, font, khung cảnh, giọng, nhạc. Một lần duyệt này thay cho hai lần duyệt cũ (style frames + animatic khối màu), vì người không chuyên khó nhận xét nhịp trên hình giả.

## Đầu vào
`script.md` đã duyệt, giọng đọc + `*.words.json` (bước 3), `shot-list.md` (bước 4), Series Kit (`frame.md`, `series-kit.md`, `blocks/`), Style Bible.

## 1. (Chỉ ở chế độ Kỹ) Style frames trước
Dựng 4–6 khung đại diện bằng chính các khung cảnh trong `blocks/` với nội dung thật, chụp bằng `<hf> snapshot --no-end --at <giây> -o styleframes/`, gửi duyệt. Chế độ mặc định bỏ qua mục này: ảnh tĩnh sẽ được chụp từ pilot ở mục 4.

## 2. Dựng pilot
- Khởi tạo dự án và chép kit theo `06-build.md` mục 1–2.
- Dựng **chương 1 đầy đủ**: intro của series, các cảnh theo shot list (mỗi cảnh là một khung trong `blocks/`, mốc giây lấy từ words.json), giọng, nhạc, SFX.
- Chạy **cổng QC** (`06-build.md` mục 7). Pilot phải qua cổng rồi mới gửi người dùng.
- Render chất lượng `looks` (mặc định), ra `renders/pilot.mp4`.

## 3. Loại cảnh và khung tương ứng
Loại cảnh nào cũng ưu tiên dùng khung có sẵn:
| Loại cảnh | Dùng khi | Bố cục |
|---|---|---|
| `title` | Mở video, mở chương | Tiêu đề lớn, nền giấy, một đường gạch vàng chạy ra |
| `talking` | Người nói, ý cảm xúc | Face-cam tròn có viền nhịp tim, 1 dòng chữ khóa |
| `point` | Một ý chính | 1 câu ≤ 8 từ + 1 icon hoặc minh họa |
| `list` | 3–5 ý song song | Các thẻ xuất hiện lệch nhau, mỗi thẻ ≤ 5 từ |
| `flow` | Quy trình, các bước | Sơ đồ có mũi tên vẽ dần |
| `data` | Số liệu | Một con số lớn đếm lên + 1 dòng giải thích |
| `compare` | Trước/sau, đúng/sai | Chia đôi màn hình |
| `quote` | Trích dẫn, câu chốt | Chữ lớn, nhiều khoảng trống |
| `screen` | Hướng dẫn phần mềm | Khung màn hình + vòng tròn chỉ chuột + zoom |
| `outro` | Kết | Tóm tắt 3 ý + lời kêu gọi + khung kết cố định của series |


Khung sẵn có trong `blocks/` của Series Kit: `title` → `title-card` · `data` → `big-number` · `list` → `three-points` · `compare` → `compare` · `flow` → `process-steps` · `quote` → `key-message` · `outro` → `cta-outro`. `talking`, `screen`, `point` chưa có khung: dựng theo `frame.md`, và nếu dùng lại nhiều lần thì đề xuất thêm vào kit.

## 4. Gửi duyệt
- **Mở HyperFrames Studio** cho người dùng xem pilot (SKILL.md, "Xem trước bằng HyperFrames Studio"), ngoài file MP4.
- Pilot phải có nhạc. Người dùng chưa gửi file nhạc thì nói thẳng "bản này chưa có nhạc" và hỏi cách xử lý.
- Chụp 4–6 khung từ pilot (`<hf> snapshot --review`), lưu vào `styleframes/`. Đây là "MẪU" để các chương sau và review so sánh.
- Gửi: đường dẫn `renders/pilot.mp4`, ảnh contact sheet, và 3 câu hỏi cụ thể:
  1. Màu, chữ, bố cục đã đúng ý chưa?
  2. Tốc độ đọc và tốc độ hình đã vừa chưa (nhanh / vừa / chậm)?
  3. Có cảnh nào muốn đổi cách thể hiện không?
- Người dùng góp ý thì sửa pilot (tối đa 2 vòng), rồi mới sang bước 6. Góp ý về nhịp hoặc màu thì áp dụng cho cả video, ghi vào `PROGRESS.md`.

## Tự kiểm trước khi gửi
- [ ] Pilot đã qua cổng QC (0 lỗi)
- [ ] Mỗi khung có **một điểm nhìn chính**, đọc hiểu trong 2 giây; đạt phép thử poster
- [ ] Chữ ≥ 48 px ở nội dung chính, nằm trong vùng an toàn
- [ ] Màu và font đúng phong cách, mã font đã chốt trong `brief.md`; chữ đủ dấu, không tràn. Xanh/vàng dùng tiết chế
- [ ] Đặt cạnh style frame của tập trước (nếu có) thì nhìn ra ngay là cùng series (phép thử "MẪU vs CỦA BẠN", quality-standards mục D)
