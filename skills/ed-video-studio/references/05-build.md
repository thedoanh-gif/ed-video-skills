# Bước 5: Dựng & ghép (HyperFrames)

**Đọc `/hyperframes` trước.** File này chỉ nói cách áp quy trình TH lên HyperFrames. Phần cú pháp và luật render nằm trong skill gốc của HyperFrames. Nếu hai bên khác nhau thì theo HyperFrames.

## 1. Khởi tạo dự án
```bash
cd 04_projects/<du-an>
npx hyperframes init hf          # xem `npx hyperframes init --help` cho các tùy chọn hiện hành
```
- Chép từ Series Kit vào `hf/assets/`: `fonts/` (DINRoundOT, khai báo bằng `@font-face` trỏ tới `assets/fonts/...`), `audio/` (nhạc chủ đề, SFX), `blocks/` (intro, thẻ chuyển chương, outro cố định nếu kit có).
- Đặt `frame.md` của Series Kit vào dự án làm design system để `/hyperframes-creative` đọc được.

## 2. Mỗi chương là một composition riêng
- `hf/compositions/ch01.html`, `ch02.html`… Mỗi chương có **một timeline GSAP dừng sẵn**, đăng ký vào `window.__timelines["<id>"]`.
- Mỗi chương dài 30–60 giây và render riêng ra `renders/ch01.mp4`. Thông số **giống hệt nhau** giữa các chương (kích thước, fps, codec) để ghép không cần encode lại.
- Intro và outro dùng block cố định của series, **không thiết kế lại** ở từng tập.

## 3. Những luật dễ sai (tóm tắt từ /hyperframes, xem bản đầy đủ ở đó)
- Phần tử có thời gian dùng `class="clip"` + `data-start` + `data-duration` (giây).
- Mọi thứ hiển thị phải tính theo thời gian timeline: không dùng `Math.random()` không seed, `Date.now()`, timer, `repeat: -1`.
- Animate transform/opacity, không animate `left/top/width/height`. Không tween `display/visibility` trên `.clip`.
- Giọng và nhạc là `<audio>` riêng **có `id`**. Video face-cam giữ tiếng thì dùng `data-has-audio="true"`, không thì `muted`.
- Đường dẫn asset bắt đầu bằng `assets/...`, không có `/` ở đầu.
- Trước khi render, chạy `npx hyperframes check --json` và sửa hết lỗi.

## 4. Đồng bộ với giọng
- Đọc `audio/narration.words.json` (từ `scripts/to_srt.py`). Tạo `data-start` cho từng phần tử theo **thời điểm của từ khóa** ghi trong shot list, không gõ số giây bằng tay.
- Cách làm gợi ý: viết một file `timing.js` hoặc JSON map `keyword → giây` sinh từ words.json, rồi để các composition đọc file đó. Đổi giọng thì chỉ cần sinh lại map này.

## 5. Face-cam (cảnh `talking`)
- Cắt khung mặt từ video gốc (ffmpeg crop/scale), đặt vào khung tròn theo Series Kit.
- Viền nhịp tim: lấy đường bao âm lượng (RMS) từ audio bằng ffmpeg hoặc Python, xuất thành mảng giá trị theo frame (JSON). Viền vẽ bằng SVG, độ dày/biên độ theo giá trị tại thời điểm hiện tại. Tất cả phải tính được từ thời gian timeline.
- Video quay có ánh sáng tối hoặc phẳng → xử lý màu bằng `npx hyperframes media-treatment`, không dùng CSS filter.

## 6. Âm thanh (nguồn: `audio-sources.md`)
- Giọng AI (lựa chọn D): `<python> <skill>/scripts/tts_vi.py script-voice.txt --out audio/ --voice <theo kit> --rate <theo kit>` → `chXX.mp3` + `chXX.words.json` (không cần transcribe).
- Nhạc/SFX do AI tạo: `make_audio.py music|sfx` với mood/bpm/seed của kit. Tạo một lần, lưu vào Series Kit, các tập sau dùng lại.
- **Giọng**: chuẩn hóa về khoảng -16 LUFS. Giọng người thật thu ồn thì lọc nhẹ (highpass 80 Hz, khử ồn vừa phải, compressor nhẹ). Ghi bộ lọc đã dùng vào Series Kit để các tập sau dùng y hệt.
- **Nhạc nền**: dùng nhạc chủ đề của series, giữ một mức suốt video (xem `06-build.md` mục 6).
- **SFX**: chỉ dùng bộ SFX của kit. Mỗi chương tối đa 3–5 SFX. SFX nhấn đúng lúc motion, không rải đều.
- Có thể mix bằng `<audio>` trong HyperFrames, hoặc mix ngoài thành một file `audio/mix.wav` cho cả video rồi ghép bằng `scripts/join_chapters.py --audio`. Với video có nhiều chương, nên dùng cách thứ hai để tránh hụt tiếng ở chỗ nối chương.

## 7. Render
```bash
npx hyperframes render ...      # xem --help: chọn composition/chương, output, chất lượng
```
- Render từng chương: `renders/ch01.mp4`… Ghi tạm ra tên khác rồi mới đổi tên khi render xong (tránh file dở dang).
- Trước khi render cả chương, xem 2–3 frame ở những chỗ có nhiều thứ nhất trên màn hình (`npx hyperframes snapshot --at ...`).
- Ghép: `<python> <skill>/scripts/join_chapters.py renders/ch*.mp4 -o renders/full.mp4 --audio audio/mix.wav`
- Sửa một chương: chỉ render lại chương đó rồi ghép lại.

## 8. Ghi nhật ký
Lưu vào `build-log.md`: lệnh đã chạy, thời gian render từng chương, lỗi gặp phải và cách sửa. Bước 7 sẽ dùng nhật ký này để rút bài học cho Series Kit.
