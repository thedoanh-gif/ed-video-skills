# Cài đặt ED_Video Studio (Windows, không cần quyền admin)

Làm một lần cho mỗi máy. Cần Claude Code đã cài và đăng nhập, mạng internet, khoảng 3–5 GB trống.

Phiên bản công cụ đã chạy thật nằm trong `assets/kit.lock.json`.

## 1. Chép skill
Chạy trong PowerShell, tại thư mục repo vừa tải về:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null; Copy-Item -Recurse -Force .\skills\ed-video-* "$env:USERPROFILE\.claude\skills\"
```

## 2. Cài công cụ nền

| Công cụ | Cách cài không cần admin |
|---|---|
| Python 3.10 trở lên | Bộ cài từ python.org, chọn "Install for me only", bỏ chọn "Use admin privileges", chọn "Add python.exe to PATH" |
| Node.js 22 trở lên | Tải bản `.zip` LTS (Windows x64) từ nodejs.org, giải nén vào `%LOCALAPPDATA%\Programs\nodejs`, thêm thư mục đó vào PATH người dùng |
| FFmpeg | Tải `ffmpeg-release-essentials.zip` từ gyan.dev, giải nén vào `%LOCALAPPDATA%\Programs\ffmpeg`, thêm thư mục `bin` vào PATH người dùng |

Thêm vào PATH người dùng: mở Start, gõ "environment variables", chọn "Edit environment variables for your account", sửa biến `Path`.

## 3. Thư viện Python và biến môi trường

```powershell
py -3 -m pip install --user edge-tts==7.3.1 pillow numpy
```

Tắt gửi dữ liệu sử dụng của HyperFrames và tránh lỗi chữ tiếng Việt:

```powershell
setx HYPERFRAMES_NO_TELEMETRY 1
```

```powershell
setx DO_NOT_TRACK 1
```

```powershell
setx PYTHONUTF8 1
```

Đóng rồi mở lại terminal để các biến có hiệu lực.

## 4. Skill của HyperFrames
`ed-video-studio` cần skill `/hyperframes`:

```powershell
npx -y hyperframes@0.9.84 skills
```

## 5. Font DINRoundOT
Repo không kèm font DINRoundOT. Xin người quản kit 8 file sau từ nguồn được phép dùng:

`DINROUNDOT-LIGHT.otf`, `-LIGHTITALIC`, `-REGULAR`, `-ITALIC`, `-MEDIUM`, `-MEDIUMITALIC`, `-BOLD`, `-BOLDITALIC`

Chép vào cả hai thư mục:

- `%USERPROFILE%\.claude\skills\ed-video-studio\assets\series-kits\th-default\fonts\`
- `%USERPROFILE%\.claude\skills\ed-video-studio\assets\series-kits\dark-studio\fonts\`

Series riêng trong `TH-Video\03_series-kits\<series>\fonts\` cũng cần đủ font. Thiếu font thì skill dừng lại báo, không tự thay font khác ở bản cuối.

Người dùng không có DINRoundOT thì chọn font khác (F2–F8) trong `assets/styles/`.

## 6. Tạo thư mục làm việc

```text
TH-Video/
  01_library/          video mẫu + transcript (.vtt)
  02_style-bible/      STYLE-BIBLE.md
  03_series-kits/      mỗi series một thư mục
  04_projects/         mỗi video một thư mục
```

## 7. Kiểm tra

```powershell
py -3 "$env:USERPROFILE\.claude\skills\ed-video-studio\scripts\doctor.py" --fix --full
```

`--fix` tự cài thư viện Python còn thiếu. Sau này mỗi lần làm video, skill tự chạy bước kiểm tra này và tự cài phần thiếu; thiếu Python, Node hoặc FFmpeg thì Claude hỏi bạn trước khi tải.

Kết luận **SẴN SÀNG** là dùng được. Còn lỗi thì làm theo dòng `→` dưới mỗi lỗi, hoặc dán kết quả cho Claude và nhờ sửa. Lần đầu chạy `--full` mất vài phút vì phải tải HyperFrames và Chrome để render.

## Khi dùng lần đầu
Nhận dạng giọng nói (làm phụ đề từ file ghi âm) sẽ tải model khoảng 1,5–3 GB.
