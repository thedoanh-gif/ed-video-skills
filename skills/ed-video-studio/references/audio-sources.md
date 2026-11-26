# Giọng đọc, nhạc nền, SFX: nguồn và cách làm

Chọn ở bước Input, rồi ghi vào Series Kit để mọi tập dùng giống nhau.

## 1. Giọng đọc (hỏi người dùng ngay từ đầu)
| Lựa chọn | Cách làm | Mốc từng từ | Lưu ý |
|---|---|---|---|
| **A. Giọng trong file quay** | Tách tiếng từ video gốc | `<hf> transcribe` → `to_srt.py` | Lọc ồn theo bộ lọc trong Series Kit |
| **B. File ghi âm riêng** | Người dùng gửi file (mỗi chương một file thì càng tốt) | transcribe → `to_srt.py --script script-display.txt` | Cùng một người đọc, cùng micro cho cả series |
| **C. ElevenLabs** | Agent soạn `script-voice.txt` + thông số. Người dùng tạo giọng rồi gửi file | transcribe → `to_srt.py --script` | Cố định voice ID + thông số trong Series Kit |
| **D. Giọng AI do agent tạo** | `scripts/tts_vi.py` (mặc định edge-tts, giọng neural tiếng Việt) | **Có sẵn** (`chXX.words.json`) | Xem ghi chú bên dưới |
| **E. Không lời** | Chỉ nhạc + chữ | — | Chữ trên màn hình phải tự kể được câu chuyện |

**Ghi chú về D (giọng AI):**
- `edge-tts`: `<python> -m pip install edge-tts`. Giọng `vi-VN-HoaiMyNeural` (nữ) hoặc `vi-VN-NamMinhNeural` (nam). Tự nhiên, miễn phí, **cần internet**. Đây là cách dùng không chính thức dịch vụ đọc của Microsoft Edge. Phù hợp cho bản nháp và video nội bộ. Video quan trọng nên dùng ElevenLabs hoặc người thật.
- Không có mạng: `--engine piper` (Piper, mã nguồn mở, chạy offline, có giọng vi_VN). Kém tự nhiên hơn, không có mốc từng từ.
- Một chương lỗi thì các chương khác vẫn chạy tiếp; chạy lại riêng chương lỗi bằng `--only ch02`. Chỉnh tốc độ bằng `--rate` (mặc định `+12%`) để đạt 170–190 từ/phút. Ghi `voice/rate/pitch` vào Series Kit.
- HyperFrames TTS (Kokoro) **không có tiếng Việt**. Không dùng cho lời tiếng Việt.

## 2. Nhạc nền (người dùng chọn)
**a) AI tạo bằng code (mặc định, không vướng bản quyền):**
```bash
<python> <skill>/scripts/make_audio.py music --out audio/theme.wav --mood calm|bright|focus --bpm 100 --seconds 90 --seed 7
```
- `calm`: nhẹ, ấm (chính sách, văn hóa) · `bright`: tươi, vui (truyền thông, sự kiện) · `focus`: tập trung (hướng dẫn, kỹ năng)
- Cùng mood + bpm + seed thì ra cùng một bản → ghi vào Series Kit để các tập dùng chung. Bản nhạc lặp liền mạch, có thể nối dài cho đủ video.

**b) Tải từ nguồn miễn phí** (người dùng tự tải hoặc agent hướng dẫn):
| Nguồn | Giấy phép | Ghi chú |
|---|---|---|
| Pixabay Music | Pixabay Content License: dùng miễn phí, không bắt buộc ghi nguồn | Kiểm tra lại điều khoản trên trang trước khi dùng |
| YouTube Audio Library | Miễn phí. Một số bản yêu cầu ghi nguồn | Xem cột "Attribution" |
| Free Music Archive | Tùy bản (CC0, CC-BY…) | **Chỉ chọn CC0 hoặc CC-BY** (ghi nguồn), tránh NC/ND nếu không chắc |
| Mixkit | Mixkit License (miễn phí) | |
Khi tải về: ghi tên bài, tác giả, link, giấy phép vào `credits.txt` của dự án và Series Kit.
**Không dùng** nhạc thương mại, nhạc trên TikTok/Spotify, nhạc phim.

## 3. SFX
**a) AI tạo bằng code:** `<python> <skill>/scripts/make_audio.py sfx --out audio/sfx/` sinh ra whoosh, pop, tick, chime, stamp, swipe, click.
**b) Nguồn miễn phí:** Pixabay Sound Effects · Mixkit SFX · Freesound (**lọc giấy phép CC0**; bản CC-BY thì phải ghi nguồn) · YouTube Audio Library.
Giữ **một bộ SFX cố định** cho cả series (lưu trong `03_series-kits/<series>/audio/sfx/`). Mỗi chương tối đa 3–5 SFX.

## 4. Mix (nhắc lại)
Giọng -16 LUFS · nhạc **giữ một mức suốt video**, khoảng -36 LUFS (thấp hơn giọng ~20 dB), không tự hạ khi có lời · vào nhẹ ở đầu, nhỏ dần ở cuối · true peak ≤ -1 dBTP. `mix_audio.py` tự đo bản nhạc và đặt một mức cố định; chỉnh bằng `--music-lufs` (-33 to hơn, -39 nhỏ hơn); `--duck` chỉ khi người dùng yêu cầu.
