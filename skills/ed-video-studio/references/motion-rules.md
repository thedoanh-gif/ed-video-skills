# Luật motion

Tổng hợp từ kho mẫu (Style Bible mục 3, 6) và các skill motion graphic phổ biến trên GitHub. Thông số cụ thể (thời lượng, easing) lấy từ `frame.md` của Series Kit. File này nói **nguyên tắc**.

> Bản đầy đủ có ví dụ: `quality-standards.md` (mục B, E). File này là bản tóm tắt để tra nhanh khi dựng.

## 5 nguyên tắc nền
1. **Easing**: không có chuyển động tuyến tính. Vào cảnh dùng ease-out, di chuyển dùng ease-in-out. Nảy (back, elastic) chỉ dùng cho điểm nhấn như số liệu hay stamp, tối đa 1–2 lần mỗi chương.
2. **Nhịp & stagger**: các phần tử cùng nhóm vào lệch nhau 0.08–0.15s. Ra cảnh nhanh hơn vào cảnh (khoảng 60% thời lượng). Mọi thời gian tính bằng giây trên timeline, không gõ số frame bằng tay.
3. **Một điểm nhìn**: mỗi thời điểm chỉ một thứ mới chuyển động mạnh, những thứ khác đứng yên hoặc "thở" nhẹ.
4. **Design system**: chỉ dùng token trong `frame.md`. Một kiểu bo góc, một kiểu bóng, một bộ màu cho cả video.
5. **Chuyển cảnh có nghĩa**: chuyển chương dùng block `chapter-card` của kit. Đi sâu vào chi tiết thì phóng camera vào đúng phần tử đó (chi tiết nằm sẵn trong khung tổng), không cắt sang một màn hình xa lạ.

## Mỗi lần vào cảnh animate 2–3 thuộc tính
Ví dụ: opacity 0→1 + y 24→0 + scale 0.96→1. Chỉ đổi mỗi opacity thì trông rẻ, đổi 4–5 thuộc tính thì rối.

## Đồng bộ với lời
- Phần tử xuất hiện **đúng lúc hoặc trễ ≤ 0.2s** so với từ khóa trong lời, không sớm hơn.
- Số liệu bắt đầu đếm khi giọng bắt đầu đọc con số.
- Trong một câu dài, phần tử chính vào ở từ khóa, phần tử phụ vào ở cuối câu.

## Khung đứng yên
- Khung có người nói: được đứng yên lâu, nhưng thẻ chú thích phải thay đổi ít nhất 15 giây một lần.
- Khung chỉ có đồ họa: tối đa 10 giây không có sự kiện mới. Trong lúc chờ thì có chuyển động "thở" (±2px hoặc ±1% scale, chu kỳ 3–5s, theo hàm sin của thời gian timeline).

## Lớp hình (từ dưới lên)
1. Nền (giấy, panel) + texture rất nhẹ
2. Asset (ảnh, video, face-cam)
3. Đồ họa (thẻ, chữ, icon, sơ đồ)
4. Hoàn thiện: vignette, grain. **Làm bằng `<hf> media-treatment`, không dùng CSS filter.**

## Ảnh tĩnh
Mọi ảnh tĩnh nằm trên màn hình quá 3 giây phải có chuyển động chậm (Ken Burns: scale 1→1.06, hoặc trượt 2–3% suốt thời gian hiện).

## Giao diện giả lập
Cửa sổ chat, code, app, trình duyệt: vẽ bằng HTML theo token của kit. Chữ trong cửa sổ hiện kiểu gõ phím (0.02–0.04s mỗi ký tự) hoặc theo từng dòng. Con trỏ chuột di theo đường cong ease-in-out, lúc click có vòng tròn lan ra.

## Chống 5 lỗi AI hay mắc
Không lắc lư hoặc nhấp nháy liên tục (dừng đúng lúc) · không zoom chậm cả cảnh · không "chữ karaoke" · không icon chung chung (bánh răng, địa cầu, bóng đèn) · kiểm tra đọc được ở cỡ điện thoại.

## Kiểm tra nhanh trước khi render
- [ ] Không có tween nào dùng `ease: "none"` cho phần tử vào hoặc ra cảnh
- [ ] Không có 2 nhóm phần tử chuyển động mạnh cùng lúc
- [ ] Mọi phần tử có thời gian ra cảnh (hoặc cố ý giữ đến hết cảnh)
- [ ] Dừng hình ở 3 thời điểm bất kỳ: khung nào cũng "đủ đẹp để in poster"
- [ ] Không có chữ bị cắt, không đè nhau, các hàng thẳng
- [ ] Qua cổng QC: `<hf> check hf --json --at-transitions --safe-zone=standard` có 0 lỗi (06-build.md mục 7)
