# Ví dụ hoàn chỉnh: Báo cáo đào tạo (bản đã được duyệt hình, 26/11/2026)

Video 4:35, 13 chương, 16:9. Toàn bộ số liệu trong `du-lieu.txt` là **giả lập**.

| File | Vai trò |
|---|---|
| `du-lieu.txt` | Nơi duy nhất người dùng sửa số và chữ ngắn (`*_nhan`) |
| `gen_script.py` | `du-lieu.txt` → `script*.md/txt` + `data.json`; báo lỗi khi số không khớp |
| `build.py` | Intro, CH01–CH03, lắp ráp `hf/` và `timing.json` |
| `scenes_p12.py`, `scenes_p3.py`, `scenes_p4.py` | Cảnh CH04–CH13 và outro: mẫu để chép ý tưởng cảnh |
| `dung_lai.py`, `dung-lai.bat` | Chạy cả chuỗi: số liệu → giọng chương đổi → dựng → trộn → kiểm tra → render → phụ đề |

## Dùng lại cho dự án mới
1. `<hf> init hf --non-interactive` trong thư mục dự án.
2. Chép từ kit: `fonts/` → `hf/assets/fonts/`; `gsap.min.js` của skill → `hf/assets/vendor/`; `audio/theme.mp3` và `audio/sfx/` → `audio/`.
3. Chép `engine/*.py` và các file ví dụ vào thư mục dự án, rồi viết lại `du-lieu.txt`, `gen_script.py` và các cảnh theo nội dung mới.
4. Tạo `audio/voice-settings.json`: `{"voice": "vi-VN-HoaiMyNeural", "rate": "+12%"}`.
5. Sau lần tạo giọng đầu: `py -3 dung_lai.py --ghi-moc`. Từ đó dùng `dung-lai.bat`.

Các cảnh vẽ theo **chủ đề hiện có** (AI, an toàn, sản xuất…). Đổi số và chữ ngắn thì hình tự theo; đổi chủ đề thì phải viết lại cảnh.

Ở bản gốc, `check`, `render` và phụ đề được chạy bằng lệnh rời; trong `dung_lai.py`, đoạn render → phụ đề → `qc_probe` chưa được chạy thử.
