# frame.md: Design tokens TH Paper

Dạng DESIGN.md để /hyperframes-creative đọc. Các giá trị dưới đây là nguồn duy nhất về màu, font và kích thước. Không viết giá trị trực tiếp vào composition.

## Color
| Token | Hex | Dùng cho |
|---|---|---|
| `--bg` | `#F7F0E2` | Nền giấy chính |
| `--bg-alt` | `#EAF2FC` | Nền phần "mẹo", vòng nền face-cam |
| `--bg-dark` | `#27364A` | Nền phần lưu ý, thẻ ngắt, nhãn chương |
| `--ink` | `#27364A` | Chữ chính, viền, bóng |
| `--ink-2` | `#6B7280` | Chữ phụ, chú thích |
| `--primary-deep` | `#234C87` | Nhấn xanh đậm |
| `--primary` | `#2F5D9F` | Biểu tượng, đường nối, thanh biểu đồ |
| `--accent` | `#B88A2D` | Từ khóa, gạch chân, viền nhịp tim |
| `--accent-text` | `#9D6F1D` | Từ khóa dạng chữ trên nền sáng (đủ tương phản) |
| `--card` | `#FFFFFF` | Thẻ, cửa sổ |
| `--accent-on-dark` | `#E2C27D` | Chữ nhấn trên nền tối (khung `key-message`) |
Quy tắc: mỗi khung tối đa **1 màu nhấn chính** (vàng hoặc xanh) cộng với màu mực. Không dùng xanh hoặc vàng bão hòa cao. Series chọn phong cách khác (P1–P4, P6) thì `theme.css` của phong cách ghi đè các token này (`assets/styles/`); bảng màu riêng thì thay token, giữ nguyên tên.

## Typography
- Font: **DINRoundOT**, 8 file có sẵn trong `fonts/` của kit: Light, Regular, Medium, Bold (+ Italic của từng loại). Chép vào `hf/assets/fonts/` và khai báo `@font-face` (font-family `DINRoundOT`, weight 300/400/500/700). **Không có bản Black**: chữ display dùng Bold.
- DINRoundOT là mặc định (F1). Series chốt font khác (F2–F8, `assets/styles/fonts.json`) thì đó là font của series, áp bằng `assets/styles/tao_mau.py --ap-dung`.
- Thiếu font thì **dừng lại báo người dùng**, không tự thay bằng font khác ở bản cuối.
- Mono (nhãn chương, code): `JetBrains Mono` hoặc font mono có sẵn trên máy.
| Vai trò | Cỡ (1920×1080) | Đậm | Line-height |
|---|---|---|---|
| Display (title, số liệu) | 120–160px | Bold (700) | 1.0 |
| H1 (tiêu đề cảnh) | 72px | Bold | 1.1 |
| H2 | 48px | Bold | 1.2 |
| Body (thẻ, danh sách) | 36–40px | Medium | 1.3 |
| Caption, nhãn | 24–28px | Medium, mono | 1.2 |
Khổ 9:16 (1080×1920): giữ nguyên cỡ chữ, chỉ đổi bố cục thành dạng dọc.

## Shape
- Bo góc: thẻ 14px · nút, tag 999px · face-cam tròn
- Viền: 3px `--ink`
- Bóng: `6px 6px 0 var(--ink)` (bóng đặc, không blur)

Token hình khối mà các khung trong `blocks/` đọc (khai báo trên `:root` của `index.html`):
| Token | Giá trị TH Paper |
|---|---|
| `--radius-card` | `14px` |
| `--card-border` | `3px solid #27364A` |
| `--card-shadow` | `6px 6px 0 #27364A` |
| `--font-display` | `'DINRoundOT', sans-serif` |
Không khai báo thì khung dùng kiểu "sạch" (bo 28px, bóng mờ, không viền). Đổi phong cách của cả series chỉ cần đổi 3 token này.

Khối khai báo mẫu, chép vào `<style>` của `index.html`:
```css
:root{--bg:#F7F0E2;--bg-alt:#EAF2FC;--bg-dark:#27364A;--ink:#27364A;--ink-2:#6B7280;
  --primary-deep:#234C87;--primary:#2F5D9F;--accent:#B88A2D;--accent-text:#9D6F1D;--accent-on-dark:#E2C27D;
  --card:#FFFFFF;--radius-card:14px;--card-border:3px solid #27364A;--card-shadow:6px 6px 0 #27364A;
  --font-display:'DINRoundOT',sans-serif}
```

## Layout
- Vùng an toàn: chữ chính cách mép trái/phải ít nhất 192px và trên/dưới 108px (title-safe 10%, đúng mức `<hf> check --safe-zone=standard` kiểm). Các khung trong `blocks/` đã tuân theo.
- Lưới 12 cột, gutter 32px. Tiêu đề cảnh neo ở vị trí cố định: trên trái (x=96, y=96) hoặc giữa trên.
- Nhãn chương: góc trên trái, trên tiêu đề 16px. Footer: đáy, cách mép 40px.

## Motion tokens
| Token | Giá trị |
|---|---|
| `--ease-in-scene` | `power3.out` |
| `--ease-move` | `power2.inOut` |
| `--dur-enter` | 0.5s |
| `--dur-exit` | 0.3s |
| `--stagger` | 0.12s |
| `--dur-zoom` | 0.8s |
