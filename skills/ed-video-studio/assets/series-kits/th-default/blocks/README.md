# blocks/: 7 khung cảnh dựng sẵn

Mỗi file là một sub-composition HyperFrames 1920×1080 có biến. Gắn vào `index.html` bằng `data-composition-src`, đổi nội dung bằng `data-variable-values`. **Không sửa file khung để đổi nội dung.**

```html
<div id="c01-s02" class="clip" data-composition-id="c01-s02"
     data-composition-src="compositions/big-number.html"
     data-start="8.2" data-duration="6"
     data-variable-values='{"value":"38","suffix":"%","label":"nhân viên mới nghỉ việc trong năm đầu","times":"0.3|1.4|2.0"}'></div>
```

## Danh sách khung
| Khung | Loại cảnh | Biến chính | `times` (giây, tính từ đầu cảnh) | Thời lượng gợi ý |
|---|---|---|---|---|
| `title-card` | title, chapter-card, intro tạm | `eyebrow`, `title`, `subtitle`, `number` | nhãn \| tiêu đề \| dòng phụ | 3–5s |
| `big-number` | data | `value`, `prefix`, `suffix`, `label`, `note`, `count` | số bắt đầu đếm \| ý nghĩa \| nguồn | 5–7s |
| `three-points` | list, tóm tắt | `heading`, `items` (2–4 ý, ngăn bằng `\|`), `focus` | tiêu đề \| ý 1 \| ý 2 \| ý 3 \| ý 4 | 6–10s |
| `compare` | compare (trước/sau, sai/đúng) | `heading`, `left_title`, `left_items`, `right_title`, `right_items` | tiêu đề \| cột trái \| cột phải | 6–9s |
| `process-steps` | flow | `heading`, `steps` (3–5 bước) | tiêu đề \| bước 1 \| bước 2 \| … | 6–10s |
| `key-message` | quote, câu chốt cuối mỗi phần | `message`, `highlight`, `by` | câu chốt \| tô màu \| nguồn | 4–6s |
| `cta-outro` | outro | `title`, `action`, `contact`, `logo` | logo \| lời kêu gọi \| hành động \| liên hệ | 5–7s |

Biến để trống thì phần đó ẩn. Chữ dài hơn giới hạn thì khung tự thu nhỏ cỡ chữ, nhưng vẫn nên giữ đúng giới hạn số từ (Style Bible: mục ≤ 5 từ, tiêu đề ≤ 8 từ).

## Mốc `times`
Lấy từ `audio/*.words.json`: giây của từ khóa trừ `data-start` của cảnh. Chữ hiện cùng lúc hoặc trễ ≤ 0,2s so với lời. Thiếu giá trị nào thì khung dùng mặc định.

## Màu và kiểu dáng
Khung đọc token CSS trên `:root` của `index.html` (xem `frame.md`): `--bg`, `--bg-alt`, `--bg-dark`, `--ink`, `--ink-2`, `--primary`, `--accent`, `--accent-text`, `--accent-on-dark`, `--card`, `--radius-card`, `--card-border`, `--card-shadow`, `--font-display`. Đổi bảng màu hoặc phong cách (Paper có viền + bóng đặc, hay Sạch có bóng mờ) chỉ cần đổi token.

## Phong cách (TH, P1–P4, P6)
Muốn khung mang giao diện phong cách: dán CSS do `ed-video-studio/assets/styles/tao_mau.py --ap-dung` tạo vào `index.html`, và thêm vào thẻ gắn class `sb sb-<ten-ngan>`: `sb-title`, `sb-number`, `sb-steps`, `sb-compare`, `sb-points`, `sb-message`, `sb-outro`.

## Yêu cầu khi dùng
- `index.html` nạp GSAP tại chỗ: `<script src="assets/vendor/gsap.min.js"></script>` (file có trong skill `ed-video-studio/assets/vendor/`).
- Khai báo `@font-face` DINRoundOT (400, 500, 700), hoặc dùng CSS phong cách + font ở trên.
- Thời lượng cảnh do `data-duration` của **thẻ gắn** quyết định. Thẻ gốc bên trong file khung để `data-duration="600"`; đặt ngắn hơn thẻ gắn thì phần dư bị **đen hình**.
- Đã kiểm với HyperFrames 0.9.84: `check --at-transitions --safe-zone=standard` 0 lỗi; render 45 giây (7 khung) bản nháp mất khoảng 80 giây trên máy 4 nhân.

## Thêm khung mới
Chép một khung gần giống, đổi `data-composition-id` (ở thẻ gốc, trong mọi selector CSS và ở `window.__timelines["…"]`) thành tên mới, khai báo biến trong `data-composition-variables`. Chạy cổng QC rồi mới đưa vào kit.
