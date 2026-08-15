from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tomllib
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


NAME_CATEGORY_RULES = [
    ("Hiệu năng & tối ưu", ("performance", "latency", "throughput", "optimizer", "optimization", "webperf")),
    ("Bảo mật & tuân thủ", ("security", "secure", "hardening", "vulnerability", "threat", "compliance", "hipaa", "safety", "gateguard")),
    ("Testing, QA & đánh giá", ("test", "testing", "tdd", "qa", "verification", "eval", "benchmark", "canary")),
    ("Debug & phục hồi lỗi", ("debug", "debugging", "troubleshoot", "error", "recovery", "diagnostic", "build fix", "fix defect")),
    ("Lập kế hoạch & yêu cầu", ("plan", "plans", "planning", "spec", "brainstorming", "interview", "idea", "requirement", "blueprint", "product lens", "intent driven")),
    ("Backend, API & dữ liệu", ("backend", "api", "database", "postgres", "mysql", "redis", "django", "fastapi", "springboot", "laravel", "nestjs", "data", "migration", "prisma", "clickhouse")),
    ("UI/UX & frontend", ("ui", "ux", "frontend", "design", "accessibility", "a11y", "react", "vue", "angular", "svelte", "tailwind", "motion", "swiftui")),
    ("DevOps, Git & phát hành", ("git", "deploy", "deployment", "docker", "kubernetes", "ci cd", "shipping", "release", "worktree", "terminal", "cloud", "launch", "branch")),
    ("Review, chất lượng & refactor", ("review", "quality", "refactor", "simplification", "codehealth", "audit", "coding standards", "plankton")),
    ("Tài liệu & nghiên cứu", ("document", "article", "research", "documentation", "docs", "knowledge", "literature", "source driven")),
    ("Agent, skill & tự động hóa", ("agent", "harness", "autonomous", "orchestration", "parallel", "mcp", "skill", "skillcheck", "workflow", "automation", "ecc", "council")),
    ("Marketing & tăng trưởng", ("marketing", "seo", "advertising", "copywriting", "content", "social", "sales", "growth", "campaign", "brand")),
    ("Media & sáng tạo", ("image", "video", "slides", "portrait", "animation", "creative", "remotion", "blender")),
]

DESCRIPTION_CATEGORY_RULES = [
    ("Hiệu năng & tối ưu", ("performance optimization", "core web vitals", "performance regression", "profiling reveals bottlenecks")),
    ("Bảo mật & tuân thủ", ("security checklist", "security review", "owasp", "vulnerability", "threat model", "regulatory compliance")),
    ("Testing, QA & đánh giá", ("test-driven development", "red-green-refactor", "end-to-end testing", "quality gate", "test failure")),
    ("Debug & phục hồi lỗi", ("root cause", "unexpected behavior", "error recovery", "diagnostic workflow", "debugging")),
    ("Lập kế hoạch & yêu cầu", ("requirements are unclear", "implementation plan", "break work into", "before touching code", "design dialogue")),
    ("UI/UX & frontend", ("user-facing ui", "responsive layout", "design system", "typography", "interface design", "frontend")),
    ("Backend, API & dữ liệu", ("rest api", "database schema", "backend", "data migration", "orm")),
    ("DevOps, Git & phát hành", ("deploy to production", "rollback strategy", "docker compose", "continuous integration", "git workflow")),
    ("Review, chất lượng & refactor", ("code review", "code quality", "maintainability", "refactor")),
    ("Tài liệu & nghiên cứu", ("cited reports", "source attribution", "documentation workflow", "literature review")),
    ("Agent, skill & tự động hóa", ("coding agent", "agent workflow", "skill catalog", "multi-agent", "mcp server")),
    ("Marketing & tăng trưởng", ("marketing campaign", "conversion", "seo", "brand voice")),
    ("Media & sáng tạo", ("image generation", "video creation", "presentation slides")),
]

CATEGORY_PROMPTS = {
    "Bảo mật & tuân thủ": "Hãy dùng {skill} để kiểm tra luồng đăng nhập và phân quyền hiện tại; xếp hạng rủi ro, chỉ ra bằng chứng và đề xuất bản sửa có thể xác minh.",
    "Testing, QA & đánh giá": "Hãy dùng {skill} để xây dựng và chạy chiến lược kiểm thử cho luồng thanh toán; báo cáo test pass/fail, độ bao phủ và phần còn thiếu.",
    "Debug & phục hồi lỗi": "Hãy dùng {skill} để tìm nguyên nhân API bị gọi hai lần; thu thập bằng chứng, sửa tối thiểu và xác minh lỗi không tái diễn.",
    "Review, chất lượng & refactor": "Hãy dùng {skill} để review thay đổi hiện tại; ưu tiên lỗi logic, regression, khả năng bảo trì và test còn thiếu.",
    "Lập kế hoạch & yêu cầu": "Hãy dùng {skill} để lập kế hoạch thêm đăng nhập Google; nêu file ảnh hưởng, bước triển khai, rủi ro và tiêu chí hoàn thành.",
    "UI/UX & frontend": "Hãy dùng {skill} để thiết kế và review dashboard SaaS responsive; nêu layout, màu sắc, typography, accessibility và cách triển khai.",
    "Backend, API & dữ liệu": "Hãy dùng {skill} để thiết kế API tạo đơn hàng; nêu interface, validation, lỗi, dữ liệu và ví dụ triển khai phù hợp dự án.",
    "DevOps, Git & phát hành": "Hãy dùng {skill} để chuẩn bị phát hành phiên bản hiện tại; chạy các quality gate, lập kế hoạch rollback và xác minh sau triển khai.",
    "Tài liệu & nghiên cứu": "Hãy dùng {skill} để nghiên cứu chủ đề đang triển khai, tổng hợp nguồn và tạo hướng dẫn ngắn gọn có thể áp dụng cho repository này.",
    "Agent, skill & tự động hóa": "Hãy dùng {skill} để thiết kế workflow agent cho tác vụ hiện tại; nêu trigger, các bước, công cụ, checkpoint và điều kiện hoàn thành.",
    "Marketing & tăng trưởng": "Hãy dùng {skill} để xây dựng kế hoạch tăng trưởng cho sản phẩm SaaS; xác định đối tượng, thông điệp, kênh và chỉ số đo lường.",
    "Media & sáng tạo": "Hãy dùng {skill} để tạo nội dung hình ảnh hoặc video cho tính năng mới; nêu bố cục, phong cách, đầu ra và tiêu chí kiểm tra.",
    "Hiệu năng & tối ưu": "Hãy dùng {skill} để đo hiệu năng của ứng dụng hiện tại, xác định nút thắt bằng dữ liệu, tối ưu thay đổi có tác động cao và đo lại kết quả.",
    "Khác": "Hãy dùng {skill} để xử lý hạng mục phù hợp trong dự án hiện tại; phân tích bối cảnh, thực hiện từng bước và xác minh kết quả.",
}

CATEGORY_SLUGS = {
    "Lập kế hoạch & yêu cầu": "planning.md",
    "Testing, QA & đánh giá": "testing.md",
    "Debug & phục hồi lỗi": "debugging.md",
    "Review, chất lượng & refactor": "review-quality.md",
    "Bảo mật & tuân thủ": "security.md",
    "UI/UX & frontend": "ui-ux.md",
    "Hiệu năng & tối ưu": "performance.md",
    "Backend, API & dữ liệu": "backend-data.md",
    "DevOps, Git & phát hành": "devops-release.md",
    "Agent, skill & tự động hóa": "agents-automation.md",
    "Tài liệu & nghiên cứu": "docs-research.md",
    "Marketing & tăng trưởng": "marketing-growth.md",
    "Media & sáng tạo": "media-creative.md",
    "Khác": "other.md",
}


@dataclass(frozen=True)
class SkillRecord:
    name: str
    description: str
    path: str
    source: str
    invocation: str
    category: str
    enabled: bool


def normalize_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return str(json.loads(value))
        except json.JSONDecodeError:
            pass
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def parse_frontmatter(path: Path) -> tuple[str, str, list[str]]:
    issues: list[str] = []
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        return path.parent.name, "", [f"Không đọc được: {exc}"]

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return path.parent.name, "", ["Thiếu YAML frontmatter"]

    end = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if end is None:
        return path.parent.name, "", ["YAML frontmatter chưa đóng"]

    metadata: dict[str, str] = {}
    index = 1
    while index < end:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[index])
        if not match:
            index += 1
            continue
        key, value = match.group(1), match.group(2)
        if value in {"|", "|-", ">", ">-"}:
            block: list[str] = []
            index += 1
            while index < end and (not lines[index].strip() or lines[index][0].isspace()):
                block.append(lines[index].strip())
                index += 1
            metadata[key] = " ".join(part for part in block if part)
            continue
        metadata[key] = normalize_scalar(value)
        index += 1

    name = metadata.get("name", "").strip() or path.parent.name
    description = re.sub(r"\s+", " ", metadata.get("description", "")).strip()
    if "name" not in metadata:
        issues.append("Thiếu trường name; dùng tên thư mục")
    if not description:
        issues.append("Thiếu description")
    return name, description, issues


def normalized_words(value: str) -> str:
    return " " + re.sub(r"[^a-z0-9]+", " ", value.lower()).strip() + " "


def matches_keyword(haystack: str, keyword: str) -> bool:
    return f" {normalized_words(keyword).strip()} " in haystack


def classify(name: str, description: str) -> str:
    normalized_name = normalized_words(name)
    for category, keywords in NAME_CATEGORY_RULES:
        if any(matches_keyword(normalized_name, keyword) for keyword in keywords):
            return category
    normalized_description = normalized_words(description)
    for category, keywords in DESCRIPTION_CATEGORY_RULES:
        if any(matches_keyword(normalized_description, keyword) for keyword in keywords):
            return category
    return "Khác"


def compact_description(name: str, description: str) -> str:
    if not description:
        return f"Thực hiện workflow {name.replace('-', ' ')}."
    sentence = re.split(r"(?<=[.!?])\s+", description, maxsplit=1)[0]
    if len(sentence) > 240:
        sentence = sentence[:237].rstrip() + "..."
    return sentence


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except (OSError, ValueError):
        return False


def scan_root(
    root: Path,
    source: str,
    namespace: str | None,
    enabled: bool,
    seen_paths: set[str],
    issues: list[dict[str, str]],
) -> list[SkillRecord]:
    if not root.exists():
        return []

    records: list[SkillRecord] = []
    try:
        skill_files = sorted(root.rglob("SKILL.md"))
    except OSError as exc:
        issues.append({"path": str(root), "issue": f"Không quét được: {exc}"})
        return records

    for skill_file in skill_files:
        if any(part in {".git", "node_modules"} for part in skill_file.parts):
            continue
        try:
            canonical = str(skill_file.resolve()).lower()
        except OSError:
            canonical = str(skill_file.absolute()).lower()
        if canonical in seen_paths:
            continue
        seen_paths.add(canonical)

        name, description, file_issues = parse_frontmatter(skill_file)
        for issue in file_issues:
            issues.append({"path": str(skill_file), "issue": issue})

        actual_source = source
        if is_relative_to(skill_file, Path.home() / ".codex" / "skills" / ".system"):
            actual_source = "Codex system"
        invocation = f"${namespace}:{name}" if namespace else f"${name}"
        records.append(
            SkillRecord(
                name=name,
                description=description,
                path=str(skill_file),
                source=actual_source,
                invocation=invocation,
                category=classify(name, description),
                enabled=enabled,
            )
        )
    return records


def run_codex_plugin_list() -> tuple[list[dict], str | None]:
    try:
        result = subprocess.run(
            ["codex", "plugin", "list", "--json"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [], str(exc)
    if result.returncode != 0:
        return [], result.stderr.strip() or f"codex exited with {result.returncode}"
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return [], f"JSON plugin không hợp lệ: {exc}"
    return list(payload.get("installed", [])), None


def configured_plugins(codex_home: Path) -> tuple[list[dict], str | None]:
    config_path = codex_home / "config.toml"
    if not config_path.exists():
        return [], None
    try:
        with config_path.open("rb") as config_file:
            payload = tomllib.load(config_file)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return [], str(exc)

    configured: list[dict] = []
    for plugin_id, settings in payload.get("plugins", {}).items():
        if not isinstance(settings, dict) or not settings.get("enabled", True):
            continue
        name, separator, marketplace = str(plugin_id).partition("@")
        if not separator:
            continue
        base = codex_home / "plugins" / "cache" / marketplace / name
        versions = [path for path in base.iterdir() if path.is_dir()] if base.exists() else []
        versions.sort(key=lambda path: path.stat().st_mtime, reverse=True)
        installed_path = versions[0] if versions else None
        configured.append(
            {
                "pluginId": plugin_id,
                "name": name,
                "marketplaceName": marketplace,
                "version": installed_path.name if installed_path else None,
                "installedPath": str(installed_path) if installed_path else None,
                "enabled": True,
                "source": {"path": str(installed_path)} if installed_path else {},
            }
        )
    return configured, None


def plugin_root(item: dict, codex_home: Path) -> Path | None:
    marketplace = str(item.get("marketplaceName", ""))
    name = str(item.get("name", ""))
    version = item.get("version")
    candidates: list[Path] = []
    if marketplace and name and version:
        candidates.append(codex_home / "plugins" / "cache" / marketplace / name / str(version))
    installed_path = item.get("installedPath")
    if installed_path:
        candidates.append(Path(str(installed_path)))
    source = item.get("source") or {}
    for key in ("path", "url"):
        value = source.get(key)
        if value and not re.match(r"^[a-z]+://", str(value), flags=re.IGNORECASE):
            candidates.append(Path(str(value)))
    return next((candidate for candidate in candidates if candidate.exists()), None)


def declared_skill_roots(root: Path) -> list[Path]:
    roots: list[Path] = []
    manifests = [root / ".codex-plugin" / "plugin.json", root / "plugin.json"]
    for manifest in manifests:
        if not manifest.exists():
            continue
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        skill_path = payload.get("skills")
        if isinstance(skill_path, str):
            candidate = root / skill_path.replace("/", os.sep)
            if candidate.exists():
                roots.append(candidate)
                break
    fallback = root / "skills"
    if not roots and fallback.exists():
        roots.append(fallback)
    migrated_commands = root / ".codex-plugin" / "migrated-command-skills"
    if migrated_commands.exists():
        roots.append(migrated_commands)
    return roots


def local_skill_roots(codex_home: Path) -> list[tuple[Path, str]]:
    roots: list[tuple[Path, str]] = [
        (Path.home() / ".agents" / "skills", "Người dùng (~/.agents/skills)"),
        (codex_home / "skills", "Người dùng (~/.codex/skills)"),
    ]
    current = Path.cwd().resolve()
    for parent in (current, *current.parents):
        candidate = parent / ".agents" / "skills"
        if candidate.exists():
            roots.append((candidate, f"Repository ({candidate})"))
        if (parent / ".git").exists():
            break
    unique: list[tuple[Path, str]] = []
    seen: set[str] = set()
    for root, source in roots:
        key = str(root.resolve()).lower() if root.exists() else str(root.absolute()).lower()
        if key not in seen:
            unique.append((root, source))
            seen.add(key)
    return unique


def discover(include_disabled: bool) -> tuple[list[SkillRecord], list[dict[str, str]]]:
    codex_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    records: list[SkillRecord] = []
    issues: list[dict[str, str]] = []
    seen_paths: set[str] = set()

    for root, source in local_skill_roots(codex_home):
        records.extend(scan_root(root, source, None, True, seen_paths, issues))

    plugins, plugin_error = run_codex_plugin_list()
    if plugin_error:
        issues.append({"path": "codex plugin list --json", "issue": plugin_error})
    fallback_plugins, config_error = configured_plugins(codex_home)
    if config_error:
        issues.append({"path": str(codex_home / "config.toml"), "issue": config_error})
    plugins_by_id = {str(item.get("pluginId")): item for item in plugins}
    for item in fallback_plugins:
        plugins_by_id.setdefault(str(item.get("pluginId")), item)
    plugins = list(plugins_by_id.values())
    for item in plugins:
        enabled = bool(item.get("enabled", True))
        if not enabled and not include_disabled:
            continue
        root = plugin_root(item, codex_home)
        if root is None:
            issues.append({"path": str(item.get("pluginId", item.get("name", "plugin"))), "issue": "Không tìm thấy thư mục plugin đã cài"})
            continue
        skill_roots = declared_skill_roots(root)
        if not skill_roots:
            continue
        namespace = str(item.get("name") or item.get("marketplaceName") or "plugin")
        plugin_id = str(item.get("pluginId") or namespace)
        version = item.get("version")
        source = f"Plugin {plugin_id}" + (f" v{version}" if version else "")
        for skill_root in skill_roots:
            records.extend(scan_root(skill_root, source, namespace, enabled, seen_paths, issues))

    records.sort(key=lambda record: (record.category.casefold(), record.name.casefold(), record.source.casefold()))
    return records, issues


def markdown_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().replace("|", "\\|")


def prompt_for(record: SkillRecord) -> str:
    template = CATEGORY_PROMPTS.get(record.category, CATEGORY_PROMPTS["Khác"])
    return template.format(skill=f"`{record.invocation}`")


def source_label(source: str) -> str:
    normalized = source.casefold()
    if normalized.startswith("plugin ecc@"):
        return "ECC"
    if normalized.startswith(("plugin superpowers@", "plugin superpowers-dev@")):
        return "Superpowers"
    if normalized.startswith("plugin agent-skills@"):
        return "Agent Skills"
    if normalized.startswith("plugin "):
        plugin_id = source.removeprefix("Plugin ").split(" v", maxsplit=1)[0]
        return plugin_id.split("@", maxsplit=1)[0]
    if "~/.agents/skills" in normalized:
        return "User skills"
    if "~/.codex/skills" in normalized:
        return "Codex user"
    if normalized == "codex system":
        return "Codex system"
    if normalized.startswith("repository"):
        return "Repository"
    return source


def duplicate_guidance(name: str, rows: list[SkillRecord]) -> str:
    invocations = {row.invocation for row in rows}
    if "$design-system" in invocations and "$ecc:design-system" in invocations:
        return "Dùng `$design-system` cho token/component spec; dùng `$ecc:design-system` để tạo hoặc audit hệ thống hình ảnh."
    if "$superpowers:test-driven-development" in invocations and "$agent-skills:test-driven-development" in invocations:
        return "Dùng Superpowers khi cần TDD red-green-refactor nghiêm ngặt; dùng Agent Skills cho workflow TDD theo repository."
    return "Đọc mô tả từng lựa chọn và chọn đúng phạm vi; giữ namespace khi gọi skill plugin."


def render_category_page(category: str, records: list[SkillRecord]) -> str:
    lines = [
        f"# {category}",
        "",
        "[← Tổng quan](./index.md) · [Tất cả skills](./all-skills.md)",
        "",
        f"Có **{len(records)}** skill trong hạng mục này.",
        "",
        "| Nhu cầu / chức năng | Skill đề xuất | Prompt ví dụ | Nguồn |",
        "|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(compact_description(record.name, record.description)),
                    f"`{markdown_cell(record.invocation)}`",
                    markdown_cell(prompt_for(record)),
                    markdown_cell(source_label(record.source)),
                ]
            )
            + " |"
        )
    lines.extend(["", "[← Tổng quan](./index.md)", ""])
    return "\n".join(lines)


def render_dashboard_index(records: list[SkillRecord], issues: list[dict[str, str]], filters: list[str]) -> str:
    source_counts = Counter(source_label(record.source) for record in records)
    category_counts = Counter(record.category for record in records)
    duplicate_groups = {name: rows for name, rows in group_by_name(records).items() if len(rows) > 1}
    lines = [
        "# Skillcheck",
        "",
        "> Bảng điều hướng ngắn gọn. Mở một hạng mục để xem **nhu cầu / skill đề xuất / prompt ví dụ**.",
        "",
        "## Tổng quan",
        "",
        f"- **{len(records)}** skills từ **{len(source_counts)}** nguồn",
        f"- **{len(duplicate_groups)}** tên trùng; **{len(issues)}** vấn đề metadata hoặc truy cập",
    ]
    if filters:
        lines.append(f"- Bộ lọc đang dùng: **{markdown_cell(', '.join(filters))}**")
    lines.extend(
        [
            "",
            "## Chọn nhanh theo nhu cầu",
            "",
            "| Nhu cầu | Skill nên bắt đầu | Prompt ngắn |",
            "|---|---|---|",
            "| Làm rõ ý tưởng | `$superpowers:brainstorming` hoặc `$agent-skills:idea-refine` | `Làm rõ yêu cầu cho tính năng ... trước khi code.` |",
            "| Lập kế hoạch | `$superpowers:writing-plans` hoặc `$agent-skills:planning-and-task-breakdown` | `Lập kế hoạch triển khai ... theo từng file và bước xác minh.` |",
            "| Viết test/TDD | `$superpowers:test-driven-development` hoặc skill test đúng stack | `Triển khai ... theo red-green-refactor và chạy test.` |",
            "| Debug | `$superpowers:systematic-debugging` | `Tìm root cause của ... bằng bằng chứng rồi sửa tối thiểu.` |",
            "| Review code | `$agent-skills:code-review-and-quality` | `Review thay đổi hiện tại, ưu tiên bug và regression.` |",
            "| UI/UX | `$ui-ux-pro-max` | `Thiết kế ... responsive, accessible và sẵn sàng triển khai.` |",
            "| Bảo mật | `$ecc:security-review` | `Review bề mặt tấn công của ... và đề xuất cách xác minh bản sửa.` |",
            "| Phát hành | `$agent-skills:shipping-and-launch` | `Chuẩn bị release ..., gồm quality gate và rollback.` |",
            "",
            "## Danh mục",
            "",
            "| Hạng mục | Số skill | Mở |",
            "|---|---:|---|",
        ]
    )
    for category, count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0].casefold())):
        slug = CATEGORY_SLUGS.get(category, CATEGORY_SLUGS["Khác"])
        lines.append(f"| {markdown_cell(category)} | {count} | [Xem](./{slug}) |")
    lines.extend(["", "## Theo nguồn", "", "| Nguồn | Số skill |", "|---|---:|"])
    for source, count in sorted(source_counts.items(), key=lambda item: (-item[1], item[0].casefold())):
        lines.append(f"| {markdown_cell(source)} | {count} |")
    lines.extend(["", "## Skill trùng tên", ""])
    if duplicate_groups:
        lines.extend(["| Tên | Các lựa chọn | Cách chọn |", "|---|---|---|"])
        for name, rows in sorted(duplicate_groups.items(), key=lambda item: item[0].casefold()):
            options = ", ".join(f"`{row.invocation}` ({source_label(row.source)})" for row in rows)
            lines.append(
                f"| `{markdown_cell(name)}` | {markdown_cell(options)} | {markdown_cell(duplicate_guidance(name, rows))} |"
            )
    else:
        lines.append("Không phát hiện tên skill trùng.")
    lines.extend(
        [
            "",
            "## Cách dùng Skillcheck",
            "",
            "- `$skillcheck` — bắt đầu Q&A để làm rõ nhu cầu, sau đó đề xuất skill và prompt đúng bối cảnh.",
            "- `$skillcheck testing React checkout` — chỉ hỏi phần thông tin quan trọng còn thiếu.",
            "- `$skillcheck all` — bỏ qua Q&A và tạo lại toàn bộ danh mục.",
            "",
            "[Xem toàn bộ skills trong một trang](./all-skills.md) · Dữ liệu máy đọc: [`catalog.json`](./catalog.json)",
            "",
        ]
    )
    return "\n".join(lines)


def write_dashboard(
    directory: Path,
    records: list[SkillRecord],
    issues: list[dict[str, str]],
    filters: list[str],
) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    grouped: dict[str, list[SkillRecord]] = defaultdict(list)
    for record in records:
        grouped[record.category].append(record)
    directory.joinpath("index.md").write_text(render_dashboard_index(records, issues, filters), encoding="utf-8")
    for category, filename in CATEGORY_SLUGS.items():
        directory.joinpath(filename).write_text(render_category_page(category, grouped.get(category, [])), encoding="utf-8")
    directory.joinpath("all-skills.md").write_text(render_markdown(records, issues, filters), encoding="utf-8")
    directory.joinpath("catalog.json").write_text(
        json.dumps(
            {"count": len(records), "skills": [asdict(record) for record in records], "issues": issues},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def render_markdown(records: list[SkillRecord], issues: list[dict[str, str]], filters: list[str]) -> str:
    source_counts = Counter(record.source for record in records)
    category_counts = Counter(record.category for record in records)
    duplicate_groups = {name: rows for name, rows in group_by_name(records).items() if len(rows) > 1}

    lines = [
        "# Skillcheck — Danh mục Codex skills",
        "",
        f"- Tổng số skill: **{len(records)}**",
        f"- Số nguồn: **{len(source_counts)}**",
        f"- Tên skill bị trùng: **{len(duplicate_groups)}**",
        f"- Vấn đề metadata/quyền truy cập: **{len(issues)}**",
    ]
    if filters:
        lines.append(f"- Bộ lọc: **{markdown_cell(', '.join(filters))}**")

    lines.extend(["", "## Theo nguồn", "", "| Nguồn | Số skill |", "|---|---:|"])
    for source, count in sorted(source_counts.items(), key=lambda item: (-item[1], item[0].casefold())):
        lines.append(f"| {markdown_cell(source)} | {count} |")

    lines.extend(["", "## Theo hạng mục", "", "| Hạng mục | Số skill |", "|---|---:|"])
    for category, count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0].casefold())):
        lines.append(f"| {markdown_cell(category)} | {count} |")

    grouped: dict[str, list[SkillRecord]] = defaultdict(list)
    for record in records:
        grouped[record.category].append(record)
    for category in sorted(grouped, key=str.casefold):
        lines.extend([
            "",
            f"## {category}",
            "",
            "| Nhu cầu / chức năng | Skill đề xuất | Prompt ví dụ | Nguồn |",
            "|---|---|---|---|",
        ])
        for record in grouped[category]:
            need = compact_description(record.name, record.description)
            lines.append(
                "| "
                + " | ".join(
                    [
                        markdown_cell(need),
                        f"`{markdown_cell(record.invocation)}`",
                        markdown_cell(prompt_for(record)),
                        markdown_cell(record.source),
                    ]
                )
                + " |"
            )

    lines.extend(["", "## Skill trùng tên", ""])
    if duplicate_groups:
        lines.extend(["| Tên | Các lựa chọn | Hướng xử lý |", "|---|---|---|"])
        for name, rows in sorted(duplicate_groups.items(), key=lambda item: item[0].casefold()):
            options = ", ".join(f"`{row.invocation}` ({row.source})" for row in rows)
            lines.append(f"| `{markdown_cell(name)}` | {markdown_cell(options)} | Đọc từng SKILL.md và chọn theo phạm vi; không gộp tự động. |")
    else:
        lines.append("Không phát hiện tên skill trùng.")

    lines.extend(["", "## Vấn đề phát hiện", ""])
    if issues:
        lines.extend(["| Đường dẫn | Vấn đề |", "|---|---|"])
        for issue in issues:
            lines.append(f"| `{markdown_cell(issue['path'])}` | {markdown_cell(issue['issue'])} |")
    else:
        lines.append("Không phát hiện vấn đề metadata hoặc quyền truy cập.")

    lines.append("")
    return "\n".join(lines)


def group_by_name(records: Iterable[SkillRecord]) -> dict[str, list[SkillRecord]]:
    grouped: dict[str, list[SkillRecord]] = defaultdict(list)
    for record in records:
        grouped[record.name].append(record)
    return grouped


def apply_filters(records: list[SkillRecord], queries: list[str], sources: list[str], categories: list[str]) -> list[SkillRecord]:
    filtered = records
    for query in queries:
        term = query.casefold()
        filtered = [
            record
            for record in filtered
            if term in " ".join([record.name, record.description, record.source, record.category, record.invocation]).casefold()
        ]
    if sources:
        source_terms = [value.casefold() for value in sources]
        filtered = [record for record in filtered if any(term in record.source.casefold() for term in source_terms)]
    if categories:
        category_terms = [value.casefold() for value in categories]
        filtered = [record for record in filtered if any(term in record.category.casefold() for term in category_terms)]
    return filtered


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inventory Codex skills and generate usage guidance.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dashboard-dir", type=Path)
    parser.add_argument("--query", action="append", default=[])
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--include-disabled", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    records, issues = discover(args.include_disabled)
    records = apply_filters(records, args.query, args.source, args.category)
    filters = [*args.query, *args.source, *args.category]

    if args.dashboard_dir:
        write_dashboard(args.dashboard_dir, records, issues, filters)
        print(
            json.dumps(
                {
                    "dashboard": str(args.dashboard_dir.resolve()),
                    "count": len(records),
                    "issues": len(issues),
                },
                ensure_ascii=False,
            )
        )
        if not args.output:
            return 0

    if args.format == "json":
        content = json.dumps(
            {"count": len(records), "skills": [asdict(record) for record in records], "issues": issues},
            ensure_ascii=False,
            indent=2,
        )
    else:
        content = render_markdown(records, issues, filters)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
        print(json.dumps({"output": str(args.output.resolve()), "count": len(records), "issues": len(issues)}, ensure_ascii=False))
    else:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
