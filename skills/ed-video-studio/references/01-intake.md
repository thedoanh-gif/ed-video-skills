# Bước 1: Input & trao đổi ngắn

Mục tiêu: trong **một lượt hỏi** (tối đa hai nếu là series mới), chốt đủ thông tin để viết kịch bản. Kết quả là file `brief.md` (mẫu `assets/templates/brief.md`) và `PROGRESS.md` (mẫu `assets/templates/progress.md`). Brief **không cần duyệt riêng**: 5 dòng chính của brief sẽ nằm ở đầu kịch bản và được duyệt cùng kịch bản (chế độ Kỹ thì duyệt riêng).

## 1. Đọc trước, hỏi sau
Đọc hết những gì người dùng đã đưa: tài liệu nội dung (chính sách, slide, Word, PDF), ảnh, file ghi âm, video. Câu nào trả lời được từ tài liệu thì **không hỏi lại**. Gặp file âm thanh hoặc video có lời thì chạy `<hf> transcribe` ngay để biết bên trong nói gì (xem `voice-to-srt.md`).

## 2. Bộ câu hỏi (chỉ hỏi phần còn thiếu, theo dạng chọn đáp án)

**Nguyên tắc: chọn Series Kit là xong phần kỹ thuật.** Series đã có kit thì kit đã chốt hình, giọng, màu, nhạc, logo: chỉ hỏi câu 1 và Lượt 2. CBNV không cần hiểu các lựa chọn kỹ thuật bên dưới.

**Chưa có kit đã chốt thì phải hỏi phong cách, giọng, màu, nhạc trước khi viết brief và kịch bản.** Yêu cầu ngắn, hay dữ liệu giả lập, cũng không phải lý do để tự quyết.

**Lượt 1: định dạng & phong cách** (chỉ hỏi khi là video lẻ hoặc series mới)
1. **Series**: thuộc series nào (liệt kê các thư mục trong `03_series-kits/`), hay là video lẻ / series mới?
2. **Phong cách hình**: gửi ảnh `assets/styles/preview/chon-phong-cach.jpg`, người dùng trả lời **một mã**: TH BlueGold (mặc định) / P1 Năng lượng / P2 Tươi mát / P3 Nắng sớm / P4 Kẹo ngọt / P5 Dark Studio / P6 Nhiều màu. Cũng nhận: theo video mẫu, kit khác trong `03_series-kits/`, hoặc mã màu riêng (`assets/palettes.md`). Muốn xem kỹ một phong cách thì gửi `preview/bang-<phong-cach>.jpg`.
2b. **Font chữ**: gửi ảnh `assets/styles/preview/chon-font.jpg`, người dùng trả lời **một mã** F1–F8. Đề xuất theo `fonts_hint` của phong cách (`assets/styles/styles.json`). Video phát ra ngoài công ty thì không đề xuất F1.
2c. **Hình chính**
   A. Người thật diễn hoặc nói trước camera (có file quay) → face-cam + minh họa
   B. Quay màn hình hoặc phần mềm → screen + chú thích động
   C. Chỉ motion graphic, không có người
   D. Từ poster hoặc ảnh có sẵn
3. **Giọng đọc** (chi tiết: `audio-sources.md` mục 1)
   A. Giọng có sẵn trong file quay
   B. File ghi âm riêng
   C. ElevenLabs (agent soạn lời + thông số, người dùng tạo giọng rồi gửi file)
   D. **Giọng AI do agent tự tạo** (edge-tts giọng nữ HoaiMy / nam NamMinh, cần internet; hoặc Piper offline)
   E. Không lời, chỉ nhạc và chữ
4. **Màu sắc**: đi theo phong cách ở câu 2, không hỏi riêng. Chỉ hỏi khi người dùng muốn mã màu của riêng họ.
5. **Nhạc nền & SFX** (`audio-sources.md` mục 2–3): A. AI tạo bằng code (mặc định, không lo bản quyền) / B. Tự tải từ nguồn miễn phí (Pixabay, YouTube Audio Library…) / C. Không nhạc. Chọn B thì nói rõ cần gửi file **trước pilot**; chưa có file ở pilot thì nhắc lại và đề xuất A. Nhạc luôn giữ một mức suốt video.
6. **Logo** (chỉ hỏi một lần cho mỗi series): có file logo không? Cần PNG nền trong suốt hoặc SVG, lưu vào `03_series-kits/<series>/brand/logo.png`. Không có thì video không có logo, không tự lấy logo trên mạng.
7. **Nhân vật dẫn chuyện**: mặc định **không dùng**. Chỉ dùng khi người dùng **tự đưa** nhân vật (PNG/SVG nền trong suốt, nên có 3–4 tư thế). Agent không tự vẽ hay lấy nhân vật trên mạng.

**Lượt 2: nội dung và phát hành** (bỏ qua câu nào đã rõ)
8. **Mục tiêu**: xem xong người xem phải *biết* gì / *làm* gì? (1 câu)
9. **Người xem**: toàn bộ CBNV, quản lý, nhân viên mới, khối sản xuất…
10. **Thời lượng**: mặc định ~5 phút. Video mạnh nhất khi chỉ có 1 thông điệp chính và tối đa 3–5 ý.
11. **Kênh phát**: LMS (16:9, < 600 MB) / Teams, email / Zalo (9:16 hoặc 1:1) / màn hình sảnh
12. **Nguồn hình**: ảnh người dùng gửi / icon và minh họa tự vẽ bằng SVG / logo. **Không lấy ảnh trên mạng** nếu không rõ bản quyền.

Gợi ý: gom câu 2–7 thành **một tin nhắn** dạng chọn đáp án, kèm hai ảnh chọn và câu 8–9 nếu tài liệu chưa trả lời. Người dùng chỉ cần trả lời "P3, F4, C, D, A, có logo, không". Mã đã có trong yêu cầu (người dùng chép từ trang hướng dẫn) thì không hỏi lại. Series đã có kit thì chỉ hỏi những mục kit chưa chốt.

**Video báo cáo (đào tạo, kết quả năm, dự án)**: đừng chỉ kể con số. Hỏi hoặc đề xuất đủ các mục: chương trình trọng điểm (ví dụ tư duy, AI) · tính ứng dụng vào công việc · phản hồi của người học · điểm hài lòng · điểm cần cải thiện · kế hoạch và việc cần làm. Người dùng muốn **sửa số sau** hoặc dữ liệu còn giả lập thì làm theo kiểu dữ liệu tách riêng (`06-build.md` mục 4b), và gắn nhãn "NỘI DUNG GIẢ LẬP" trên hình.

## 3. Kiểm tra độ khả thi trước khi chốt brief
- **Khối lượng**: theo tốc độ đọc trong Style Bible (chuẩn 170–190 từ/phút), 5 phút ≈ 850–950 từ lời đọc. Tài liệu dài hơn nhiều thì đề xuất cắt hoặc chia tập.
- **Chất lượng nguồn**: video quay mờ hoặc tối, âm thanh ồn, ảnh độ phân giải thấp → báo ngay, đề xuất cách xử lý.
- **Giọng**: ElevenLabs thì kiểm tra Series Kit đã có voice ID chưa. Giọng AI thì kiểm tra máy có `edge-tts` và có mạng; không có thì đề xuất Piper hoặc ElevenLabs. Chạy thử 1 câu cho người dùng nghe trước khi tạo cả video.
- **Series mới**: lựa chọn ở câu 2–6 sẽ thành Series Kit mới (chép `th-default` rồi áp phong cách, font, voice profile, nhạc). Xem `series-kit-spec.md`.
- **Phong cách và khổ**: P1–P4, P6 mới kiểm khổ 16:9. Chọn khổ dọc thì nói rõ phải dựng và kiểm lại bố cục.
- **Thông tin nhạy cảm** (lương, dữ liệu cá nhân, số liệu nội bộ chưa công bố): hỏi xác nhận được phép đưa vào video.

## 4. Ghi brief, chuyển thẳng sang kịch bản
Ghi `brief.md` và tạo `PROGRESS.md`. Không dừng chờ duyệt: chuyển sang bước 2 luôn. 5 dòng tóm tắt brief (thông điệp, người xem, thời lượng, giọng, kênh) và các giả định tự quyết sẽ được đặt ở đầu bản kịch bản gửi duyệt.

Chế độ Kỹ: gửi bản tóm tắt brief tối đa 10 dòng và hỏi "Chốt brief này để viết kịch bản nhé?" trước khi sang bước 2.
