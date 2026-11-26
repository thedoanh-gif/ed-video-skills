---
name: ed-video-illustrate
description: Thiết kế bộ hình minh họa và chuyển động cho từng ý của kịch bản video TH, sau khi có giọng đọc và trước khi dựng. Mỗi ý được minh họa bằng một CẢNH cụ thể (nhân vật đang nói chuyện, bong bóng thoại có lời thật, cửa sổ chat, bảng so sánh, đồng hồ đếm, vòng khoanh, dấu gạch, con trỏ...), không phải icon đứng cạnh một khối chữ. Dùng khối th-canvas của Series Kit.
---

# ED_Video Kit: Illustrate (minh họa trước, chuyển động sau)

**Vấn đề skill này giải quyết.** Video chỉ có "khối chữ chạy vào + icon bên cạnh" là *thay đổi hình thức, không thay đổi bản chất*: người học chán sau 30 giây. Video mẫu (M1 "Càng làm nhiều, video của bạn càng chuyên nghiệp", M2, M3 trong `01_library` hoặc `...\06_ED\1. Video mẫu\`) làm ngược lại: mỗi ý được **diễn lại bằng một cảnh mô phỏng** (đồng hồ chạy khi nói "mười giây bằng một buổi chiều", năm thẻ vào lần lượt khi nói "stagger", năm khung lệch tông bị gạch khi nói "năm người lạ", ô nhập gõ chữ, con trỏ bấm nút Chạy, thanh tiến độ 118/200).

**Vị trí trong quy trình:** sau bước 3 (giọng đọc + mốc từ) và **thay cho bước 4 shot list kiểu "chọn khung + điền chữ"**. Đầu ra là spec cảnh để dựng ở bước 6.

## Đọc trước
- `references/scene-vocabulary.md`: danh mục phần tử, mẫu bố cục, mẫu "ý → cảnh" cho kỹ năng mềm.
- `references/dsl.md`: cách mô tả cảnh (JSON/Python) cho khối `th-canvas` và cách neo giờ vào theo từng từ trong lời đọc.
- Bắt buộc **xem lại video mẫu** (trích `fps=1/2,tile=4x5`) trước khi thiết kế, và xem lại khi review.

## Nguyên tắc ưu tiên (người dùng đã chốt)
- **Nội dung hiện ra là chính, nhân vật là phụ.** Làm cảnh bằng box chữ, khung chat, bong bóng, thẻ so sánh, số đếm, thanh, dấu khoanh/gạch, con trỏ. Nhân vật chỉ làm điểm nhấn nhỏ khi thật sự cần; không đầu tư tạo bộ nhân vật riêng (tốn thời gian, ít giá trị).
- **Không vẽ bộ phận cơ thể bằng code** (tai, mắt...): trông xấu. Dùng biểu tượng sạch (tai nghe, mục tiêu, micro) hoặc chữ.
- Nếu cần nhân vật, dùng ảnh minh họa có sẵn do người dùng cung cấp (cắt theo tư thế, đổi tư thế theo lời, kind `pose`), không dùng nhân vật vẽ bằng code.

## Hai cổng bắt buộc (đọc `references/brief-and-motion-templates.md`)
- **Cổng A, Brief minh họa cho TỪNG nhịp ý**: ẩn dụ hình, nhân vật + tư thế + biểu cảm, đạo cụ và nghĩa của chúng, chữ nguyên văn. Hình phải được đầu tư riêng cho nội dung từng phần nhưng cùng một bộ phong cách; ưu tiên bộ minh họa có sẵn/hình do người dùng cung cấp, vẽ bằng code chỉ cho đạo cụ đơn giản.
- **Cổng B, Motion script chi tiết cho từng nhịp**: bảng mốc giờ theo từ · đối tượng · chuyển động · thời lượng · easing · trạng thái cuối · lý do; đủ 4 lớp (vào, hành động theo lời, nhấn mạnh, nền sống). Một dòng "hiện ra" không phải là motion script.
Chưa qua hai cổng thì không viết spec cảnh. Gửi duyệt một **bản thử 30 giây** trước khi dựng cả video.

## Quy trình 5 bước
1. **Chẻ kịch bản thành "nhịp ý"**: mỗi câu/cụm có một ý riêng. Với từng nhịp ghi 3 dòng: *Ý là gì* · *Cảnh nào kể ý đó* · *Từ khóa trong lời đọc làm mốc vào*, rồi làm Cổng A và Cổng B.
2. **Chọn "cảnh kể chuyện" cho từng nhịp** theo bảng ý → cảnh (mục 2 của `scene-vocabulary.md`). Luật cứng:
   - Mỗi nhịp phải trả lời được: *tắt tiếng đi, người xem có đoán ra ý không?*
   - **Hiện nội dung thật**: nói về câu hỏi thì cảnh có đúng câu hỏi đó trong bong bóng/khung chat; nói về hai người thì có hai nhân vật với lời thoại; nói về con số thì có số đếm lên. Không dùng icon để "tượng trưng".
   - **Không lặp khuôn**: không quá 2 cảnh liên tiếp cùng bố cục (chữ trái / hình phải là bố cục bị cấm làm mặc định). Xoay giữa: hai nhân vật + bong bóng · chia đôi ✕/✓ · cửa sổ giao diện · lưới thẻ · số lớn + đồng hồ · sơ đồ vòng · ảnh điện thoại · bảng so sánh.
   - **Có hành động**: mỗi cảnh có ít nhất một thứ đang đổi trạng thái theo lời (laptop gập lại, kim đồng hồ quay, gõ chữ, thanh đầy lên, bị gạch, được khoanh, dấu ✓ vẽ ra, con trỏ bấm).
   - **Nhấn mạnh có chủ đích**: mỗi cảnh có một khoảnh khắc "chốt" (khoanh/gạch/stamp/số nhảy) ngay khi từ khóa được nói.
3. **Vẽ bộ hình trước** (không kèm chuyển động): liệt kê các "đạo cụ" cần cho cả video (nhân vật, bong bóng, cửa sổ, thẻ, icon, UI) và kiểm tra khối `th-canvas` có đủ không. Thiếu thì bổ sung vào khối rồi mới viết cảnh (ghi vào `scene-vocabulary.md` để dùng lại cho tập sau).
4. **Viết spec cảnh** (`references/dsl.md`): tọa độ trên khung 1920×1080, giờ vào neo vào từ khóa (`A("laptop")`), tối thiểu 6–10 phần tử mỗi cảnh dài trên 8 giây, và **không cảnh nào đứng yên quá 3 giây** (có phần tử mới, đổi trạng thái hoặc chuyển động nhịp thở).
5. **Tự kiểm với video mẫu** trước khi gửi: lấy 20 khung đều của cảnh dài nhất, đặt cạnh khung mẫu; trả lời 4 câu: có *hiện nội dung thật* không? có *hành động* không? có *đổi khuôn* không? có *nhấn mạnh* theo từ khóa không? Câu nào "không" thì sửa tiếp.

## Nhân vật & màu
- Bộ nhân vật mặc định của khối `th-canvas`: 6 người (`a`..`f`) khác áo/tóc, có tay (`pose`: rest/up/chin/hold/point), mặt (`smile/sad/flat/o/think`), mắt chớp, miệng mấp máy đúng khoảng đang nói (`talk`), gật đầu (`nod`). Một series dùng **cùng nhóm nhân vật** để người xem nhận ra.
- Màu chỉ lấy từ palette TH (xanh navy/xanh dương/vàng đồng/mint/hồng blush). Mỗi **phần** của video có một màu nhấn riêng (như mỗi chương của M1 có tông riêng): ví dụ phần 1 vàng, phần 2 xanh trời, phần 3 mint, phần 4 hồng. Thẻ giấy: viền ink 3px, bóng 6px, bo 14.
- Chữ trên cảnh ≥ 28px (tốt hơn ≥ 36px); số/từ khóa ≥ 60px.

## Gửi duyệt
Không bắt người dùng duyệt từng cảnh. Gửi **1 ảnh storyboard** (mỗi nhịp ý một khung chụp ở thời điểm đầy đủ nhất) cùng danh sách 3–5 cảnh "đinh" của video và hỏi một câu: "Phong cách minh họa này đã hấp dẫn và đúng ý chưa?".

## Lỗi hay gặp (đã xảy ra, tập đầu của series Kỹ năng giao tiếp)
- Giữ nguyên khuôn chữ trái + icon phải, chỉ thêm animation → người dùng nhận xét ngay là "chỉ đổi hình thức".
- Dùng nth lớn (`A("Câu", 2, ...)`) làm mốc: khi từ lặp lại, mốc nhảy sang đoạn sau. Dùng `after` đủ gần và `nth=1`; build phải in cảnh báo mốc trễ.
- Cảnh liệt kê 4 ý đứng yên 10 giây sau khi ý cuối hiện ra: thêm hành động hoặc tách cảnh.
- Tiêu đề chương dài bị icon lớn đè: giới hạn bề rộng chữ, đặt icon xa lề phải.
