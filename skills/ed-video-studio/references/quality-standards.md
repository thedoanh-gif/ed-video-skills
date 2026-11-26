# Chuẩn chất lượng: bóc từ video mẫu M1 "Càng Làm Nhiều, Video Của Bạn Càng Chuyên Nghiệp"

M1 là một bài giảng về motion "nghiệp dư vs đẳng cấp" khi làm cùng AI. Dưới đây là toàn bộ chuẩn rút ra từ video, diễn đạt lại và chuyển thành luật cho skill. File này được dùng ở bước 4–7 và là căn cứ của ed-video-review.

---

## A. Gốc rễ: "an toàn = nhạt"
Giao việc chung chung ("làm cho tôi một intro") thì AI trả về lựa chọn an toàn nhất: căn giữa, mờ dần, màu xám. Kết quả là một cảnh "quốc dân", ai làm cũng giống nhau. **Chất lượng nằm ở nguyên tắc và độ cụ thể của yêu cầu, không nằm ở công cụ.**
→ Luật: mọi cảnh phải có spec cụ thể (mục C) trước khi dựng. Không dựng cảnh từ một câu mô tả mơ hồ.

## B. Năm nguyên tắc motion

### 1. Easing: gia tốc chuyển động
- Chuyển động tốc độ đều trông như game bị lag. Chuyển động có gia tốc (như quả bóng lăn) trông như thật.
- Cùng quãng đường, cùng thời gian: bản easing luôn cho cảm giác đắt hơn bản tuyến tính.
- Khi giao việc phải nói rõ kiểu: "trượt vào, chậm dần ở cuối" = `ease-out` / `power2.out`.

### 2. Timing & stagger: lần lượt, không ùa ra
- **Cùng một lúc ✗ → lần lượt, cách nhau ~0,1 giây ✓.**
- **Nhịp hình = nhịp lời.** Mỗi phần tử vào đúng lúc giọng nói tới nó. Sớm ✗, muộn ✗.
- Quy trình bắt buộc: **Thu giọng → lấy mốc từng từ (file .srt hoặc words.json) → AI dựng hình theo mốc**. Không dựng hình trước rồi mới ghép giọng.

### 3. Một điểm nhìn: mỗi khung hình chỉ một trọng tâm
- Trọng tâm là thứ **to nhất, sáng nhất, ở vị trí đắc địa nhất**. Phần còn lại lùi xuống (mờ, nhỏ, trung tính).
- Một màn hình nhồi "DOANH THU + HOT + WOW + mũi tên + biểu đồ + sao" là nghiệp dư. Chỉ cần "+32%" là đủ.
- **Chữ trên màn hình ≤ 5 từ.** Hình tự nói được thì bỏ chữ.

### 4. Design system: một hệ thống, nhất quán
- "Năm người lạ" ✗: mỗi cảnh một màu, một font, một kiểu nút. "Một bộ quy tắc" ✓: các cảnh như anh em một nhà.
- Bộ quy tắc gồm: **1 bảng màu (nền + nhấn), 1–2 font, 1 kiểu bo góc, 1 kiểu đổ bóng**, lề cố định (ví dụ 120px), lưới 12 cột.
- Viết thành một file (DESIGN.md hoặc `frame.md`) để AI tuân thủ. Mẫu cảnh của bạn phải **bắt được** mẫu tham chiếu.

### 5. Chuyển cảnh có lý do, không phải pháo hoa
- Mỗi chuyển cảnh nối logic hai cảnh. Ba kiểu mẫu:
  1. **Con số phóng lớn**: thẻ số liệu trong cảnh trước phóng to thành cảnh sau
  2. **Icon mở bung**: một icon hoặc khung điện thoại phóng to tới khi màn hình của nó thành bối cảnh mới
  3. **Góc máy lướt sang**: camera trượt ngang sang vùng nội dung kế bên
- Kết quả cần đạt: **câu chuyện trôi chảy**. Mô tả chuyển cảnh bằng **logic thị giác** ("khung điện thoại phóng to dần cho tới khi màn hình của nó trở thành bối cảnh"), không chỉ ghi tên hiệu ứng.

## C. Giao việc: câu lệnh tệ vs tốt
| ✗ Cách 1: chung chung | ✓ Cách 2: chi tiết |
|---|---|
| "Làm cảnh giới thiệu ba tính năng của app, đẹp và hiện đại." | "Cảnh dài **6 giây**, **nền màu kem**, đặt **một khung iPhone ở chính giữa**. Ba tính năng hiện **lần lượt, khớp lời đọc ở các mốc 1,2 – 2,8 – 4,5 giây**. Mỗi tính năng là một thẻ **trượt từ dưới lên, ease-out**. Tính năng đang được nhắc thì **sáng rõ, hai thẻ kia mờ đi**." |
| → gradient tím, 3 thẻ giống nhau, kiểu "quốc dân" | → có chủ đích, khớp lời, có một điểm nhìn |

**Spec cảnh tối thiểu (7 mục)** — mọi dòng trong shot list phải đủ:
1. **Thời lượng** (giây) · 2. **Nền** · 3. **Bố cục / vật thể chính và vị trí** · 4. **Thứ tự xuất hiện + mốc thời gian lấy từ lời** · 5. **Kiểu chuyển động + easing** · 6. **Trọng tâm** (cái gì sáng, cái gì lùi) · 7. **Cấm** (điều không được làm trong cảnh này)

## D. Xem lại: "một bí kíp rất đáng tiền"
1. **Dừng hình ở bất kỳ giây nào → có đủ đẹp để in thành poster không?** Đây là phép thử chính.
2. Checklist từng khung: **Chữ bị cắt? · Đè lên nhau? · Hàng thẳng chưa?**
3. **Đặt cạnh mẫu**: frame "MẪU" (style frame đã duyệt hoặc video tham chiếu) và "CỦA BẠN" đặt cạnh nhau. Khoanh vùng các điểm lệch.
4. **Góp ý phải đo được.** ✗ "Nhìn chưa đẹp lắm" → ✓ "Tiêu đề to thêm 20%, nhích lên trên một chút", "Nền ấm hơn · chữ dày hơn · lề rộng hơn".
5. Sửa từng cảnh: dựng cảnh một, xem, sửa, rồi mới sang cảnh hai.

## E. Năm lỗi AI hay mắc (dặn trước để phòng)
| # | Lỗi | Cách phòng |
|---|---|---|
| 1 | **Lắc lư, nhấp nháy** không ngừng | Chuyển động phải **dừng đúng lúc**. Sau khi vào cảnh thì đứng yên, chỉ "thở" rất nhẹ (≤ ±2px) |
| 2 | **Zoom chậm rì cả cảnh** cho có chuyển động | Không dùng zoom kéo dài cả cảnh làm chuyển động chính. Mỗi chuyển động phải có mục đích |
| 3 | **Chữ karaoke**: bê nguyên văn lời thoại lên màn hình | Chữ chỉ giữ từ khóa ≤ 5 từ. Phụ đề là lớp riêng, chỉ bật khi kênh cần |
| 4 | **Icon chung chung** (bánh răng, quả địa cầu, bóng đèn) | Dùng hình cụ thể của nội dung: giao diện thật được vẽ lại, đồ vật cụ thể, số liệu thật |
| 5 | **Quên màn hình điện thoại**: chữ nhỏ, xem trên điện thoại không đọc được | Thu nhỏ khung hình về cỡ điện thoại (~360px ngang) để kiểm tra. Chữ chính vẫn phải đọc được |

## F. Quy trình 6 bước của M1 (đối chiếu với ed-video-studio)
| M1 | ed-video-studio |
|---|---|
| 1. Kịch bản | Bước 2 |
| 2. Giọng đọc → mốc từng từ | **Bước 3: tạo giọng ngay sau khi duyệt kịch bản** |
| 3. Phân cảnh (ý chính + hình) | Bước 4 (shot list) |
| 4. Design system (DESIGN.md) | Series Kit `frame.md` + `blocks/` + style frames chụp từ pilot (bước 5) |
| 5. Dựng từng cảnh (cảnh một, rồi cảnh hai) | Bước 5, dựng và kiểm từng chương |
| 6. Xem & sửa (góp ý, tinh chỉnh) → Render | Bước 6–7 |

## G. Skill học dần và vai trò
- **Skill = cẩm nang nghề cho AI** (SKILL.md hướng dẫn + examples/ ví dụ mẫu + scripts/ công cụ). Mỗi skill là một chuyên gia.
- Skill riêng của bạn gồm **giọng đọc, thumbnail, phong cách**, cộng các ghi chú góp ý tích lũy. Vòng lặp: **Video 1 → AI tổng kết góp ý → ghi vào skill → Video 2**. Sau mỗi tập AI "hiểu ý sếp" hơn. → Đây chính là mục *Nhật ký series* trong Series Kit (bước 8).
- **AI = người thợ lành nghề nhất bạn từng có. Bạn = đạo diễn ngồi trên ghế đạo diễn.** Con mắt thẩm mỹ (cần gì? thừa gì? rườm rà?) là phần của người dùng. → Đây là lý do có các điểm **[DUYỆT]**.
