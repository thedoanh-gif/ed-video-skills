# Rubric review (100 điểm)

Mỗi tiêu chí chấm **Đạt / Một phần / Không đạt** (= 100% / 50% / 0% số điểm), kèm mốc thời gian làm bằng chứng.

## 1. Chuẩn chất lượng: 40 điểm
| # | Tiêu chí | Điểm | Cách kiểm |
|---|---|---|---|
| 1.1 | **Phép thử poster**: dừng hình ở bất kỳ đâu cũng đủ đẹp để in | 6 | Xem contact sheet 5 giây/khung, tìm khung xấu nhất |
| 1.2 | **Một điểm nhìn**: mỗi khung một trọng tâm (to, sáng, đắc địa nhất) | 5 | Khung có ≥ 2 thứ cùng "hét" là lỗi |
| 1.3 | **Chữ ≤ 5 từ/mục**, tiêu đề ≤ 8 từ, **không có chữ karaoke** | 5 | Đếm chữ ở các khung nhiều chữ nhất |
| 1.4 | **Easing**: không có chuyển động đều tuyến tính, chuyển động dừng đúng lúc | 4 | Xem đoạn vào cảnh ở 3 chương |
| 1.5 | **Stagger + nhịp hình = nhịp lời**: lần lượt ~0,1s, khớp từ khóa (không sớm, trễ ≤ 0,2s) | 6 | Đối chiếu 5 từ khóa trong shot list với video |
| 1.6 | **Design system**: không có "năm người lạ"; màu, font, bo góc, bóng nhất quán | 4 | So sánh 6 khung ở 6 chương |
| 1.7 | **Chuyển cảnh có lý do** (logic thị giác), không phải pháo hoa | 3 | Xem tất cả chỗ chuyển chương |
| 1.8 | **Sạch lỗi bố cục**: không có chữ bị cắt, không đè nhau, hàng thẳng, nằm trong vùng an toàn | 4 | Xem từng khung trong contact sheet |
| 1.9 | **Không mắc 5 lỗi AI**: lắc lư nhấp nháy · zoom chậm rì · karaoke · icon chung chung · quên màn hình điện thoại | 3 | Xem khung cỡ điện thoại (`phone_*.jpg`) |

## 2. Độ khớp Series Kit: 20 điểm
| # | Tiêu chí | Điểm |
|---|---|---|
| 2.1 | Intro, chapter-card, outro, footer đúng block của kit | 5 |
| 2.2 | Màu, bo góc, bóng đúng phong cách đã chốt; font đúng mã đã chốt trong `brief.md` hoặc kit (mặc định DINRoundOT), đủ dấu tiếng Việt | 5 |
| 2.3 | Chỉ dùng motion language của kit, loại cảnh có trong kit | 4 |
| 2.4 | Giọng đúng voice profile (voice ID/thông số hoặc cùng người đọc + cùng bộ lọc), nhạc và SFX đúng bộ | 4 |
| 2.5 | Đặt cạnh style frames hoặc tập trước: nhìn ra ngay cùng series (khung MẪU \| CỦA BẠN) | 2 |

## 3. Kỹ thuật: 15 điểm
| # | Tiêu chí | Điểm |
|---|---|---|
| 3.1 | `qc_probe.py` không có FAIL (dung lượng, codec, có tiếng) | 5 |
| 3.2 | Độ lớn ~-16 LUFS, nhạc giữ một mức (không to nhỏ theo giọng) và không lấn giọng, không hụt tiếng ở chỗ nối chương | 4 |
| 3.3 | Không có khung đen hoặc giật ở chỗ nối chương, không có frame lỗi | 3 |
| 3.4 | Phụ đề (nếu có) đúng chính tả, khớp thời gian, ≤ 42 ký tự/dòng | 3 |

## 4. Khán giả: 25 điểm
| # | Tiêu chí | Điểm |
|---|---|---|
| 4.1 | Hook giữ chân trong 20 giây đầu (persona bận rộn vẫn xem tiếp) | 6 |
| 4.2 | Hiểu được thông điệp chính sau một lần xem | 6 |
| 4.3 | Nhịp: không có đoạn chán (khung không có người nói đứng yên > 10 giây, nhịp đổi hình 8–10 lần/phút) | 5 |
| 4.4 | Nhớ được ≥ 3 ý / biết việc cần làm sau khi xem | 4 |
| 4.5 | Giọng văn đúng TH: tôn trọng, không lên lớp, không sáo rỗng | 4 |

## 5. Sức hút & chuyển động so với video mẫu: 20 điểm (cộng vào, tổng 120 quy về 100)
Lăng kính này trả lời một câu: **học viên có muốn xem tiếp không?** Đạt rubric 1–4 mà vẫn đơn điệu thì video vẫn hỏng. Bắt buộc **xem song song** khung của video mình với video mẫu trong `01_library` (hoặc `...\06_ED\1. Video mẫu\`): trích cùng một đoạn 30–40 giây mỗi video (`ffmpeg -vf fps=1/2,scale=480:-1,tile=4x5`), xem cả đoạn dày 0,3s/khung quanh một lần chữ/hình xuất hiện.
| # | Tiêu chí | Điểm | Cách kiểm |
|---|---|---|---|
| 5.1 | **Cảnh "sống"**: trong mọi cảnh luôn có thứ đang chuyển động (hình thở/đổi trạng thái, chữ vào/ra, chỉ báo chạy). Không có cảnh nào chỉ "hiện ra rồi đứng im" quá 3 giây | 5 | Lấy 3 khung cách nhau 2s trong cùng 1 cảnh dài: nếu giống hệt nhau là lỗi |
| 5.2 | **Hộp chữ/hình ra theo đúng từng ý của lời đọc** (chữ hiện đúng lúc từ khóa được nói, mỗi ý một nhịp, có nhấn mạnh: gạch chân, khoanh, gạch bỏ, dấu ✓/✕ vẽ ra) | 5 | Đối chiếu từ khóa với khung; so với mẫu M2/M3 (vòng khoanh, gạch ngang, hàng bảng hiện dần) |
| 5.3 | **Hình minh họa diễn tả ý bằng hành động**, không chỉ là tranh tĩnh (kim đồng hồ quay, bubble gõ chữ, con trỏ bấm, mũi tên chạy, đối tượng bị gạch) | 4 | Hình có kể được ý của câu nói nếu tắt tiếng không? |
| 5.4 | **Đa dạng bố cục & nhịp thay đổi**: không lặp cùng một khuôn trái chữ / phải hình quá 3 cảnh liên tiếp; có cảnh chuyển, đổi nền, phóng/zoom, bảng so sánh, mock-up giao diện | 3 | Xem contact sheet: có nhận ra "cùng 1 template" không |
| 5.5 | **Chuyển cảnh có chủ đích** (quét, đẩy, biến hình giữa 2 cảnh), không cắt cứng hay mờ trắng | 3 | Xem 5 chỗ chuyển |

**Luật cổng:** tiêu chí 5.1 hoặc 5.2 "Không đạt" = **Phải sửa**. Báo cáo phải nêu thẳng "so với mẫu, video này còn thiếu gì" bằng 2–3 câu, kèm 3 khung đặt cạnh nhau (mẫu | của mình).

## Ngưỡng kết luận
- **≥ 85 và không có "Phải sửa"** → `PHÁT ĐƯỢC`
- **70–84**, hoặc có "Phải sửa" nhưng chỉ ảnh hưởng ≤ 2 chương → `SỬA RỒI PHÁT`
- **< 70**, hoặc lỗi ở kịch bản hay cấu trúc → `CẦN LÀM LẠI PHẦN…` (chỉ rõ quay lại bước nào)

## Phân mức
- **Phải sửa**: sai thông tin, lỗi kỹ thuật, chữ bị cắt hoặc đè, sai brand, một tiêu chí khán giả bị "Không đạt"
- **Nên sửa**: lệch chuẩn chất lượng hoặc Series Kit, nhưng người xem phổ thông khó nhận ra
- **Cân nhắc**: gu thẩm mỹ, có thể giữ nguyên
