# Skill Library Check

[Tiếng Việt](./README.md) | [English](./README_EN.md) | [简体中文](./README_ZH-CN.md)

`Skillcheck` 是一个 Codex 技能，用于盘点已安装的技能、通过自适应问答澄清需求、为不同任务推荐合适的技能，并生成可直接使用的提示词。

本仓库包含适用于 Codex CLI 和 VS Code Codex 扩展的 Skillcheck 源代码。

## 核心功能

- 从本机实时扫描技能，而不是依赖预先记忆的列表。
- 发现 Personal、仓库、Codex system 以及已启用插件中的技能。
- 当需求不明确时，每次只询问一个问题，最多提出五个必要问题。
- 自动跳过用户已经提供的信息。
- 在推荐之前总结上下文并等待用户确认。
- 推荐主要技能、辅助技能，以及确有意义的替代方案。
- 根据目标、技术栈、当前状态、交付物、限制条件和验收标准生成提示词。
- 检测重复技能名称以及无效的 `SKILL.md` 元数据。
- 生成便于在 VS Code 中阅读的多页面 Markdown 仪表板。
- 生成可供其他工具读取的 `catalog.json`。

## 环境要求

- Codex CLI 或 VS Code 的 Codex 扩展。
- Python **3.11 或更高版本**。
- 使用 Git 克隆仓库时需要安装 Git。

扫描器仅使用 Python 标准库，无需执行 `pip install`。

检查环境：

```powershell
codex --version
python --version
git --version
```

## 安装

### Windows PowerShell

```powershell
git clone https://github.com/lythuachau/Skill-library-check.git

$source = Join-Path $PWD "Skill-library-check\skills\skillcheck"
$target = Join-Path $HOME ".agents\skills\skillcheck"

New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -Path "$source\*" -Destination $target -Recurse -Force
```

验证安装：

```powershell
Test-Path "$HOME\.agents\skills\skillcheck\SKILL.md"
```

正确结果应为：

```text
True
```

### macOS 或 Linux

```bash
git clone https://github.com/lythuachau/Skill-library-check.git
mkdir -p "$HOME/.agents/skills/skillcheck"
cp -R Skill-library-check/skills/skillcheck/. "$HOME/.agents/skills/skillcheck/"
test -f "$HOME/.agents/skills/skillcheck/SKILL.md" && echo "Skillcheck installed"
```

### 重新加载 VS Code

安装完成后：

1. 使用 `Ctrl+Shift+P` 打开命令面板。
2. 执行 **Developer: Reload Window**。
3. 新建一个 Codex 对话。
4. 输入 `$skillcheck`；如果 VS Code 显示多个选项，请选择 **Skillcheck – Personal**。

## 调用技能

### 推荐方式

输入 `$skillcheck`，从自动补全列表中选择技能，然后输入需求：

```text
$skillcheck 请推荐适合测试 React 结账流程的技能。
```

也可以先打开技能列表：

```text
/skills
```

然后选择 **Skillcheck** 并输入需求。

> `recommend` 不是一个子技能，它只是需求文本的一部分。例如：`$skillcheck recommend skills for testing a React checkout flow`。

## 使用模式

### 1. 需求不明确

```text
$skillcheck
```

Skillcheck 会逐个询问缺失信息：

1. 需要完成的目标。
2. 项目、功能和技术栈。
3. 当前实现状态或已观察到的问题。
4. 期望的交付物。
5. 限制条件和验收标准。

信息足够后，Skillcheck 会立即停止提问，总结需求，并等待用户回复 `确认`、`ok` 或提供修正内容。

对话示例：

```text
用户：$skillcheck
Skillcheck：你现在需要处理哪类工作？
用户：测试 React 结账流程。
Skillcheck：结账功能已经实现，还是正在开发？
用户：已经实现，但还没有测试。
Skillcheck：你需要单元测试、集成测试还是端到端测试？
用户：使用 Playwright 编写集成测试和 E2E 测试。
Skillcheck：[总结需求并等待确认]
用户：确认。
```

### 2. 需求已经明确

```text
$skillcheck 使用 Playwright 测试 React 结账流程，需要集成测试和 E2E 测试
```

Skillcheck 会使用现有信息，只补充询问那些会实质影响技能选择或最终提示词的关键内容。

### 3. 生成完整目录

```text
$skillcheck all
```

`all` 模式跳过问答并立即生成完整仪表板。

## 按任务分类的示例

### 需求澄清

```text
$skillcheck 我想添加 Google 登录，但用户流程和 MVP 范围还不明确。请选择能够澄清需求并生成 specification 的技能。
```

### 规划

```text
$skillcheck 推荐用于规划 Next.js 15 和 Supabase Google 登录功能的技能。计划必须列出受影响文件、migration、测试和完成标准。
```

### 测试与 TDD

```text
$skillcheck 选择适合严格 TDD 开发 React 购物车的技能。使用 Vitest 和 Testing Library，并在完成前运行 typecheck。
```

### 调试

```text
$skillcheck React Strict Mode 下订单 API 被调用两次。请选择采用根因分析、修改前要求证据并在修复后验证 regression 的调试技能。
```

### 代码审查

```text
$skillcheck 选择用于审查当前 diff 的技能。优先检查逻辑错误、安全问题、regression、性能和缺失测试，不要只关注细小样式问题。
```

### UI/UX

```text
$skillcheck 推荐用于设计 Next.js 和 Tailwind 响应式 SaaS 仪表板的技能。需要设计系统、accessibility 和组件规格。
```

### 安全

```text
$skillcheck 选择用于审查 FastAPI authentication 和 authorization 的技能。需要风险分级、证据、修复方案和验证步骤。
```

### 发布

```text
$skillcheck 推荐用于将 Docker 应用发布到 production 的技能。需要 quality gate、migration plan、rollback 和 smoke test。
```

## 生成的仪表板

默认情况下，Skillcheck 在当前仓库中生成报告：

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

### 文件说明

| 文件 | 内容 |
|---|---|
| `index.md` | 总览、快速路由，以及按来源和类别统计的数量 |
| 分类页面 | 需求、推荐技能、示例提示词和来源 |
| `all-skills.md` | 在一个表格中列出所有已发现技能 |
| `catalog.json` | 供脚本和其他工具使用的结构化数据 |

每个分类页面使用以下结构：

| 需求 / 能力 | 推荐技能 | 示例提示词 | 来源 |
|---|---|---|---|
| 来自实时元数据的简短说明 | 包含插件 namespace 的准确调用名称 | 可直接复制的提示词 | 简短来源标签 |

## 直接运行扫描器

Skillcheck 通常会在确认需求后自动运行扫描器，也可以手动运行。

### Windows PowerShell

```powershell
$scanner = "$HOME\.agents\skills\skillcheck\scripts\scan_skills.py"
python $scanner --dashboard-dir ".\.agents\skillcheck"
```

### macOS 或 Linux

```bash
python "$HOME/.agents/skills/skillcheck/scripts/scan_skills.py" \
  --dashboard-dir "./.agents/skillcheck"
```

### 按关键词筛选

```powershell
python $scanner --query "testing" --dashboard-dir ".\.agents\skillcheck"
python $scanner --query "React" --dashboard-dir ".\.agents\skillcheck"
```

### 按来源筛选

```powershell
python $scanner --source "Superpowers" --dashboard-dir ".\.agents\skillcheck"
python $scanner --source "ECC" --dashboard-dir ".\.agents\skillcheck"
```

### 按类别筛选

```powershell
python $scanner --category "Testing" --dashboard-dir ".\.agents\skillcheck"
python $scanner --category "UI/UX" --dashboard-dir ".\.agents\skillcheck"
```

### 导出 JSON

```powershell
python $scanner --format json --output ".\.agents\skillcheck-catalog.json"
```

`--query`、`--source` 和 `--category` 参数可以重复使用。

## 扫描的技能来源

| 来源 | 路径或发现方式 |
|---|---|
| Personal skills | `~/.agents/skills` |
| Codex user/system skills | `$CODEX_HOME/skills` 或 `~/.codex/skills` |
| Repository skills | 从工作目录到仓库根目录之间的 `.agents/skills` |
| Plugin skills | `codex plugin list --json` 返回的插件技能目录 |

插件 namespace 会被保留：

```text
$agent-skills:test-driven-development
$superpowers:test-driven-development
$ecc:security-review
```

这样可以区分名称相同但工作流不同的技能。

## Personal 与 Team 的区别

| 类型 | 作用范围 | 常见位置 |
|---|---|---|
| Personal | 当前用户的所有项目 | `~/.agents/skills/skillcheck` |
| Team | 单个仓库、workspace 或组织 | `<repository>/.agents/skills/skillcheck` 或组织管理的来源 |

为避免重复，只应在一个作用范围内安装活动技能。本仓库将源代码存放在 `skills/skillcheck`，而不是 `.agents/skills/skillcheck`，因此仅克隆仓库不会自动创建另一个 Team skill。

## 更新

进入已克隆的仓库：

```powershell
git pull

$source = Join-Path $PWD "skills\skillcheck"
$target = Join-Path $HOME ".agents\skills\skillcheck"
Copy-Item -Path "$source\*" -Destination $target -Recurse -Force
```

然后在 VS Code 中执行 **Developer: Reload Window**。

## 故障排除

### 找不到 Skillcheck

检查文件：

```powershell
Get-Item "$HOME\.agents\skills\skillcheck\SKILL.md"
```

然后：

1. 执行 **Developer: Reload Window**。
2. 新建一个 Codex 对话。
3. 输入 `$skillcheck` 或打开 `/skills`。
4. 确认 YAML frontmatter 包含 `name: skillcheck` 和 `description`。

### 同时出现 Personal 和 Team

查找所有副本：

```powershell
Get-ChildItem "$HOME\.agents\skills", ".\.agents\skills" -Filter SKILL.md -File -Recurse |
  Select-String -Pattern '^name:\s*skillcheck\s*$'
```

如果需要跨项目使用，请保留 Personal。若不希望仓库副本作为 Team skill 加载，请重命名它或将其移出 `.agents/skills`。

### `$skillcheck recommend` 没有显示为单独技能

这是正常行为。`$skillcheck` 是技能，`recommend` 是需求的一部分：

```text
$skillcheck recommend the right skills for testing a React checkout flow
```

请先从自动补全中选择 `$skillcheck`，再输入后续需求。

### 插件技能缺失

```powershell
codex plugin list --json
```

确认插件已经安装、启用，并且包含有效的技能目录。

### PowerShell 中的 Unicode 问题

```powershell
$env:PYTHONUTF8 = "1"
python "$HOME\.agents\skills\skillcheck\scripts\scan_skills.py" --dashboard-dir ".\.agents\skillcheck"
```

## 隐私说明

扫描器不会将技能内容发送到本仓库运营的独立服务。它会读取本地元数据，调用 `codex plugin list --json` 查找已启用插件，并将报告写入用户指定的输出目录。

`catalog.json` 可能包含本机绝对路径。在提交或公开分享前请先检查该文件。

## 源代码结构

```text
skills/skillcheck/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── scan_skills.py
```

- `SKILL.md`：问答、确认、路由和结果展示行为。
- `agents/openai.yaml`：界面显示名称、简短说明和默认提示词。
- `scripts/scan_skills.py`：技能发现、分类、重复检测和仪表板生成。

## 验证贡献内容

```powershell
python -m py_compile ".\skills\skillcheck\scripts\scan_skills.py"
python ".\skills\skillcheck\scripts\scan_skills.py" --format json --query "skillcheck"
git diff --check
```

推荐的贡献流程：

1. Fork 本仓库。
2. 为修改创建新分支。
3. 更新技能或扫描器。
4. 执行上述验证命令。
5. 创建 pull request，并说明修改前后的行为。

## 仓库链接

- GitHub：<https://github.com/lythuachau/Skill-library-check>
- 技能源代码：[`skills/skillcheck`](./skills/skillcheck)
- Issue tracker：<https://github.com/lythuachau/Skill-library-check/issues>
