---
name: skillcheck
description: Inventory Codex skills from user, repository, system, and installed-plugin locations; use adaptive Q&A to clarify vague requests; recommend the right skills for a work item; generate context-specific prompts; and build a readable multi-page catalog. Use when the user invokes Skillcheck, asks what skills are installed, asks which skill to use for planning/testing/debugging/review/UI work, or wants a complete skill catalog.
---

# Skillcheck

Build recommendations from the live filesystem and the user's confirmed context. Never rely on a remembered skill list.

## Route the invocation

Classify the request before scanning:

- **Full catalog:** `$skillcheck all` or an equivalent explicit request. Skip Q&A and build the complete dashboard immediately.
- **Clear work item:** the request already states a concrete goal and useful context, such as `$skillcheck testing React checkout`. Ask only for critical missing information that would materially change the recommendation.
- **Vague request:** `$skillcheck`, `/Skillcheck`, or a request without a clear goal. Run the adaptive Q&A below before recommending skills or generating example prompts.

## Run adaptive Q&A

Ask one question per turn. Skip facts already provided, avoid repeating questions, and stop as soon as there is enough context. Ask no more than five questions unless the user explicitly asks for deeper discovery.

Use this order, adapting the choices to earlier answers:

1. **Mục tiêu:** What does the user need now? Offer concise numbered examples such as làm rõ yêu cầu, lập kế hoạch, coding, testing, debug, review, security, UI/UX, performance, release, toàn bộ danh mục, or a free-form goal.
2. **Dự án và stack:** Which repository, product area, language, framework, and relevant files or feature are involved?
3. **Trạng thái hiện tại:** Is this a new feature, an existing implementation, a failure, or a change under review? Capture symptoms or known evidence when relevant.
4. **Đầu ra mong muốn:** Does the user want a plan, code change, test suite, diagnosis, review report, UI specification, release checklist, or another concrete deliverable?
5. **Ràng buộc và xác minh:** Capture deadlines, compatibility constraints, commands, acceptance criteria, and what must be checked before completion.

Questions must be easy to answer and include a free-form path. Do not force the user through every choice when a short answer is sufficient.

When enough information is available, restate it in the user's language:

```text
Mục tiêu:
Dự án/stack:
Trạng thái hiện tại:
Đầu ra mong muốn:
Ràng buộc/xác minh:
```

Ask the user to confirm or correct this summary, then wait. Do not scan, recommend skills, or generate the final prompt until confirmation. A direct confirmation such as `duyệt`, `ok`, or `đúng` is sufficient.

## Build the inventory after confirmation

1. Resolve `scripts/scan_skills.py` relative to this `SKILL.md`.
2. Resolve the repository root. Prefer `<repository>/.agents/skillcheck`; if the current directory is already `.agents`, use `<current-directory>/skillcheck`.
3. Run the scanner with the available Python launcher:

```powershell
python "<skillcheck-dir>/scripts/scan_skills.py" --dashboard-dir "<repository>/.agents/skillcheck"
```

For a clear, confirmed work item, pass one or more `--query "<text>"`, `--source "<text>"`, or `--category "<text>"` filters when they improve relevance. Do not filter `$skillcheck all`.

The scanner inspects:

- Current user skills under `~/.agents/skills`.
- Legacy/user and system skills under `$CODEX_HOME/skills` or `~/.codex/skills`.
- Repository `.agents/skills` directories from the working directory to the repository root.
- Skill roots declared by every enabled plugin returned by `codex plugin list --json`.

## Present recommendations

Use the user's language. Recommend a small ordered set rather than dumping the catalog:

1. **Skill chính** — best fit for the confirmed outcome.
2. **Skill bổ trợ** — adds stack-specific implementation, testing, review, or delivery guidance.
3. **Skill thay thế** — include only when it represents a meaningful tradeoff.

Read the live `description` and, when needed, the actual `SKILL.md` before recommending. Preserve the exact invocation, including plugin namespace.

Always use this compact structure:

| Nhu cầu | Skill đề xuất | Prompt ví dụ |
|---|---|---|

Tailor every example prompt with the confirmed goal, stack, current state, deliverable, constraints, and verification criteria. Prompts must be ready to paste; avoid generic examples after Q&A.

Link to the readable dashboard rather than printing hundreds of rows in chat. Prefer a relative link such as `[Mở Skillcheck](./skillcheck/index.md)` when the report is under the current `.agents` directory. Mention `all-skills.md` only when the user needs the entire ungrouped table.

Report the counts for skills, sources, duplicates, and metadata/access issues. The dashboard contains:

- `index.md` for summary, quick routing, categories, sources, and duplicate guidance.
- One page per category with needs, recommended skills, prompts, and short source labels.
- `all-skills.md` for the complete table.
- `catalog.json` for machine-readable data.

## Routing priorities

Use these defaults, then refine them from each installed skill's actual scope:

| Hạng mục | Ưu tiên | Khi chọn |
|---|---|---|
| Khám phá yêu cầu | Superpowers `brainstorming`; Agent Skills `idea-refine`, `interview-me`, `spec-driven-development` | Superpowers for design dialogue; Agent Skills for a formal spec lifecycle. |
| Lập kế hoạch | Superpowers `writing-plans`; Agent Skills `planning-and-task-breakdown`; ECC planning skills | Superpowers for file-level steps, Agent Skills for lifecycle planning, ECC for specialized orchestration. |
| TDD và testing | Superpowers `test-driven-development`; Agent Skills `test-driven-development`; ECC stack-specific testing | Superpowers for strict red-green-refactor, Agent Skills for repository-aware TDD, ECC for a particular stack. |
| Debug | Superpowers `systematic-debugging`; Agent Skills `debugging-and-error-recovery`; ECC diagnostics | Start with systematic root-cause analysis, then add stack-specific diagnostics. |
| Code review | Agent Skills `code-review-and-quality`; Superpowers review skills; ECC quality/security skills | Broad review first, then specialized audits. |
| UI/UX | `ui-ux-pro-max`; Agent Skills `frontend-ui-engineering`; ECC frontend skills | Start with design intelligence, then add implementation guidance. |
| Hiệu năng | Agent Skills `performance-optimization`; ECC stack-specific performance skills | Measure first, optimize, then measure again. |
| Bảo mật | ECC `security-review` or `security-scan`; Agent Skills `security-and-hardening` | Focused scan plus secure engineering practices. |
| Phát hành | Agent Skills `shipping-and-launch`; Superpowers `finishing-a-development-branch`; ECC deployment skills | Combine delivery checks, branch completion, and deployment guidance. |

## Invocation compatibility

Prefer `$skillcheck` or select `skillcheck` through `/skills`. A compatibility prompt may expose `/prompts:skillcheck` in Codex CLI and the IDE extension. Treat `/Skillcheck` written in normal chat as an explicit invocation.
