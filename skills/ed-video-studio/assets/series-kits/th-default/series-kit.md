---
series: th-default
display_name: TH Paper (mặc định)
style_base: B. Paper & Mascot + C. Host + Overlay (Style Bible mục 4)
version: 1.1
---

# Series Kit: TH Paper (mặc định)

Dùng khi video chưa thuộc series nào. Muốn lập series riêng (ví dụ Coffee Monday) thì chép cả thư mục này sang `TH-Video/03_series-kits/<ten-series>/` rồi sửa. **Mọi tập trong một series phải dùng chung một kit.**

## 0. Lựa chọn của series (điền ở bước Input của tập đầu tiên, sau đó giữ cố định)
| Mục | Lựa chọn |
|---|---|
| Phong cách | `TH` (mặc định) · P1 · P2 · P3 · P4 · P6 · màu riêng (xem `assets/styles/`; P5 dùng kit `dark-studio`) |
| Font | `F1` DINRoundOT (mặc định) · F2–F8 (xem `assets/styles/fonts.json`) |
| Giọng đọc | file quay · ghi âm · ElevenLabs · giọng AI · không lời |
| Nhạc nền | AI tạo (mood/bpm/seed) · tải nguồn miễn phí (ghi credit) · không nhạc |
| SFX | AI tạo · nguồn miễn phí |
| Nhân vật | không dùng (mặc định) · người dùng cung cấp |
| Logo | file trong `brand/` (người dùng gửi một lần) · không logo |

## 1. Danh tính hình ảnh
- Design tokens: xem `frame.md` (màu, font, bo góc, bóng, lưới). Màu bên dưới là bảng **TH**. Chọn phong cách khác thì áp `theme.css` theo `assets/styles/README.md`.
- Nền: giấy kem `#F7F0E2`, vignette rất nhẹ ở mép. Các phần "lưu ý/giới hạn" dùng nền tối `#27364A`.
- Khung, thẻ: viền `#27364A` dày 3px, bóng lệch đặc 6px 6px màu `#27364A`, bo góc 14px.
- Từ khóa tiêu đề: chữ màu `#9D6F1D` (`--accent-text`) + gạch chân `#B88A2D`. Từ phủ định hoặc cảnh báo: `#2F5D9F` đậm, không dùng đỏ chói.

## 2. Người dẫn (chọn một ở bước Input, rồi giữ cho cả series)
- **Giọng thuần**: không có hình người dẫn.
- **Người thật**: face-cam tròn đường kính 300px (16:9) ở góc dưới phải, **viền nhịp tim** vẽ theo âm lượng giọng, màu `#B88A2D` trên vòng nền `#EAF2FC`. Lower third: tên (DINRoundOT Bold) + chức danh (Regular), nền trắng viền `#27364A`, xuất hiện một lần trong 15 giây đầu của người đó.
- **Nhân vật**: chỉ dùng khi **người dùng cung cấp** (PNG/SVG nền trong suốt, nên có 3–4 tư thế: đứng, chỉ tay, giơ tay, cầm bảng). Lưu vào `blocks/mascot/`. Agent không tự vẽ nhân vật, không lấy nhân vật trên mạng.

## 3. Loại cảnh của kit
`title, talking, point, list, flow, data, compare, quote, screen, outro` (xem `references/05-pilot.md`; khung dựng sẵn ở `blocks/`), cộng thêm:
- `menu`: thẻ "Nội dung hôm nay" đánh số 1–5, dùng sau phần Hứa
- `warning`: nền tối + dải chéo `#B88A2D`/`#27364A` ở mép trên, cho phần giới hạn hoặc lưu ý
- `tip`: nền `#EAF2FC`, thẻ ghim có nhãn "MẸO 1/3"

## 4. Khung cố định (không đổi giữa các tập)
| Block | Thời lượng | Mô tả |
|---|---|---|
| `intro` | 4s | Tên series hiện lên, nhạc chủ đề vào, logo từ `brand/` nếu có. Dùng khung `title-card` (nhãn = tên series) cho đến khi series có intro riêng |
| `chapter-card` | 2–3s | Khung `title-card`: nhãn `PHẦN X`, tiêu đề phần, số lớn mờ bên phải |
| `footer` | suốt video | Dòng nhỏ `TÊN SERIES · Tập N · Phần X` + 3 ô màu thương hiệu ở góc dưới |
| `outro` | 6s | Khung `three-points` (3 ý chính) rồi khung `cta-outro` (lời kêu gọi + logo từ `brand/`) |
Các khung trong `blocks/` đọc màu từ token của `frame.md`, nên các tập **dùng lại nguyên file**, chỉ đổi nội dung qua biến. Xem `blocks/README.md`.

## 5. Motion language
Chỉ dùng các kiểu dưới đây (xem thông số chi tiết trong `references/motion-rules.md`):
1. **Vào cảnh**: mờ dần + nâng 24px + phóng 0.96→1, `power3.out`, 0.5s
2. **Dựng danh sách**: lệch nhau 0.12s mỗi mục
3. **Nhấn**: gạch chân vàng chạy từ trái sang phải 0.4s, hoặc khoanh tròn nét vẽ tay
4. **Số liệu**: đếm lên 1.2s, `power2.out`, con số dừng lại có nảy nhẹ
5. **Đi sâu**: phóng camera từ khung tổng vào một chi tiết, 0.8s, `power2.inOut`
6. **Ra cảnh**: nhanh hơn lúc vào (0.3s), mờ dần + hạ 12px
7. **Thở**: phần tử đứng yên lắc lư rất nhẹ (±2px, chu kỳ 4s)
Stamp nhấn mạnh (chữ chéo trong khung viền): phóng 1.4→1 + xoay -8°, 0.25s, kèm SFX "stamp".

## 6. Voice profile
- **Nguồn**: `<file-quay | ghi-am | elevenlabs | giong-ai | khong-loi>` (chốt ở tập 1)
- **ElevenLabs**: `voice_id: <điền>` · model Multilingual v2 (hoặc mới hơn nếu hỗ trợ tiếng Việt tốt hơn) · stability 0.5 · similarity 0.75 · style 0.15 · speed 1.0
- **Giọng AI** (`scripts/tts_vi.py`, bản edge-tts ghim trong `assets/kit.lock.json`): engine `edge` · voice `vi-VN-HoaiMyNeural` (nữ) hoặc `vi-VN-NamMinhNeural` (nam) · rate `+12%` (HoaiMy ở `+0%` chỉ khoảng 155 từ/phút; `+12%` đạt chuẩn 170–190) · pitch `+0Hz`
- **Người thật**: cùng một người đọc, micro cài áo, phòng kín. Bộ lọc: `highpass=f=80, afftdn=nf=-25, acompressor=threshold=-20dB:ratio=3, loudnorm=I=-16:TP=-1.5`
- **Không đổi các thông số trên giữa các tập.**
- **Giọng văn**: xưng "mình – bạn", câu ≤ 20 từ, tốc độ 170–190 từ/phút, mở mỗi phần bằng một câu hỏi.
- **Bảng thuật ngữ** (dùng cho phụ đề và cách đọc): `glossary.txt`

## 7. Âm thanh (nguồn: `references/audio-sources.md`)
- **Nhạc chủ đề** `audio/theme.wav`:
  - AI tạo: `make_audio.py music --mood calm --bpm 100 --seed 7` (ghi lại 3 thông số nếu đổi)
  - Hoặc bản tải từ nguồn miễn phí: tên bài, tác giả, link, giấy phép ghi vào `audio/CREDITS.txt`
  - Giữ một mức suốt video, khoảng -36 LUFS (thấp hơn giọng ~20 dB), không tự hạ khi có lời
- **SFX** `audio/sfx/`: whoosh (chuyển chương), pop (phần tử vào), stamp, tick (số đếm), chime (outro), swipe, click. Tạo bằng `make_audio.py sfx` hoặc lấy từ nguồn miễn phí (CC0).

## 8. Xuất file
Mặc định 1920×1080, 30 fps, H.264 yuv420p, AAC 192k, -16 LUFS. Preset theo kênh: xem `references/08-finalize.md`.

## 9. Nhật ký series (bước 7 ghi vào đây)
| Tập | Ngày | Bài học / thay đổi kit |
|---|---|---|
