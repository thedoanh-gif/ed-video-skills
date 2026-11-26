---
name: ed-video-studio
description: 'Làm video motion graphic chuẩn TH trên HyperFrames từ input đến MP4: video ~5 phút, người thật kèm minh họa, bản tin, đào tạo; giữ phong cách và giọng đồng nhất theo series.'
---

# ED_Video Studio

Skill điều phối (v1.4). Mục tiêu: người dùng chỉ cần đưa input và duyệt ở 3 điểm, còn lại agent làm, đồng thời mỗi video **giống các tập khác trong cùng series** về hình, nhịp và giọng.

## Khi bắt đầu: người dùng chọn phong cách và font
Áp dụng cho mọi video **chưa có Series Kit đã chốt**. Làm trước khi viết brief và kịch bản.

1. Đã ghi mã trong yêu cầu (ví dụ "Phong cách: P3. Font: F4", từ trang hướng dẫn) thì dùng luôn, **không hỏi lại**; chỉ nhắc nếu lựa chọn có giới hạn (xem bảng dưới).
2. Chưa ghi thì **gửi hai ảnh** `assets/styles/preview/chon-phong-cach.jpg` và `chon-font.jpg` (có công cụ gửi file thì gửi file, không thì đưa đường dẫn).
3. Hỏi **một mã phong cách và một mã font** bằng tin nhắn, kèm đề xuất theo nội dung và lý do một dòng. Danh sách có 7 phong cách và 8 font, nên không ép vào hộp chọn chỉ vài đáp án; nếu dùng hộp chọn thì ghi rõ "hoặc gõ mã khác trong ảnh".
4. Gom cùng lượt với giọng đọc, nhạc nền, logo (`references/01-intake.md`). Ghi mã đã chọn vào `brief.md` và Series Kit.

| Mã | Phong cách | Hợp với |
|---|---|---|
| TH | TH BlueGold (mặc định) | Chính sách, đào tạo, truyền thông chính thức |
| P1 | Năng lượng | Sự kiện, phong trào, kêu gọi tham gia |
| P2 | Tươi mát | Sức khỏe, phúc lợi, môi trường |
| P3 | Nắng sớm | Kỹ năng, mẹo làm việc, Coffee Monday |
| P4 | Kẹo ngọt | Văn hóa, gắn kết, ngày lễ |
| P5 | Dark Studio | Công nghệ, AI, hướng dẫn phần mềm, báo cáo số liệu |
| P6 | Nhiều màu | Giới thiệu, hướng dẫn vui, truyền thông trẻ |

Font: **F1** DINRoundOT (mặc định, chỉ nội bộ) · **F2** Montserrat · **F3** Segoe UI · **F4** Roboto · **F5** Open Sans · **F6** Josefin Sans · **F7** Roboto Slab · **F8** Constantia. F3, F8 chỉ dựng được trên Windows. P1–P4, P6 chưa dùng cho video dài và chỉ mới kiểm khổ 16:9.

Cách áp vào dự án: `<python> <skill>/assets/styles/tao_mau.py --ap-dung <ma> --font <ma> --hf <du-an>/hf`, rồi làm theo `assets/styles/README.md`.

## Trước khi bắt đầu

1. **Kiểm tra môi trường bằng một lệnh**: `<python> <skill>/scripts/doctor.py` (thêm `--full` để kiểm cả HyperFrames và Chrome; cách sửa in ngay dưới mỗi lỗi). Script đọc phiên bản đã ghim trong `assets/kit.lock.json` và báo OK / CẢNH BÁO / LỖI cho Node, HyperFrames, FFmpeg, Python, edge-tts, mạng tới máy chủ giọng đọc, telemetry. Có LỖI thì dừng lại, chỉ người dùng tới `CAI-DAT.md`, không tự cài giữa chừng một dự án. Skill cần chạy **trên máy đã cài HyperFrames**. Ở môi trường không cài được (ví dụ chat trên web) vẫn làm được bước 1–2 (brief, kịch bản) và Voice→SRT, rồi báo người dùng mở Claude Code để dựng.
2. **Máy công ty, không có quyền admin.** Không chạy lệnh nào cần quyền quản trị: không "Run as administrator", không `sudo`, không cài vào `Program Files`, không sửa PATH hệ thống (chỉ PATH của người dùng), không choco, không Docker. `doctor` của HyperFrames có thể gợi ý lệnh cần quyền admin (whisper-cpp, Docker): bỏ qua, đó là phần tùy chọn. Cách cài không cần admin: `CAI-DAT.md`.
3. **Đọc skill `/hyperframes` trước khi viết bất kỳ dòng HTML nào.** Luật render của HyperFrames thắng mọi hướng dẫn trong skill này nếu hai bên mâu thuẫn.
4. **Tìm thư mục làm việc `TH-Video/`** (thường nằm ở Desktop/Documents/OneDrive). Không thấy thì hỏi người dùng. Cấu trúc:
   ```
   TH-Video/
     01_library/          video mẫu + transcript (.vtt)
     02_style-bible/      STYLE-BIBLE.md (do ed-video-style-library tạo)
     03_series-kits/<series>/   series-kit.md, frame.md, fonts/, brand/ (logo), audio/, blocks/
     04_projects/yymmdd_ten-video/   mỗi video một thư mục
   ```
5. **Nạp chuẩn**: đọc `02_style-bible/STYLE-BIBLE.md` và Series Kit của series được chọn. Chưa có Series Kit thì dùng `assets/series-kits/th-default/` (có sẵn font DINRoundOT và 7 khung cảnh dựng sẵn), áp phong cách và font người dùng chọn (`assets/styles/`), cùng giọng, nhạc, rồi lưu thành kit mới. Người dùng chọn **P5 Dark Studio** thì dùng kit `dark-studio` (`03_series-kits/dark-studio/`, bản gốc ở `assets/series-kits/dark-studio/`): đã được duyệt hình, có sẵn bộ mã dựng trong `engine/`.

## Gọi HyperFrames (`<hf>`): luôn dùng bản đã ghim
Trong bộ skill này, `<hf>` nghĩa là `npx -y hyperframes@<phiên bản trong assets/kit.lock.json>`, hiện là **`npx -y hyperframes@0.9.84`**. Không gọi `npx hyperframes` trần: `npx` sẽ tự tải bản mới nhất và làm vỡ dự án đang làm dở (đã xảy ra: 0.9.59 → 0.9.84 giữa chừng). Muốn nâng phiên bản thì làm riêng: thử trên một dự án mẫu, chạy đủ cổng QC, rồi mới sửa `kit.lock.json`. Đặt biến môi trường người dùng `HYPERFRAMES_NO_TELEMETRY=1` (lệnh trong `CAI-DAT.md`) để tắt gửi dữ liệu sử dụng.

## Gọi Python (`<python>`)
Trong bộ skill này, `<python>` là lệnh Python 3 chạy được trên máy. Xác định một lần ở đầu phiên rồi dùng xuyên suốt:
- **macOS/Linux**: `python3`.
- **Windows**: thử lần lượt `py -3`, `python`, rồi `%LOCALAPPDATA%\Programs\Python\Python3*\python.exe` (gọi bằng đường dẫn đầy đủ; trong PowerShell đặt `&` phía trước). Không dùng `python3`: trên Windows thường không có. `python` báo "Python was not found" tức là lối tắt Microsoft Store, bỏ qua và thử lệnh kế tiếp. Chỉ nhận lệnh nào chạy `--version` ra Python 3.
- **Windows**: đặt `PYTHONUTF8=1` trước khi chạy script (PowerShell: `$env:PYTHONUTF8='1'`) để không lỗi chữ tiếng Việt.
- Cài thư viện bằng `<python> -m pip install ...`.

## Quy trình 8 bước, 3 điểm duyệt

Mỗi bước ghi kết quả thành file trong thư mục dự án, và cập nhật `PROGRESS.md` (mẫu `assets/templates/progress.md`) sau mỗi bước: đang ở bước nào, đã chốt gì, còn chờ gì. Nhờ vậy làm tiếp được ở phiên sau, và người khác đọc được. **[DUYỆT]** nghĩa là dừng lại, gửi kết quả, chờ người dùng đồng ý rồi mới đi tiếp.

| # | Bước | Đọc | File kết quả | Duyệt |
|---|---|---|---|---|
| 0 | Kiểm tra môi trường | `scripts/doctor.py` | (in ra màn hình) | — |
| 1 | Hỏi một lượt, viết brief | `references/01-intake.md` | `brief.md`, `PROGRESS.md` | — (duyệt chung ở bước 2) |
| 2 | Kịch bản, brief 5 dòng đặt ở đầu | gọi skill `ed-video-script` | `script.md`, `script-voice.txt`, `script-display.txt` | **[DUYỆT 1: brief + kịch bản]** |
| 3 | Giọng đọc → mốc từng từ | `references/voice-to-srt.md` | `audio/chXX.mp3`, `audio/*.words.json` | — |
| 4 | Shot list: chọn khung cảnh + điền nội dung | `references/04-shot-list.md` | `shot-list.md` | — |
| 5 | Pilot: dựng thật chương 1 (hoặc 30 giây đầu) | `references/05-pilot.md` | `renders/pilot.mp4` + `styleframes/*.png` | **[DUYỆT 2: hình + nhịp]** |
| 6 | Dựng các chương còn lại, qua cổng QC | `references/06-build.md`, `references/motion-rules.md`, `references/quality-standards.md` | `hf/`, `renders/chXX.mp4`, `build-log.md` | — |
| 7 | Review độc lập | gọi skill `ed-video-review` | `review/review-report.md` | — (phải đạt "Phải sửa = 0") |
| 8 | Hoàn thiện, xuất theo kênh, ghi bài học | `references/08-finalize.md` | `final/` + nhật ký Series Kit | **[DUYỆT 3: bản cuối]** |

Thư mục dự án: `04_projects/yymmdd_ten-video-khong-dau/`, ví dụ `261123_coffee-monday-tap-03/`.

**Vì sao chỉ 3 điểm duyệt:** người dùng là CBNV, không phải đạo diễn. Họ nhận xét tốt trên thứ nhìn được như thật (kịch bản, một đoạn video thật, bản cuối), nhưng khó nhận xét "nhịp" trên animatic khối màu. Brief được duyệt chung với kịch bản vì sai brief sẽ lộ ra ngay ở phần tóm tắt kịch bản.

**Chế độ Kỹ** (khi người dùng nói "chế độ kỹ", hoặc là người quản kit, hoặc làm tập đầu của series mới): thêm **[DUYỆT brief]** riêng sau bước 1, và **[DUYỆT style frames]** (4–6 ảnh tĩnh, xem `05-pilot.md` mục 1) trước khi dựng pilot. Tổng 5 điểm duyệt.

**Chuẩn chất lượng gốc:** `references/quality-standards.md` (bóc từ video mẫu M1): 5 nguyên tắc motion, spec cảnh 7 mục, bí kíp xem lại, 5 lỗi AI hay mắc. Đọc file này **trước bước 4** và áp dụng đến hết quy trình.

**Thứ tự vàng: giọng trước, hình sau.** Ngay khi kịch bản được duyệt, tạo hoặc lấy giọng đọc (bước 3). Mọi mốc thời gian của hình đều lấy từ giọng thật.

**Dựng từ khung cảnh có sẵn, không viết từ trang trắng.** Series Kit có thư mục `blocks/` (7 khung: title-card, big-number, three-points, compare, process-steps, key-message, cta-outro). Mỗi cảnh trong shot list chọn một khung rồi điền nội dung và mốc giây. Chỉ viết cảnh mới khi không khung nào phù hợp, và ghi rõ đó là loại cảnh mới (có thể đưa vào kit sau khi được duyệt).

### Nguyên tắc khi đi qua các bước
- **Không nhảy bước.** Không tạo giọng khi kịch bản chưa duyệt, không dựng các chương còn lại khi pilot chưa duyệt. Sửa ở bước sớm rẻ hơn rất nhiều.
- **Người dùng nói "làm luôn"**: vẫn giữ điểm duyệt **kịch bản** và **pilot**. Các điểm khác tự quyết và ghi giả định vào `brief.md`.
- **Hỏi phong cách trước khi viết**: với video chưa có Series Kit đã chốt, hỏi **phong cách (TH, P1–P6), font (F1–F8), giọng đọc, nhạc** rồi mới viết brief và kịch bản, kể cả khi yêu cầu chỉ có một câu. Không tự quyết thay bốn mục này.
- **Hỏi ít, hỏi đúng**: tối đa 3 câu một lượt (riêng lượt phong cách ở bước 1 gom thành một lượt chọn đáp án), ưu tiên câu hỏi chọn đáp án A/B/C. Series đã có kit thì không hỏi lại phần kỹ thuật (màu, giọng, nhạc).
- **Cho xem trên HyperFrames Studio**: mở màn hình xem trước ở điểm duyệt pilot và trước khi render bản cuối, không đợi người dùng hỏi (mục "Xem trước bằng HyperFrames Studio").
- **Nhạc nền giữ một mức** suốt video, không tự nhỏ đi khi có giọng đọc. Chỉ dùng kiểu tự hạ (`--duck`) khi người dùng yêu cầu.
- **Nói rõ thứ còn thiếu trước khi xin duyệt**: ví dụ người dùng chọn tự tải nhạc mà chưa gửi file thì nhắc ở pilot, và trước bản cuối đề xuất tạo nhạc AI. Không xin duyệt một bản thiếu thành phần mà không nói.
- **Phản biện**: input không ổn (nội dung quá nhiều cho 5 phút, ảnh mờ, giọng ồn, yêu cầu lệch Series Kit) thì nói thẳng, nêu lý do và đề xuất cách khác.
- **Một chương lỗi không dừng cả bài.** Giọng đọc lỗi ở chương nào thì thử lại chương đó (`tts_vi.py --only chXX`). Render lỗi ở chương nào thì sửa và render lại chương đó.
- **Tự sửa có giới hạn**: cổng QC hoặc review báo lỗi thì tự sửa tối đa **2 vòng**. Sau 2 vòng vẫn còn lỗi thì dừng, báo người dùng lỗi gì, ở đâu, đề xuất cách xử lý.
- **Làm tiếp dự án cũ**: đọc `PROGRESS.md` trước, rồi các file trong thư mục dự án. Giữ nguyên những quyết định đã duyệt.

## Xem trước bằng HyperFrames Studio
`<hf> preview <du-an>/hf` mở Studio (cổng mặc định 3002): phát cả video, kéo timeline, nghe âm thanh đã trộn.
- Ứng dụng Claude có khung trình duyệt: khai báo trong `.claude/launch.json` rồi mở bằng công cụ preview. Trên Windows dùng `"runtimeExecutable": "npx.cmd"`, `"runtimeArgs": ["-y", "hyperframes@0.9.84", "preview", "<đường dẫn tuyệt đối tới hf>", "--port=3002", "--no-open", "--foreground"]`. Công cụ báo không thấy `launch.json` thì tạo file ở đúng thư mục nó nêu.
- Đưa người dùng đường dẫn `http://localhost:3002`, cách phát, và cách ghi mốc giây cần sửa.
- Dự án sinh `hf/` bằng script: **dặn người dùng không sửa trong Studio**, vì lần dựng sau ghi đè. Muốn sửa thì sửa dữ liệu hoặc mã dựng.

## Chế độ gọi riêng: Voice → SRT

Khi người dùng chỉ cần phụ đề, ví dụ "chuyển file ghi âm này thành SRT" hay "làm phụ đề cho video workshop", thì đọc `references/voice-to-srt.md` và chỉ làm đúng việc đó.

## Giới hạn cần nói rõ với người dùng
- TTS có sẵn của HyperFrames **không có tiếng Việt**. Giọng tiếng Việt lấy từ file quay, file ghi âm, ElevenLabs, hoặc giọng AI qua `tts_vi.py` (edge-tts cần internet; giọng AI dùng tốt cho video nội bộ).
- Nhân vật dẫn chuyện chỉ dùng khi người dùng tự cung cấp.
- Một video 5 phút **render theo chương**. Sửa chương nào chỉ render lại chương đó.
- Logo: kit không kèm logo. Người dùng gửi file logo (PNG nền trong suốt hoặc SVG) một lần, lưu vào `03_series-kits/<series>/brand/`.
- Font DINRoundOT là font thương hiệu TH, chỉ dùng cho tài liệu nội bộ TH. Video ra ngoài thì chọn font khác trong F2–F8.
- Font ngoài danh sách F1–F8: kiểm đủ chữ có dấu tiếng Việt và giấy phép trước khi dùng (Lato, Bahnschrift đã bị loại vì thiếu chữ).

## Tài nguyên trong skill
- `CAI-DAT.md`: cài đặt cho máy mới, không cần quyền admin
- `CHANGELOG.md`: số bản và thay đổi từng bản
- `references/`: hướng dẫn chi tiết cho từng bước, `quality-standards.md` (chuẩn bóc từ video mẫu), `motion-rules.md`, `series-kit-spec.md`
- `assets/series-kits/th-default/`: Series Kit mặc định TH BlueGold, có `blocks/` (7 khung cảnh dựng sẵn) và `brand/` (chỗ đặt logo)
- `assets/series-kits/dark-studio/`: Series Kit **Dark Studio · Nắng sớm** (đã duyệt hình): `styleframes/`, nhạc, SFX, `engine/` (mã dựng theo dữ liệu + ví dụ video báo cáo)
- `assets/kit.lock.json`: phiên bản công cụ đã ghim (HyperFrames, GSAP, edge-tts)
- `assets/vendor/gsap.min.js`: GSAP chạy tại chỗ, không phụ thuộc CDN (mạng công ty hay chặn)
- `assets/templates/`: mẫu `brief.md`, `shot-list.md`, `progress.md`
- `assets/styles/`: **7 phong cách + 8 font** người dùng chọn khi bắt đầu (ảnh chọn trong `preview/`, `theme.css`, `tao_mau.py` để áp vào dự án)
- `assets/palettes.md`: mã màu của từng phong cách và cách làm bảng màu riêng
- `references/audio-sources.md`: 5 lựa chọn giọng, nhạc và SFX (AI tạo hoặc nguồn miễn phí)
- `scripts/tts_vi.py`: giọng AI tiếng Việt theo chương, có sẵn mốc từng từ
- `scripts/make_audio.py`: tự tạo nhạc nền (lặp liền mạch) + bộ SFX, không vướng bản quyền
- `scripts/to_srt.py`: transcript/VTT → SRT, căn chữ theo kịch bản
- `scripts/mix_audio.py`: trộn giọng + nhạc (giữ một mức; `--duck` để tự hạ khi có lời) + SFX thành một file
- `scripts/join_chapters.py`: ghép các chương không cần encode lại, thay audio
- `scripts/qc_probe.py`: kiểm tra kỹ thuật theo kênh phát (LMS, Zalo, Teams…)
- `scripts/doctor.py`: kiểm tra môi trường và phiên bản ghim, chỉ đưa cách sửa không cần quyền admin
