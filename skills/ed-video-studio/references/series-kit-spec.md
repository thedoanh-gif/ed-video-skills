# Đặc tả Series Kit

Series Kit là thứ giữ các tập video **giống nhau về hình, nhịp và giọng**. Mỗi series có đúng một kit nằm trong `TH-Video/03_series-kits/<series>/`.

## Cấu trúc thư mục
```
<series>/
  series-kit.md     danh tính hình, người dẫn, loại cảnh, khung cố định, motion, voice, âm thanh, nhật ký
  frame.md          design tokens (màu, font, cỡ chữ, bo góc, bóng, lưới, motion tokens)
  glossary.txt      thuật ngữ cho phụ đề và cách đọc
  fonts/            file font
  brand/            logo (PNG nền trong suốt hoặc SVG) do người dùng gửi; kit gốc không kèm logo
  audio/            theme.mp3, sfx/
  blocks/           7 khung cảnh dựng sẵn (title-card, big-number, three-points, compare,
                    process-steps, key-message, cta-outro) + intro/footer riêng của series, mascot/ (nếu có)
  styleframes/      ảnh mẫu đã duyệt, dùng để so sánh độ khớp giữa các tập
  engine/           (tùy chọn) mã dựng dùng lại của series, thay cho blocks/ (xem kit dark-studio)
```
Người dùng duyệt và ưng phần hình của một video chưa thuộc kit nào thì **đề xuất lập kit** từ video đó: tokens, ảnh mẫu, nhạc, SFX, mã dựng. Dựng thử lại từ kit để chắc ra đúng hình cũ.

## Tạo kit mới cho một series
1. Chép `th-default` (trong skill `ed-video-studio/assets/series-kits/`) sang `03_series-kits/<series>/`.
2. Chốt **mã phong cách** (TH, P1–P6) và **mã font** (F1–F8) từ `assets/styles/`; ghi vào `series-kit.md` mục 0 và lưu `theme.css` + font đã dùng vào kit. Style Bible mục 4 (A, B, C) vẫn dùng để chọn cách kể hình.
3. Chốt **người dẫn** và **voice profile** (voice ID ElevenLabs hoặc người đọc). Đây là phần khó đổi nhất về sau.
4. Xin logo một lần, lưu vào `brand/`. Chỉnh token màu trong `frame.md` (các khung trong `blocks/` tự đổi theo). Dựng intro/footer riêng nếu series cần, lưu vào `blocks/`. Lưu style frames chụp từ pilot đã duyệt vào `styleframes/`.
5. Từ tập 2 trở đi, các tập chỉ được **dùng lại** kit, không thiết kế lại.

## Những gì phải giống nhau giữa các tập
| Mục | Mức độ |
|---|---|
| Intro, chapter-card, outro, footer | Giống hệt (dùng chung file) |
| Màu, font, bo góc, bóng | Giống hệt |
| Giọng (voice ID và thông số, hoặc cùng người đọc + cùng bộ lọc) | Giống hệt |
| Nhạc chủ đề và bộ SFX | Giống hệt |
| Motion language (7 kiểu) | Chỉ dùng trong danh sách |
| Cấu trúc Hook, Hứa, Menu, Phần, Tổng kết | Giữ nguyên khung, nội dung thay đổi |
| Loại cảnh | Ưu tiên loại có sẵn. Loại mới phải được duyệt rồi mới thêm vào kit |
