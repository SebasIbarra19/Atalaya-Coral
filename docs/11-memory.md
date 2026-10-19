---
titulo: Project Memory
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.1
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: [00-spec.md, 09-implementation-plan.md, 10-tasks.md]
---

# Project Memory

The living document. Update it at the end of every work session. Add entries, never rewrite history. If a chat contradicts this file, this file wins.

## 1. Current state

| Item | Value |
| --- | --- |
| Current phase | F1 (ingestion and database, strict) |
| Last completed task | F0 complete (gate passed 2026-10-15) |
| Next task | F1-T01 (decide the first sites) |
| Blockers | First sites are not decided |
| Last updated | 2026-10-15 |

## 2. Completed

| Date | What |
| --- | --- |
| 2026-10-10 | Flagship idea defined and references collected (`proyecto-insignia-referencias.md` in the Claude project) |
| 2026-10-14 | First specification written as a Claude Docs draft (Spanish) |
| 2026-10-14 | Reusable documentation prompt created and applied; 13 documents drafted in English |
| 2026-10-15 | F0 complete: README diagram, ADR-001 to 005, Makefile, CI green (PR #1, #2), repository public, ruleset `protect-main`, local gitleaks pre-commit hook |

## 3. Important decisions

| Date | Decision | Reason | Alternatives discarded |
| --- | --- | --- | --- |
| 2026-10-10 | Data from NOAA Coral Reef Watch 5 km for Costa Rican sites | Public, daily, real domain | Own data (does not exist yet) |
| 2026-10-10 | Branch A replicates the approach of Arcodia et al. (2025), XGBoost with SHAP, starting from a simple baseline | Explainable and proven on a similar problem | Neural networks |
| 2026-10-10 | Branch C is split: HolmesGPT for operations and an own domain agent | Learn both integrating and building | Only one of them |
| 2026-10-10 | The jiu-jitsu app is not a workload of this platform | Keep client work and portfolio separate | Reusing it |
| 2026-10-10 | AI works as mentor and copilot, not author | The goal is learning | AI writes everything |
| 2026-10-14 | No fixed dates; phases close at exit gates | Available hours vary by semester | Calendar plan |
| 2026-10-14 | Local cluster first, cloud later | Free and repeatable | Cloud from the start |
| 2026-10-14 | Mentor mode is mixed by phase | Strict where the owner wants mastery, flexible on infrastructure configuration | One mode for all |
| 2026-10-14 | Documents are written in English | Public portfolio repository | Spanish |
| 2026-10-14 | Independent from CoraMar for now | Avoid depending on approvals | Connected from the start |
| 2026-10-14 | Project name is Atalaya (watchtower); repository `Atalaya-Coral` | Short, original, ties to early warning | Isoterma, Zooxa, Coralert, Vigia, Centinela |
| 2026-10-14 | Repository will be public | Portfolio project; branch protection on GitHub Free needs a public repository | Keep private without protection |
| 2026-10-15 | CI `make-check` runs `make lint test`; secret scanning only in the `secret-scan` job | CI jobs run on separate machines and gitleaks is only installed in `secret-scan`; avoids a duplicate scan | Installing gitleaks in `make-check`; skipping `scan` when gitleaks is missing (silently disables a security check) |
| 2026-10-14 | Owner runs the remaining F0 steps by hand with AI guidance | Learn the tooling (make, CI, rulesets, hooks) | AI runs them |
| 2026-10-14 | Markdown files in the repository are the source of truth; the first Spanish Claude Docs draft is frozen as a reading copy | One source of truth | Two editable copies |
| 2026-10-18 | Domain agent uses read-only tools through an MCP server, RAG with pgvector and structured outputs (ADR-007) | Current LLM practices, easy to evaluate, no extra database | Data pasted into the prompt; separate vector database |
| 2026-10-18 | No fine-tuning; RAG and prompting instead (ADR-007) | No training set; data changes daily | Fine-tuning a small model |
| 2026-10-18 | Language model runs locally with Ollama on the host, outside the cluster (ADR-006) | Zero cost; uses the laptop GPU; GPU passthrough to a local cluster on Windows is fragile | Paid API by default; Ollama inside the cluster; llama.cpp, LocalAI, vLLM (needs a bigger GPU) |
| 2026-10-18 | Phoenix for LLM observability (ADR-008) | Single container, built on OpenTelemetry | Langfuse self-hosted (several extra services) |
| 2026-10-18 | Compose profiles and WSL2 memory cap (ADR-009) | 16 GB RAM is the real local limit | Running the whole stack at once |
| 2026-10-18 | AWS instead of Azure for F8, free plan only, account created only when F8 starts (ADR-010) | AWS appears more in the job postings reviewed; avoid accidental charges | Azure through the Student Pack |
| 2026-10-18 | lazydocker and k9s as personal development tools | Faster inspection of containers and the cluster | Only raw `docker` and `kubectl` commands |

## 4. In progress and blockers

- Review of the 13 drafts by the owner.
- Open: first sites, forecast horizon, notification channel, license confirmation.

## 5. Lessons learned

- VS Code keeps the PATH from when it was opened; restart it fully after installing a tool. `make` reads the `Makefile` in the current folder.
- `gitleaks-action` on pull requests needs `pull-requests: read` besides `contents: read`.
- Each CI job runs on its own clean machine; tools installed in one job do not exist in another.
- Git hooks must use LF line endings, live in `.git/hooks/` (not versioned) and have no extension.
- Run `git status` before every commit: anything staged goes into the commit (a test line slipped into PR #2 and was reverted in the same PR).
- Ruleset required checks match job names; renaming a job requires updating the ruleset.
- Kubernetes itself is free; a local cluster (kind or k3d) is real Kubernetes. Only managed cloud clusters and their machines cost money (F8).
- On this laptop, RAM (16 GB) limits the local stack more than the GPU does; XGBoost needs no GPU at this data size.

## 6. Document changes

| Date | Document | What changed and why |
| --- | --- | --- |
| 2026-10-14 | All | First drafts created from the documentation prompt and the specification |
| 2026-10-14 | All | Project name set to Atalaya in front matter; name TBD removed |
| 2026-10-15 | .github/workflows/ci.yml | Added `pull-requests: read`; `make-check` runs `make lint test` |
| 2026-10-15 | Makefile | `scan` runs `gitleaks git --redact --verbose` |
| 2026-10-15 | 10-tasks.md | F0 tasks checked, gate F0 passed |
| 2026-10-14 | README.md | Added architecture diagram and link to `docs/decisions/` (F0-T03) |
| 2026-10-18 | 00-spec, 01-prd, 02-trd, 03-architecture, 05-security, 08-testing, 09-plan, 10-tasks, README | Branch C design (MCP, RAG with pgvector, structured outputs, Phoenix, local Ollama), development machine constraints, Compose profiles, development tools; ADR-006 to 009 added |
| 2026-10-18 | 00-spec, 01-prd, 02-trd, 03-architecture, 05-security, 09-plan, 10-tasks, ADR-001 | Cloud provider changed from Azure to AWS (free plan only); F8 access and cost rules; ADR-010 added |

## 7. Session log

| Date | What was done | What is next |
| --- | --- | --- |
| 2026-10-18 | Reviewed DevOps, DevSecOps, MLOps, LLMOps and AIOps against the project; defined the Branch C design and the local resource budget for the development machine; moved the cloud from Azure to AWS; ADR-006 to 010 | F1-T01: decide the first sites (strict mode) |
| 2026-10-15 | Owner completed F0 by hand with guidance: installed make, PR #1 (README diagram, ADRs, CI permission fix), repository made public, ruleset `protect-main` (direct push to main rejected with GH013), local gitleaks hook (fake `github-pat` blocked), PR #2 (`make scan` with gitleaks, CI runs `make lint test`). Gate F0 passed | F1-T01: decide the first sites (strict mode) |
| 2026-10-14 | F0 review: T01, T02 confirmed done (commit ceb51f5, pushed). T03: architecture diagram added to README. T07: five ADRs written in `docs/decisions/`. Found: `make` not installed locally; repository is private (branch protection on GitHub Free needs a public repo or a paid plan) | Owner reviews ADRs; decide on installing make and gitleaks; open a PR to run CI (T05) |
| 2026-10-14 | Name chosen (Atalaya). Local repo created with remote. Starter package added (CLAUDE.md, README, Makefile stubs, .gitignore, .env.example, LICENSE, minimal CI) and project name updated in all front matter | Owner reviews and makes the first commit and push; then F0-T03 onward |
| 2026-10-14 | Applied the documentation prompt to the flagship project; drafted `00-spec` to `11-memory` and `AGENTS.md` | Owner reviews drafts; then create the repository (F0) |

## Open questions

See `00-spec.md`, section 10.

## Related documents

[00-spec.md](00-spec.md) · [09-implementation-plan.md](09-implementation-plan.md) · [10-tasks.md](10-tasks.md) · [AGENTS.md](../AGENTS.md)
