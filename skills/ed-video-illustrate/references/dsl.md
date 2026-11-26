# Mô tả cảnh cho khối `th-canvas`

Khối: `assets/th-canvas.html` (đã copy vào `03_series-kits/<series>/blocks/`). Mỗi cảnh là một host `data-composition-src="compositions/th-canvas.html"` với `data-variable-values='{"spec":"<JSON>","dur":<giây>}'`.

```
spec = { bg: "navy|light|cream|ink", acc: "gold|sky|mint|blush|pri", els: [ phần_tử, ... ] }
```
Tọa độ theo khung 1920×1080, `x,y` là góc trên-trái (riêng `person`: giữa-chân; `ic`: tâm). `t` = giây vào (tính từ đầu cảnh), `out` = giây biến mất, `a` = kiểu vào: `pop|up|down|left|right|fade|zoom|slam`.

## Phần tử (`k`)
| k | Tham số chính | Ghi chú |
|---|---|---|
| `text` | text, size, w, al, hl (cụm tô), hlc, hlt (giờ gạch chân), c, wt, type (gõ chữ) | chữ ra từng từ qua khung cắt; tô + gạch chân cụm `hl` |
| `badge` | n, text, sub, c | huy hiệu số + tên phần (như M1: ô màu số 1) |
| `tag` | text, c, rot | nhãn dán nghiêng |
| `crumb` | text | đường dẫn mono ở góc (tự thêm khi cảnh có `crumb`) |
| `person` | who a–f, s (tỉ lệ), face, pose, poseL, flip, talk=[[t0,t1],..], nod=[t..], look l/r, armT | nhân vật có tay, mắt chớp, miệng nói đúng khoảng `talk` |
| `bubble` | text, w, tail fl/fr/none, c, size, type, out | bong bóng thoại, `type` gõ từng chữ |
| `think` | text, w, dx, type | bong bóng suy nghĩ (đám mây) |
| `card` | head, hc, hs, lines, w, h, els[] | thẻ giấy; `els` là phần tử con (tọa độ tương đối thẻ) |
| `win` | title, w, h, els[] | cửa sổ có thanh tiêu đề |
| `chat` | w, msgs=[{w:me/you,text,t,type}] | khung chat tự xếp, mỗi tin bật vào đúng `t` |
| `ic` | n (ear, eye, bell, bellx, clock, heart, phone, phoneDown, laptop, cup, check, cross, doc, calendar, mic, door, bulb, target, gift, qm, star, share, note, lock, tableC, deskC), s, spin, close (gập laptop), open (mở cửa), still | icon có chuyển động riêng |
| `chip` | text, mk x/v, c, size | viên thuốc ✓/✕ |
| `stamp` | text, c, rot, size | dấu đóng nảy vào |
| `ring` `strike` `under` | x,y,w,h,c | vẽ nét khoanh, gạch bỏ, gạch chân |
| `arrow` | x1,y1,x2,y2,cv (độ cong), c | mũi tên vẽ nét |
| `cursor` | x1,y1,x2,y2 | con trỏ di chuyển và bấm |
| `bar` | w, to, v0, fmt "{n}%", label, c, dur | thanh đầy lên + số |
| `num` | to, suffix, size, c | số đếm lên |
| `wave` | w,h,c,stop | sóng âm nhảy, dừng ở `stop` |
| `tiles` | cols, rows, size, st | lưới ô màu bật lần lượt |
| `shape` | w,h,c,r,els | khối màu / khung điện thoại (lồng `els`) |

Mọi cảnh tự có: nền trang trí trôi, camera đẩy nhẹ, mảng vàng+xanh quét ở đầu và cuối cảnh (khớp với cảnh kế).

## Neo giờ theo lời (Python, `build_v3.py`)
```python
A("laptop", nth=1, after=13.0, lag=0.0)   # giây của từ "laptop" (gần mốc 13.0 của chương) + lag, tính ra tương đối đầu cảnh
```
- `after` là mốc giây trong chương để chọn đúng lần xuất hiện. **Luôn dùng nth=1** với `after` sát mốc; nth ≥ 2 dễ nhảy sang đoạn sau.
- Build in `MUỘN/SỚM` khi một mốc rơi sát cuối cảnh hoặc trước đầu cảnh: sửa hết trước khi render.
- Sau build chạy `hyperframes check`, `snapshot` ở ~70% mỗi cảnh, rồi so với video mẫu.
