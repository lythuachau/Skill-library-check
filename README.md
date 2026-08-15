# Skill Library Check

`Skillcheck` là một Codex skill giúp kiểm kê các skill đang có, làm rõ nhu cầu bằng Q&A thích ứng, đề xuất đúng skill cho từng công việc và tạo prompt có thể sử dụng ngay.

Repository này chứa mã nguồn của Skillcheck để cài đặt cho Codex CLI và Codex trong VS Code.

## Tính năng chính

- Quét danh sách skill trực tiếp từ máy thay vì dùng danh sách ghi nhớ.
- Phát hiện skill ở phạm vi Personal, repository, Codex system và plugin đã bật.
- Hỏi từng câu khi yêu cầu còn mơ hồ, tối đa năm câu hỏi cần thiết.
- Bỏ qua những thông tin người dùng đã cung cấp.
- Tóm tắt bối cảnh và chờ xác nhận trước khi đề xuất.
- Đề xuất skill chính, skill bổ trợ và lựa chọn thay thế khi cần.
- Tạo prompt theo đúng mục tiêu, stack, trạng thái, đầu ra và tiêu chí xác minh.
- Phát hiện tên skill trùng và lỗi metadata trong `SKILL.md`.
- Xuất dashboard Markdown nhiều trang, dễ mở trong VS Code.
- Xuất `catalog.json` để công cụ khác có thể xử lý.

## Yêu cầu

- Codex CLI hoặc Codex extension cho VS Code.
- Python **3.11 trở lên**.
- Git, nếu cài đặt bằng cách clone repository.

Scanner chỉ sử dụng Python standard library, không cần chạy `pip install`.

Kiểm tra môi trường:

```powershell
codex --version
python --version
git --version
```

## Cài đặt

### Windows PowerShell

```powershell
git clone https://github.com/lythuachau/Skill-library-check.git

$source = Join-Path $PWD "Skill-library-check\skills\skillcheck"
$target = Join-Path $HOME ".agents\skills\skillcheck"

New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -Path "$source\*" -Destination $target -Recurse -Force
```

Kiểm tra:

```powershell
Test-Path "$HOME\.agents\skills\skillcheck\SKILL.md"
```

Kết quả phải là:

```text
True
```

### macOS hoặc Linux

```bash
git clone https://github.com/lythuachau/Skill-library-check.git
mkdir -p "$HOME/.agents/skills/skillcheck"
cp -R Skill-library-check/skills/skillcheck/. "$HOME/.agents/skills/skillcheck/"
test -f "$HOME/.agents/skills/skillcheck/SKILL.md" && echo "Skillcheck installed"
```

### Làm mới VS Code

Sau khi cài đặt:

1. Mở Command Palette bằng `Ctrl+Shift+P`.
2. Chạy **Developer: Reload Window**.
3. Mở một cuộc trò chuyện Codex mới.
4. Gõ `$skillcheck` và chọn **Skillcheck – Personal** nếu VS Code hiển thị danh sách lựa chọn.

## Cách gọi skill

### Cách được khuyến nghị

Gõ `$skillcheck`, chọn skill trong danh sách gợi ý, sau đó viết yêu cầu:

```text
$skillcheck Hãy đề xuất skill phù hợp để kiểm thử luồng checkout React.
```

Bạn cũng có thể mở danh sách skill trước:

```text
/skills
```

Sau đó chọn **Skillcheck** và nhập yêu cầu.

> `recommend` không phải một skill con. Đây chỉ là nội dung yêu cầu. Ví dụ đúng là `$skillcheck recommend skill cho testing React checkout`.

## Các chế độ sử dụng

### 1. Yêu cầu còn mơ hồ

```text
$skillcheck
```

Skillcheck sẽ hỏi từng câu để thu thập những thông tin còn thiếu:

1. Mục tiêu cần thực hiện.
2. Dự án, tính năng và technology stack.
3. Trạng thái hiện tại hoặc lỗi đang gặp.
4. Đầu ra mong muốn.
5. Ràng buộc và cách xác minh.

Skillcheck dừng hỏi ngay khi đã đủ dữ liệu, tóm tắt yêu cầu và chờ người dùng xác nhận bằng `duyệt`, `ok`, `đúng` hoặc nội dung sửa đổi.

Ví dụ hội thoại:

```text
Người dùng: $skillcheck
Skillcheck: Bạn muốn xử lý hạng mục nào?
Người dùng: Testing luồng checkout React.
Skillcheck: Checkout hiện đã có implementation hay đang được xây mới?
Người dùng: Đã có implementation nhưng chưa có test.
Skillcheck: Bạn cần unit test, integration test hay cả E2E?
Người dùng: Integration và E2E bằng Playwright.
Skillcheck: [Tóm tắt yêu cầu và chờ xác nhận]
Người dùng: Duyệt.
```

### 2. Yêu cầu đã rõ

```text
$skillcheck testing React checkout bằng Playwright, cần integration test và E2E
```

Skillcheck sử dụng thông tin đã có và chỉ hỏi thêm dữ liệu thật sự ảnh hưởng đến lựa chọn skill hoặc prompt.

### 3. Tạo toàn bộ danh mục

```text
$skillcheck all
```

Chế độ `all` bỏ qua Q&A và tạo dashboard đầy đủ ngay lập tức.

## Ví dụ theo nhu cầu

### Làm rõ yêu cầu

```text
$skillcheck Tôi có ý tưởng thêm đăng nhập Google nhưng chưa rõ luồng người dùng và phạm vi MVP. Hãy chọn skill để làm rõ yêu cầu và tạo specification.
```

### Lập kế hoạch

```text
$skillcheck Recommend skill để lập kế hoạch thêm đăng nhập Google vào Next.js 15 và Supabase. Kế hoạch phải nêu file ảnh hưởng, migration, test và tiêu chí hoàn thành.
```

### Testing và TDD

```text
$skillcheck Chọn skill để triển khai giỏ hàng React theo TDD nghiêm ngặt. Dùng Vitest, Testing Library và phải chạy typecheck sau khi hoàn thành.
```

### Debug

```text
$skillcheck API tạo đơn hàng đang bị gọi hai lần trong React Strict Mode. Hãy chọn skill debug theo root-cause, yêu cầu bằng chứng trước khi sửa và xác minh regression.
```

### Code review

```text
$skillcheck Chọn skill để review diff hiện tại. Ưu tiên bug logic, security, regression, hiệu năng và test còn thiếu; không tập trung vào style nhỏ.
```

### UI/UX

```text
$skillcheck Recommend skill để thiết kế dashboard SaaS responsive bằng Next.js và Tailwind. Cần design system, accessibility và component specification.
```

### Bảo mật

```text
$skillcheck Chọn skill để review authentication và authorization của FastAPI. Cần xếp hạng rủi ro, bằng chứng, bản sửa và bước xác minh.
```

### Phát hành

```text
$skillcheck Recommend skill để chuẩn bị release ứng dụng Docker lên production. Cần quality gate, migration plan, rollback và smoke test.
```

## Dashboard được tạo

Mặc định Skillcheck tạo báo cáo trong repository đang mở:

```text
<repository>/.agents/skillcheck/
├── index.md
├── planning.md
├── testing.md
├── debugging.md
├── review-quality.md
├── security.md
├── ui-ux.md
├── performance.md
├── backend-data.md
├── devops-release.md
├── agents-automation.md
├── docs-research.md
├── marketing-growth.md
├── media-creative.md
├── other.md
├── all-skills.md
└── catalog.json
```

### Vai trò của từng file

| File | Nội dung |
|---|---|
| `index.md` | Tổng quan, điều hướng nhanh, số lượng theo nguồn và hạng mục |
| Các trang hạng mục | Bảng nhu cầu, skill đề xuất, prompt ví dụ và nguồn |
| `all-skills.md` | Toàn bộ skill trong một bảng duy nhất |
| `catalog.json` | Dữ liệu có cấu trúc dành cho script hoặc công cụ khác |

Mỗi trang hạng mục sử dụng cấu trúc:

| Nhu cầu / chức năng | Skill đề xuất | Prompt ví dụ | Nguồn |
|---|---|---|---|
| Mô tả ngắn từ metadata thật | Tên gọi chính xác, gồm namespace plugin | Prompt có thể sao chép | Nguồn rút gọn |

## Chạy scanner trực tiếp

Skillcheck thường tự chạy scanner sau bước xác nhận. Bạn cũng có thể chạy thủ công.

### Windows PowerShell

```powershell
$scanner = "$HOME\.agents\skills\skillcheck\scripts\scan_skills.py"
python $scanner --dashboard-dir ".\.agents\skillcheck"
```

### macOS hoặc Linux

```bash
python "$HOME/.agents/skills/skillcheck/scripts/scan_skills.py" \
  --dashboard-dir "./.agents/skillcheck"
```

### Lọc theo từ khóa

```powershell
python $scanner --query "testing" --dashboard-dir ".\.agents\skillcheck"
python $scanner --query "React" --dashboard-dir ".\.agents\skillcheck"
```

### Lọc theo nguồn

```powershell
python $scanner --source "Superpowers" --dashboard-dir ".\.agents\skillcheck"
python $scanner --source "ECC" --dashboard-dir ".\.agents\skillcheck"
```

### Lọc theo hạng mục

```powershell
python $scanner --category "Testing" --dashboard-dir ".\.agents\skillcheck"
python $scanner --category "UI/UX" --dashboard-dir ".\.agents\skillcheck"
```

### Xuất JSON

```powershell
python $scanner --format json --output ".\.agents\skillcheck-catalog.json"
```

Các tùy chọn `--query`, `--source` và `--category` có thể được lặp lại.

## Nguồn skill được quét

Scanner tìm skill từ những nguồn sau:

| Nguồn | Vị trí hoặc cách phát hiện |
|---|---|
| Personal skills | `~/.agents/skills` |
| Codex user/system skills | `$CODEX_HOME/skills` hoặc `~/.codex/skills` |
| Repository skills | `.agents/skills` từ working directory đến repository root |
| Plugin skills | Skill roots của plugin được trả về bởi `codex plugin list --json` |

Plugin namespace được giữ nguyên. Ví dụ:

```text
$agent-skills:test-driven-development
$superpowers:test-driven-development
$ecc:security-review
```

Điều này giúp phân biệt các skill trùng tên nhưng có workflow khác nhau.

## Personal và Team khác nhau thế nào?

| Loại | Phạm vi | Vị trí thường gặp |
|---|---|---|
| Personal | Dùng trong mọi dự án của người dùng hiện tại | `~/.agents/skills/skillcheck` |
| Team | Dùng trong một repository, workspace hoặc tổ chức | `<repository>/.agents/skills/skillcheck` hoặc nguồn do tổ chức cung cấp |

Để tránh xuất hiện hai mục Skillcheck giống nhau, chỉ cài bản hoạt động tại một phạm vi. Repository này lưu mã nguồn ở `skills/skillcheck`, không phải `.agents/skills/skillcheck`, nên clone repository sẽ không tự tạo thêm bản Team.

## Cập nhật

Trong thư mục đã clone:

```powershell
git pull

$source = Join-Path $PWD "skills\skillcheck"
$target = Join-Path $HOME ".agents\skills\skillcheck"
Copy-Item -Path "$source\*" -Destination $target -Recurse -Force
```

Sau đó chạy **Developer: Reload Window** trong VS Code.

## Xử lý sự cố

### Không thấy Skillcheck

Kiểm tra file:

```powershell
Get-Item "$HOME\.agents\skills\skillcheck\SKILL.md"
```

Sau đó:

1. Chạy **Developer: Reload Window**.
2. Mở cuộc trò chuyện Codex mới.
3. Gõ `$skillcheck` hoặc mở `/skills`.
4. Kiểm tra YAML frontmatter có `name: skillcheck` và `description`.

### Có cả Skillcheck Personal và Team

Tìm các bản đang tồn tại:

```powershell
Get-ChildItem "$HOME\.agents\skills", ".\.agents\skills" -Filter SKILL.md -File -Recurse |
  Select-String -Pattern '^name:\s*skillcheck\s*$'
```

Giữ bản Personal nếu muốn dùng trong mọi dự án. Đổi tên hoặc chuyển bản repository ra ngoài `.agents/skills` nếu không muốn Codex nạp nó như Team skill.

### `$skillcheck recommend` không xuất hiện như một skill riêng

Đây là hành vi đúng. Chỉ có skill `$skillcheck`; `recommend` là nội dung yêu cầu:

```text
$skillcheck recommend skill phù hợp cho testing React checkout
```

Hãy chọn `$skillcheck` từ autocomplete trước rồi nhập phần yêu cầu.

### Plugin skills không xuất hiện

Kiểm tra plugin:

```powershell
codex plugin list --json
```

Đảm bảo plugin đã được cài, bật và có thư mục skill hợp lệ.

### Lỗi Unicode trong PowerShell

```powershell
$env:PYTHONUTF8 = "1"
python "$HOME\.agents\skills\skillcheck\scripts\scan_skills.py" --dashboard-dir ".\.agents\skillcheck"
```

## Quyền riêng tư

Scanner không gửi nội dung skill lên dịch vụ riêng của repository này. Nó đọc metadata cục bộ, gọi `codex plugin list --json` để tìm plugin đã bật và ghi báo cáo vào thư mục đầu ra do người dùng chọn.

`catalog.json` có thể chứa đường dẫn tuyệt đối trên máy. Hãy kiểm tra file trước khi commit hoặc chia sẻ công khai.

## Cấu trúc mã nguồn

```text
skills/skillcheck/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── scan_skills.py
```

- `SKILL.md`: hành vi Q&A, xác nhận, routing và cách trình bày kết quả.
- `agents/openai.yaml`: tên hiển thị, mô tả ngắn và prompt mặc định trong giao diện.
- `scripts/scan_skills.py`: discovery, phân loại, phát hiện trùng và tạo dashboard.

## Kiểm tra thay đổi khi đóng góp

```powershell
python -m py_compile ".\skills\skillcheck\scripts\scan_skills.py"
python ".\skills\skillcheck\scripts\scan_skills.py" --format json --query "skillcheck"
git diff --check
```

Quy trình đề xuất:

1. Fork repository.
2. Tạo branch cho thay đổi.
3. Cập nhật skill hoặc scanner.
4. Chạy các lệnh kiểm tra phía trên.
5. Tạo pull request và mô tả hành vi trước/sau.

## Repository

- GitHub: <https://github.com/lythuachau/Skill-library-check>
- Skill source: [`skills/skillcheck`](./skills/skillcheck)
- Issue tracker: <https://github.com/lythuachau/Skill-library-check/issues>
