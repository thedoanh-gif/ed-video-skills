# Hai tài liệu bắt buộc cho MỖI nhịp ý (làm trước khi viết spec cảnh)

Hai lỗi đã xảy ra ở tập đầu (Kỹ năng giao tiếp): (1) hình minh họa dùng chung một nhóm icon/nhân vật đơn giản cho mọi phần, không được thiết kế riêng cho nội dung từng phần; (2) mô tả chuyển động chỉ là một dòng ("hiện ra", "trượt vào"), nên cảnh dựng ra đơn điệu. Vì vậy mỗi nhịp ý phải có **A. Brief minh họa** rồi **B. Motion script**, lưu trong `illustration-brief.md` và `motion-script.md` của dự án. Không viết spec khi chưa có hai tài liệu này.

## A. Brief minh họa (một khối cho mỗi nhịp ý)

```
NHỊP: ch05-s2 · "Câu hỏi mở: bắt đầu bằng Điều gì / Như thế nào / Vì sao"
Ý CẦN HIỂU (1 câu): từ mở đầu quyết định người kia kể được bao nhiêu.
ẨN DỤ HÌNH: ba chiếc chìa khóa, mỗi chìa mở một cánh cửa to dần (không dùng dấu hỏi chung chung).
CẢNH ĐẦY ĐỦ: bố cục, vị trí từng thứ (trái/phải/trên/dưới, kích thước tương đối).
NHÂN VẬT: ai, tâm trạng, tư thế, hướng nhìn, đạo cụ cầm. Người nghe: nghiêng người, tay chống cằm.
ĐẠO CỤ / HÌNH PHỤ: liệt kê từng món, kèm nghĩa của nó (vì sao nó ở đây).
CHỮ TRÊN MÀN HÌNH: nguyên văn từng dòng (câu thoại thật, số thật, nhãn thật).
BẢNG BIỂU CẢM / TƯ THẾ cần có: danh sách (vd: nhân vật A: cười, hỏi; B: ngạc nhiên rồi mở lòng kể).
MÀU & PHONG CÁCH: màu nhấn của phần, độ dày nét, bóng đổ (giống toàn series).
KHÔNG ĐƯỢC: những thứ dễ sa vào (icon dấu hỏi trơ trọi, hai người đứng yên).
```
Quy tắc:
- Mỗi **phần** của video có "bộ hình riêng" (nhân vật phụ, đạo cụ, bối cảnh khác nhau theo chủ đề: phần cuộc họp có bàn họp, phần đồng cảm có chip cảm xúc), nhưng **chung một phong cách nét**.
- Nhân vật chính xuất hiện xuyên suốt phải **giữ nhận diện** (tóc, áo) và có **bảng tư thế** đủ cho mọi nhịp (nghe, nói, nghĩ, buồn, cười, ngạc nhiên, cầm thiết bị, chỉ tay, gật, lắc).
- Nguồn hình theo thứ tự ưu tiên: (a) bộ minh họa có sẵn cùng phong cách (Icons8 qua MCP, Lottie), (b) hình AI tạo theo một prompt phong cách cố định, (c) hình do người dùng/họa sĩ cung cấp, (d) vẽ bằng code chỉ cho đạo cụ đơn giản (khung chat, thẻ, thanh, đồng hồ).
- Kiểm tra trước khi sang bước B: đặt tất cả hình của cả video cạnh nhau trên một tờ; nếu nhìn như từ nhiều nguồn khác nhau thì làm lại.

## B. Motion script (một bảng cho mỗi nhịp ý)

Mỗi dòng là **một chuyển động**, đủ chi tiết để dựng mà không phải đoán:

| # | Mốc giờ (từ khóa + độ lệch) | Đối tượng | Chuyển động | Thời lượng | Easing | Kết thúc ở trạng thái | Vì sao (gắn với lời) |
|---|---|---|---|---|---|---|---|
| 1 | "Điều" -0.1s | Chìa khóa 1 | rơi từ trên xuống, nảy 2 lần, xoay 15° | 0.6s | bounce.out | nằm trên bàn | "Điều gì" là chìa đầu tiên |
| 2 | "gì" +0.2s | Cửa 1 | lá cửa mở 30° rồi sáng viền | 0.5s | power2.out | hé mở | câu hỏi mở ra không gian |

Quy tắc viết motion:
- Mỗi cảnh có **4 lớp chuyển động**: (1) vào cảnh (staggered, không vào cùng lúc), (2) hành động chính theo lời, (3) nhấn mạnh khi từ khóa được nói (khoanh, gạch, nảy, sáng, rung), (4) **sống động nền** (thở, chớp mắt, lắc nhẹ, hạt trôi) để không có khung nào chết.
- Mỗi đối tượng quan trọng có **ít nhất 2 trạng thái** (trước/sau): cửa đóng→mở, thanh 8%→95%, mặt buồn→cười, chữ mờ→rõ.
- Dùng **đa dạng loại chuyển động**: rơi-nảy, trượt, xoay, phóng to-thu nhỏ, vẽ nét, gõ chữ, đếm số, đổi tư thế nhân vật, camera đẩy/lia, khung bật sáng, rung, tách đôi. Không dùng một kiểu vào cho cả cảnh.
- Nhân vật: ghi riêng **diễn xuất** (tư thế và biểu cảm theo từng câu, đổi tư thế tại mốc nào, nhìn về ai, tay làm gì), không chỉ "miệng nói".
- Mọi mốc giờ neo vào **từ trong lời đọc** (nth=1 + after); kết thúc cảnh trước câu kế ≥ 0.3s.
- Chuyển cảnh: nối bằng hành động (đối tượng cuối cảnh trước trở thành đối tượng đầu cảnh sau) thay vì chỉ quét màu.

## Cổng kiểm trước khi dựng
- [ ] Mỗi nhịp có brief minh họa đủ 9 mục, không mục nào để trống.
- [ ] Bảng tư thế/biểu cảm đã có hình thật cho từng dòng.
- [ ] Tờ tổng các hình trông cùng một bộ.
- [ ] Mỗi nhịp có motion script ≥ 6 dòng (cảnh dài > 8s ≥ 10 dòng), có đủ 4 lớp.
- [ ] Tắt tiếng xem animatic: hiểu được ý không?
