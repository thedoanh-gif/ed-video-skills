# Bước 6: Dựng & ghép (HyperFrames)

**Đọc `/hyperframes` trước.** File này chỉ nói cách áp quy trình TH lên HyperFrames. Phần cú pháp và luật render nằm trong skill gốc của HyperFrames. Nếu hai bên khác nhau thì theo HyperFrames.

## 1. Khởi tạo dự án
```bash
cd 04_projects/<du-an>
<hf> init hf --non-interactive   # <hf> = npx -y hyperframes@0.9.84 (bản ghim, xem SKILL.md)
```
- Chép từ Series Kit vào dự án:
  - `fonts/` → `hf/assets/fonts/` (DINRoundOT, khai báo `@font-face` trỏ tới `assets/fonts/...`; font F2–F8 do lệnh ở mục 1b chép)
  - `brand/` → `hf/assets/brand/` (logo, nếu có)
  - `audio/` → `hf/assets/audio/` (nhạc chủ đề, SFX)
  - `blocks/*.html` → `hf/compositions/` (7 khung cảnh dựng sẵn + intro/outro riêng của series nếu có)
  - `assets/vendor/gsap.min.js` của skill → `hf/assets/vendor/`, và trong `index.html` dùng `<script src="assets/vendor/gsap.min.js">` thay cho link CDN (mạng công ty hay chặn CDN, render sẽ trắng hình)
- Khai báo các token màu của `frame.md` thành biến CSS trên `:root` trong `index.html` (`--bg`, `--bg-alt`, `--bg-dark`, `--ink`, `--ink-2`, `--primary`, `--primary-deep`, `--accent`, `--accent-text`, `--card`, `--radius-card`, `--card-border`, `--card-shadow`, `--font-display`). Các khung cảnh tự đọc biến này, nên đổi bảng màu chỉ cần sửa một chỗ.
- Đặt `frame.md` của Series Kit vào dự án làm design system để `/hyperframes-creative` đọc được.

## 1b. Áp phong cách và font đã chọn
```bash
<python> <skill>/assets/styles/tao_mau.py --ap-dung <TH|P1…P6> --font <F1…F8> --hf <du-an>/hf
```
- TH, P1–P4, P6: dán `hf/assets/phong-cach.css` vào `<style>` của `index.html` **sau** khối `:root` của `frame.md`; mỗi thẻ gắn khung thêm class `sb sb-<ten-ngan>` (bảng ở `assets/styles/README.md`). Thiếu class thì khung hiện kiểu mặc định.
- P5: `engine/comp.py` tự chèn file đó khi chạy `build.py`; chọn F1 thì không cần chạy lệnh.
- Font khác F1 làm chữ rộng, hẹp khác nhau: sau khi áp phải qua cổng QC và xem khung.

## 2. Mỗi chương là một composition riêng
- `hf/compositions/ch01.html`, `ch02.html`… Mỗi chương có **một timeline GSAP dừng sẵn**, đăng ký vào `window.__timelines["<id>"]`.
- Mỗi chương dài 30–60 giây và render riêng ra `renders/ch01.mp4`. Thông số **giống hệt nhau** giữa các chương (kích thước, fps, codec) để ghép không cần encode lại.
- Intro và outro dùng block cố định của series, **không thiết kế lại** ở từng tập.

## 2b. Gắn khung cảnh có sẵn
Mỗi shot dùng khung trong `blocks/` là một thẻ gắn, nội dung đi qua `data-variable-values` (xem `blocks/README.md` để biết biến của từng khung):
```html
<div id="c02-s03" class="clip sb sb-points" data-composition-id="c02-s03"
     data-composition-src="compositions/three-points.html"
     data-start="12.4" data-duration="7.5"
     data-variable-values='{"heading":"Ba điều cần nhớ","items":"Học đúng việc|Học đúng lúc|Học có người kèm","times":"0.2|1.1|2.9|4.6"}'></div>
```
- `data-composition-id` mỗi thẻ là duy nhất (dùng luôn id của shot). Một khung gắn nhiều lần được.
- Không sửa file khung để đổi nội dung. Muốn đổi kiểu dáng của cả series thì sửa ở `03_series-kits/<series>/blocks/` và ghi vào nhật ký kit.

## 3. Những luật dễ sai (tóm tắt từ /hyperframes, xem bản đầy đủ ở đó)
- Phần tử có thời gian dùng `class="clip"` + `data-start` + `data-duration` (giây).
- Mọi thứ hiển thị phải tính theo thời gian timeline: không dùng `Math.random()` không seed, `Date.now()`, timer, `repeat: -1`.
- Animate transform/opacity, không animate `left/top/width/height`. Không tween `display/visibility` trên `.clip`.
- Giọng và nhạc là `<audio>` riêng **có `id`**. Video face-cam giữ tiếng thì dùng `data-has-audio="true"`, không thì `muted`.
- Đường dẫn asset bắt đầu bằng `assets/...`, không có `/` ở đầu.
- Trước khi render, phải qua **cổng QC** ở mục 7.

## 4. Đồng bộ với giọng
- Đọc `audio/narration.words.json` (từ `scripts/to_srt.py`). Tạo `data-start` cho từng phần tử theo **thời điểm của từ khóa** ghi trong shot list, không gõ số giây bằng tay.
- Cách làm gợi ý: viết một file `timing.js` hoặc JSON map `keyword → giây` sinh từ words.json, rồi để các composition đọc file đó. Đổi giọng thì chỉ cần sinh lại map này.

## 4b. Video số liệu dễ cập nhật (đã dùng cho video báo cáo, kit `dark-studio/engine/`)
Chuỗi một chiều: `du-lieu.txt` (người dùng sửa) → `gen_script.py` → `script*.md/txt` + `data.json` → `build.py` → `hf/` → trộn → kiểm tra → render → phụ đề.
- Số trên hình đọc từ `data.json`, không gõ cứng. Chữ ngắn trên hình cũng là khóa riêng trong file dữ liệu (`*_nhan`). Dòng chữ đưa vào lời đọc thì viết số bằng chữ.
- **Neo mốc hình theo dòng lời và đoạn giữa hai dấu câu** (`Comp.L(dong, doan)`), không neo vào chính con số. Cần bắt con số thì neo vào từ cố định đứng trước (`Comp.N`).
- Script dựng phải **dừng khi giọng cũ không khớp lời mới**. Chỉ tạo lại giọng các chương đổi lời (so mã băm từng chương).
- Hình phải xử lý được cả hai chiều của số liệu (đạt / chưa đạt, tăng / giảm). **Thử trên bản sao**: đổi số cho đảo chiều, dựng lại, xem khung.
- Nói rõ cho người dùng: đổi số và chữ ngắn thì hình tự theo; đổi chủ đề thì phải sửa cảnh.

## 4c. Lỗi bố cục và phụ đề đã gặp, tránh từ đầu
- Nhóm phần tử phủ toàn khung: đặt `transform-origin` đúng tâm **trước** khi phóng, nếu không nội dung trôi lệch.
- Nhãn trạng thái không đặt đè cột tên trong bảng so sánh. Dấu ✕, con dấu không che chữ cần đọc; con dấu cần nền đủ tối.
- Chữ vừa hiện đã mất là lỗi: giữ đủ thời gian đọc. `slam` phóng to lúc vào có thể đè phần tử bên cạnh, khi đó dùng `pop`.
- Bong bóng, khung chat, thẻ không để rỗng quá lâu trước khi chữ hiện.
- Phụ đề: không tách từ ghép và đơn vị tiền ("tỷ đồng", "triệu đồng"), gộp mẩu ngắn; ≤ 42 ký tự/dòng, 1–6 giây (`engine/make_srt.py`).
- `check` toàn video mất vài phút: khi sửa một cảnh, dùng `<hf> check hf --range=<đầu>,<cuối>` trước, rồi chạy đủ một lần ở cuối.
- edge-tts báo "No audio was received": chạy lại `--only` đúng chương đó.

## 5. Face-cam (cảnh `talking`)
- Cắt khung mặt từ video gốc (ffmpeg crop/scale), đặt vào khung tròn theo Series Kit.
- Viền nhịp tim: lấy đường bao âm lượng (RMS) từ audio bằng ffmpeg hoặc Python, xuất thành mảng giá trị theo frame (JSON). Viền vẽ bằng SVG, độ dày/biên độ theo giá trị tại thời điểm hiện tại. Tất cả phải tính được từ thời gian timeline.
- Video quay có ánh sáng tối hoặc phẳng → xử lý màu bằng `<hf> media-treatment`, không dùng CSS filter.

## 6. Âm thanh (nguồn: `audio-sources.md`)
- Giọng AI (lựa chọn D): `<python> <skill>/scripts/tts_vi.py script-voice.txt --out audio/ --voice <theo kit> --rate <theo kit>` → `chXX.mp3` + `chXX.words.json` (không cần transcribe).
- Nhạc/SFX do AI tạo: `make_audio.py music|sfx` với mood/bpm/seed của kit. Tạo một lần, lưu vào Series Kit, các tập sau dùng lại.
- **Giọng**: chuẩn hóa về khoảng -16 LUFS. Giọng người thật thu ồn thì lọc nhẹ (highpass 80 Hz, khử ồn vừa phải, compressor nhẹ). Ghi bộ lọc đã dùng vào Series Kit để các tập sau dùng y hệt.
- **Nhạc nền**: dùng nhạc chủ đề của series, **giữ một mức suốt video** (không tự nhỏ đi khi có lời), khoảng -36 LUFS, thấp hơn giọng khoảng 20 dB; chỉ vào nhẹ ở đầu và nhỏ dần ở cuối. `mix_audio.py` làm sẵn như vậy; to hơn: `--music-lufs -33`; kiểu tự hạ theo lời (`--duck`) chỉ khi người dùng yêu cầu.
- **SFX**: chỉ dùng bộ SFX của kit. Mỗi chương tối đa 3–5 SFX. SFX nhấn đúng lúc motion, không rải đều.
- Trộn bằng `<python> <skill>/scripts/mix_audio.py timing.json --voice-dir audio --music audio/theme.wav --sfx-dir audio/sfx -o audio/mix.wav` (mẫu `timing.json` ở đầu script).
- Có thể mix bằng `<audio>` trong HyperFrames, hoặc mix ngoài thành một file `audio/mix.wav` cho cả video rồi ghép bằng `scripts/join_chapters.py --audio`. Với video có nhiều chương, nên dùng cách thứ hai để tránh hụt tiếng ở chỗ nối chương.

## 7. Cổng QC trước khi render (bắt buộc, kể cả pilot)
Lỗi bố cục (chữ chồng, chữ bị cắt, khoảng trống hình) phải bị máy chặn trước khi tốn thời gian render, không phải để người xem phát hiện.

```bash
<hf> check hf --json --at-transitions --safe-zone=standard
```
- `check` gộp lint + chạy thử trong Chrome + kiểm bố cục + độ tương phản + "craft" (đoạn đứng hình quá lâu, khung đầu trống, phim không có tiếng). `--at-transitions` lấy mẫu ở mọi điểm chuyển cảnh để bắt chữ chồng thoáng qua.
- **Điều kiện qua cổng:** `ok: true` và **0 lỗi** (error). Cảnh báo (warning) thì sửa, hoặc ghi lý do giữ lại vào `build-log.md`. Ví dụ hợp lệ: `dead_stretch` 4 giây ở cảnh câu chốt vì đang chờ giọng đọc hết câu (vẫn trong chuẩn ≤ 10–15 giây của Style Bible).
- Sau đó xem bằng mắt: `<hf> snapshot hf --review` rồi mở contact sheet (`review-beats.jpg`, `review-seam-*.jpg`, `review-phone.jpg`). Tìm chữ đè, chữ sát mép, khung trống, chỗ nối chương bị giật.
- Có lỗi thì sửa rồi chạy lại cổng. **Tối đa 2 vòng tự sửa**; còn lỗi thì dừng, báo người dùng (lỗi gì, ở giây nào, đề xuất cách xử lý).
- Lần chạy đầu mất 1–3 phút vì phải mở Chrome; các lần sau dùng cache nếu file không đổi.

## 8. Render
```bash
<hf> render hf -q draft -o renders/ch01_draft.mp4     # nháp nhanh để tự xem
<hf> render hf -o renders/ch01.mp4                     # mặc định quality looks; -q delivery cho bản cuối
```
- Render từng chương: `renders/ch01.mp4`… Ghi tạm ra tên khác rồi mới đổi tên khi render xong (tránh file dở dang).
- Ghép: `<python> <skill>/scripts/join_chapters.py renders/ch*.mp4 -o renders/full.mp4 --audio audio/mix.wav`
- Sửa một chương: chỉ render lại chương đó rồi ghép lại.

## 9. Ghi nhật ký
Lưu vào `build-log.md`: lệnh đã chạy, thời gian render từng chương, lỗi gặp phải và cách sửa. Bước 8 sẽ dùng nhật ký này để rút bài học cho Series Kit.
