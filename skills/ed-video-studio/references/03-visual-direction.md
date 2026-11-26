# Bước 3: Khung hình chủ đạo (visual direction)

Mục tiêu: trước khi làm chi tiết, người dùng **nhìn thấy** video sẽ trông thế nào qua 4–6 khung hình mẫu, và hiểu cách các cảnh chuyển động. Đây là "bản thiết kế" cho cả 5 phút.

## Đầu vào
`script.md` đã duyệt, Series Kit (`frame.md`, `series-kit.md`), Style Bible.

## Việc cần làm

### 1. Chia "loại cảnh" từ kịch bản
Mỗi đoạn trong kịch bản được gán một loại cảnh **có sẵn trong Series Kit** (mục *Scene types*). Loại cảnh mặc định của TH:

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

Có loại cảnh nào chưa có trong kit thì đề xuất thêm, và **ghi rõ đây là loại mới**.

### 2. Vẽ style frames
- Dựng 4–6 khung hình đại diện **bằng chính HTML/CSS sẽ dùng để render**, không vẽ minh họa riêng. Nên chọn: `title`, `talking` hoặc `point`, `list` hoặc `flow`, `data`, `outro`.
- Chụp ảnh tĩnh ở đúng kích thước xuất (1920×1080 hoặc 1080×1920) bằng `npx hyperframes snapshot` → lưu `styleframes/01_title.png`…
- Dùng nội dung thật trong kịch bản, không dùng chữ giả (lorem ipsum).

### 3. Viết `visual-direction.md`
```
## Bảng cảnh theo chương
| Chương | Thời lượng | Loại cảnh chính | Ghi chú hình |
## Ngôn ngữ chuyển động
- Vào cảnh: ...   - Chuyển chương: ...   - Nhấn số liệu: ...   - Ra cảnh: ...
## Nhịp
- Đổi cảnh trung bình mỗi X giây (theo Style Bible), chương nhanh/chậm ở đâu
## Âm thanh
- Nhạc chủ đề của series, chỗ nhạc lên/xuống, SFX dùng ở đâu
## Khác với các tập trước (nếu có) và lý do
```

## Tự kiểm trước khi gửi duyệt
- [ ] Mỗi style frame có **một điểm nhìn chính**, đọc hiểu trong 2 giây
- [ ] Chữ ≥ 48 px (16:9) ở nội dung chính, và nằm trong vùng an toàn 5%
- [ ] Màu và font đúng `frame.md`. Xanh/vàng dùng tiết chế, không quá 3 màu nhấn
- [ ] Đặt cạnh style frame của tập trước (hoặc khung tương ứng trong video mẫu) thì nhìn ra ngay là cùng một series. Dùng phép thử "MẪU vs CỦA BẠN" (quality-standards mục D)
- [ ] Mỗi khung đạt phép thử poster, có một điểm nhìn, chữ ≤ 5 từ mỗi mục

Gửi các ảnh PNG kèm bảng cảnh tóm tắt. Hỏi người dùng muốn giữ nguyên, hay chỉnh màu, bố cục, mức độ chuyển động.
