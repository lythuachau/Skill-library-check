# Skill Library Check

[Tiếng Việt](./README.md) | [English](./README_EN.md) | [简体中文](./README_ZH-CN.md)

`Skillcheck` is a Codex skill that inventories installed skills, clarifies requests through adaptive Q&A, recommends the right skills for each task, and generates prompts that are ready to use.

This repository contains the Skillcheck source for Codex CLI and the Codex extension for VS Code.

## Key features

- Scans live skill locations instead of relying on a remembered list.
- Finds Personal, repository, Codex system, and enabled-plugin skills.
- Asks one question at a time when a request is vague, with no more than five necessary questions.
- Skips information the user has already supplied.
- Summarizes the context and waits for confirmation before recommending skills.
- Recommends a primary skill, supporting skills, and meaningful alternatives.
- Generates prompts tailored to the goal, stack, current state, deliverable, constraints, and verification criteria.
- Detects duplicate skill names and invalid `SKILL.md` metadata.
- Produces a readable multi-page Markdown dashboard.
- Produces `catalog.json` for use by other tools.

## Requirements

- Codex CLI or the Codex extension for VS Code.
- Python **3.11 or later**.
- Git when installing by cloning this repository.

The scanner uses only the Python standard library. No `pip install` step is required.

Check your environment:

```powershell
codex --version
python --version
git --version
```

## Installation

### Windows PowerShell

```powershell
git clone https://github.com/lythuachau/Skill-library-check.git

$source = Join-Path $PWD "Skill-library-check\skills\skillcheck"
$target = Join-Path $HOME ".agents\skills\skillcheck"

New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -Path "$source\*" -Destination $target -Recurse -Force
```

Verify the installation:

```powershell
Test-Path "$HOME\.agents\skills\skillcheck\SKILL.md"
```

The result should be:

```text
True
```

### macOS or Linux

```bash
git clone https://github.com/lythuachau/Skill-library-check.git
mkdir -p "$HOME/.agents/skills/skillcheck"
cp -R Skill-library-check/skills/skillcheck/. "$HOME/.agents/skills/skillcheck/"
test -f "$HOME/.agents/skills/skillcheck/SKILL.md" && echo "Skillcheck installed"
```

### Reload VS Code

After installation:

1. Open the Command Palette with `Ctrl+Shift+P`.
2. Run **Developer: Reload Window**.
3. Open a new Codex conversation.
4. Type `$skillcheck` and select **Skillcheck – Personal** if VS Code displays multiple choices.

## Invoking the skill

### Recommended method

Type `$skillcheck`, select it from autocomplete, and then enter your request:

```text
$skillcheck Recommend the right skills for testing a React checkout flow.
```

You can also open the skill list first:

```text
/skills
```

Then select **Skillcheck** and enter your request.

> `recommend` is not a child skill. It is simply part of the request. For example: `$skillcheck recommend skills for testing a React checkout flow`.

## Usage modes

### 1. Vague request

```text
$skillcheck
```

Skillcheck asks one question at a time to collect missing information:

1. The goal to accomplish.
2. The project, feature, and technology stack.
3. The current implementation state or observed problem.
4. The desired deliverable.
5. Constraints and verification criteria.

It stops as soon as enough information is available, summarizes the request, and waits for confirmation such as `approved`, `ok`, or a correction.

Example conversation:

```text
User: $skillcheck
Skillcheck: What kind of work do you need help with?
User: Testing a React checkout flow.
Skillcheck: Is checkout already implemented or still being built?
User: It is implemented but has no tests.
Skillcheck: Do you need unit, integration, or end-to-end tests?
User: Integration and E2E tests with Playwright.
Skillcheck: [Summarizes the request and waits for confirmation]
User: Approved.
```

### 2. Clear request

```text
$skillcheck testing a React checkout flow with Playwright; integration and E2E tests are required
```

Skillcheck uses the supplied information and asks only for critical missing details that would change the recommendation or final prompt.

### 3. Full catalog

```text
$skillcheck all
```

The `all` mode skips Q&A and immediately generates the complete dashboard.

## Examples by task

### Requirements discovery

```text
$skillcheck I want to add Google sign-in, but the user flow and MVP scope are unclear. Choose skills that can clarify requirements and produce a specification.
```

### Planning

```text
$skillcheck Recommend skills for planning Google sign-in with Next.js 15 and Supabase. The plan must identify affected files, migrations, tests, and completion criteria.
```

### Testing and TDD

```text
$skillcheck Choose skills for implementing a React shopping cart with strict TDD. Use Vitest and Testing Library, and run type checking before completion.
```

### Debugging

```text
$skillcheck An order API is being called twice in React Strict Mode. Choose a root-cause debugging skill that requires evidence before changes and verifies regressions afterward.
```

### Code review

```text
$skillcheck Choose skills to review the current diff. Prioritize logic bugs, security, regressions, performance, and missing tests rather than minor style issues.
```

### UI/UX

```text
$skillcheck Recommend skills for designing a responsive SaaS dashboard with Next.js and Tailwind. Include a design system, accessibility, and component specifications.
```

### Security

```text
$skillcheck Choose skills for reviewing FastAPI authentication and authorization. Include risk ranking, evidence, fixes, and verification steps.
```

### Release

```text
$skillcheck Recommend skills for releasing a Docker application to production. Include quality gates, a migration plan, rollback, and smoke tests.
```

## Generated dashboard

By default, Skillcheck generates its report inside the open repository:

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

### File roles

| File | Contents |
|---|---|
| `index.md` | Summary, quick routing, and counts by source and category |
| Category pages | Needs, recommended skills, example prompts, and sources |
| `all-skills.md` | Every discovered skill in one table |
| `catalog.json` | Structured data for scripts and other tools |

Each category page uses this structure:

| Need / capability | Recommended skill | Example prompt | Source |
|---|---|---|---|
| Short description from live metadata | Exact invocation, including plugin namespace | Ready-to-paste prompt | Short source label |

## Running the scanner directly

Skillcheck normally runs the scanner after confirmation. You can also run it manually.

### Windows PowerShell

```powershell
$scanner = "$HOME\.agents\skills\skillcheck\scripts\scan_skills.py"
python $scanner --dashboard-dir ".\.agents\skillcheck"
```

### macOS or Linux

```bash
python "$HOME/.agents/skills/skillcheck/scripts/scan_skills.py" \
  --dashboard-dir "./.agents/skillcheck"
```

### Filter by keyword

```powershell
python $scanner --query "testing" --dashboard-dir ".\.agents\skillcheck"
python $scanner --query "React" --dashboard-dir ".\.agents\skillcheck"
```

### Filter by source

```powershell
python $scanner --source "Superpowers" --dashboard-dir ".\.agents\skillcheck"
python $scanner --source "ECC" --dashboard-dir ".\.agents\skillcheck"
```

### Filter by category

```powershell
python $scanner --category "Testing" --dashboard-dir ".\.agents\skillcheck"
python $scanner --category "UI/UX" --dashboard-dir ".\.agents\skillcheck"
```

### Export JSON

```powershell
python $scanner --format json --output ".\.agents\skillcheck-catalog.json"
```

The `--query`, `--source`, and `--category` options may be repeated.

## Skill sources scanned

| Source | Location or discovery method |
|---|---|
| Personal skills | `~/.agents/skills` |
| Codex user/system skills | `$CODEX_HOME/skills` or `~/.codex/skills` |
| Repository skills | `.agents/skills` from the working directory to the repository root |
| Plugin skills | Skill roots returned by `codex plugin list --json` |

Plugin namespaces are preserved:

```text
$agent-skills:test-driven-development
$superpowers:test-driven-development
$ecc:security-review
```

This distinguishes skills with the same name but different workflows.

## Personal versus Team

| Type | Scope | Typical location |
|---|---|---|
| Personal | Available to the current user across projects | `~/.agents/skills/skillcheck` |
| Team | Available to a repository, workspace, or organization | `<repository>/.agents/skills/skillcheck` or an organization-managed source |

To avoid duplicate entries, install the active skill at only one scope. This repository stores its source under `skills/skillcheck`, not `.agents/skills/skillcheck`, so cloning it does not automatically create another Team skill.

## Updating

From the cloned repository:

```powershell
git pull

$source = Join-Path $PWD "skills\skillcheck"
$target = Join-Path $HOME ".agents\skills\skillcheck"
Copy-Item -Path "$source\*" -Destination $target -Recurse -Force
```

Then run **Developer: Reload Window** in VS Code.

## Troubleshooting

### Skillcheck is not listed

Check the file:

```powershell
Get-Item "$HOME\.agents\skills\skillcheck\SKILL.md"
```

Then:

1. Run **Developer: Reload Window**.
2. Open a new Codex conversation.
3. Type `$skillcheck` or open `/skills`.
4. Confirm the YAML frontmatter contains `name: skillcheck` and a `description`.

### Both Personal and Team entries appear

Locate every copy:

```powershell
Get-ChildItem "$HOME\.agents\skills", ".\.agents\skills" -Filter SKILL.md -File -Recurse |
  Select-String -Pattern '^name:\s*skillcheck\s*$'
```

Keep Personal for cross-project use. Rename or move the repository copy outside `.agents/skills` if it should not be loaded as a Team skill.

### `$skillcheck recommend` does not appear as a separate skill

This is expected. `$skillcheck` is the skill; `recommend` is part of your request:

```text
$skillcheck recommend the right skills for testing a React checkout flow
```

Select `$skillcheck` from autocomplete first, then enter the rest of the request.

### Plugin skills are missing

```powershell
codex plugin list --json
```

Make sure the plugin is installed, enabled, and contains a valid skill directory.

### Unicode problems in PowerShell

```powershell
$env:PYTHONUTF8 = "1"
python "$HOME\.agents\skills\skillcheck\scripts\scan_skills.py" --dashboard-dir ".\.agents\skillcheck"
```

## Privacy

The scanner does not send skill contents to a separate service operated by this repository. It reads local metadata, calls `codex plugin list --json` to find enabled plugins, and writes reports to the output directory selected by the user.

`catalog.json` may contain absolute local paths. Review it before committing or sharing it publicly.

## Source structure

```text
skills/skillcheck/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── scan_skills.py
```

- `SKILL.md`: Q&A, confirmation, routing, and presentation behavior.
- `agents/openai.yaml`: display name, short description, and default UI prompt.
- `scripts/scan_skills.py`: discovery, classification, duplicate detection, and dashboard generation.

## Validating contributions

```powershell
python -m py_compile ".\skills\skillcheck\scripts\scan_skills.py"
python ".\skills\skillcheck\scripts\scan_skills.py" --format json --query "skillcheck"
git diff --check
```

Suggested contribution workflow:

1. Fork the repository.
2. Create a branch for the change.
3. Update the skill or scanner.
4. Run the validation commands above.
5. Open a pull request describing the behavior before and after the change.

## Repository

- GitHub: <https://github.com/lythuachau/Skill-library-check>
- Skill source: [`skills/skillcheck`](./skills/skillcheck)
- Issue tracker: <https://github.com/lythuachau/Skill-library-check/issues>
