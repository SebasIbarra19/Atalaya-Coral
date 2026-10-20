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
| Last completed task | F1-T00c: local PostgreSQL 18 with pgvector in Compose, real `.env`, connection verified (2026-10-19) |
| Next task | F1-T00d (database roles: write for ingestion, read-only for the API) |
| Blockers | First sites are not decided |
| Last updated | 2026-10-19 |

## 2. Completed

| Date | What |
| --- | --- |
| 2026-10-10 | Flagship idea defined and references collected (`proyecto-insignia-referencias.md` in the Claude project) |
| 2026-10-14 | First specification written as a Claude Docs draft (Spanish) |
| 2026-10-14 | Reusable documentation prompt created and applied; 13 documents drafted in English |
| 2026-10-15 | F0 complete: README diagram, ADR-001 to 005, Makefile, CI green (PR #1, #2), repository public, ruleset `protect-main`, local gitleaks pre-commit hook |
| 2026-10-18 | Planned architecture diagram generated with Archify: `docs/diagrams/architecture.json` (source) and `architecture.html`; every node links to its lines in `03-architecture.md` and the ADRs at commit 6c3ea42 |

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
| 2026-10-18 | NGINX Ingress as reverse proxy; Terraform from F3 for the local cluster; no Ansible (ADR-013) | Standard and demanded; practice IaC for free before AWS; Kubernetes is already declarative | Traefik; Terraform only in F8; Ansible |
| 2026-10-18 | Sealed Secrets for cluster secrets (ADR-011) | Free and fits GitOps | Plain Secrets in Git; External Secrets |
| 2026-10-18 | gitleaks, CodeQL and Trivy in CI with supply chain rules (ADR-012) | DevSecOps; the March 2026 Trivy incident shows actions must be pinned | Actions pinned by tag; no scanners |
| 2026-10-18 | MLflow from the first trained model; Dependabot with owner approval | Avoid rebuilding experiments; reviewed updates | MLflow only in F6; automatic merges |
| 2026-10-18 | Architecture diagrams as HTML with the Archify skill (next task) | Richer, interactive diagrams for the portfolio | Mermaid only |
| 2026-10-19 | Local database: PostgreSQL 18 from the `pgvector/pgvector:pg18` image pinned by digest, in `deploy/compose/compose.yaml` under the `core` profile, port bound to 127.0.0.1, named volume | pgvector is needed in Branch C, so no image change later; digest pinning follows ADR-012; local-only port is least privilege | Plain `postgres:18` image; PostgreSQL 19 (not confirmed released); port open on all interfaces |
| 2026-10-19 | Python 3.14 managed with uv; committed `uv.lock`; installs with `uv sync --locked` (ADR-016) | Newest version the ML stack supports (SHAP depends on Numba); one tool for Python, environment and lockfile | Python 3.15 (too new); 3.13 (security-only); pip with venv and pip-tools; Poetry |
| 2026-10-19 | Docker Engine inside WSL2 Ubuntu instead of Docker Desktop; lazydocker as the visual interface | Fully open source, no Desktop license terms, lighter on RAM, and real Linux practice; kind and k3d run on the same engine | Docker Desktop |
| 2026-10-18 | lazydocker and k9s as personal development tools | Faster inspection of containers and the cluster | Only raw `docker` and `kubectl` commands |
| 2026-10-18 | Diagrams are Archify HTML plus JSON source in `docs/diagrams/`, built only from the documents, arrows from caller to callee, delivery receipts not committed (ADR-014) | Explorable diagrams a reviewer can check line by line | Mermaid only; output in `.archify/`; arrows in the direction of the data |
| 2026-10-18 | No AI attribution in commits, pull requests or files; one-line commit messages (ADR-015) | The owner is the only author of record, as decided on 2026-10-10 | Co-author trailer on AI-assisted commits |

## 4. In progress and blockers

- Review of the 13 drafts by the owner.
- Open: first sites, forecast horizon, notification channel, license confirmation, Python version, migration tool, EKS or k3s on EC2, uncertainty intervals, MLflow artifact storage.
- `03-architecture.md` section 4 still has two `[TO DEFINE]` items: the protocol between the dashboard and the domain agent, and the step that embeds `doc_chunks` (also what embeds the `search_docs` query).
## 5. Lessons learned

- VS Code keeps the PATH from when it was opened; restart it fully after installing a tool. `make` reads the `Makefile` in the current folder.
- `gitleaks-action` on pull requests needs `pull-requests: read` besides `contents: read`.
- Each CI job runs on its own clean machine; tools installed in one job do not exist in another.
- Git hooks must use LF line endings, live in `.git/hooks/` (not versioned) and have no extension.
- Run `git status` before every commit: anything staged goes into the commit (a test line slipped into PR #2 and was reverted in the same PR).
- Ruleset required checks match job names; renaming a job requires updating the ruleset.
- Kubernetes itself is free; a local cluster (kind or k3d) is real Kubernetes. Only managed cloud clusters and their machines cost money (F8).
- Ubuntu in WSL is a separate machine: it needs its own Git identity, its own gitleaks for the pre-commit hook and `core.fileMode false` for a repository on the Windows disk. Never bypass the hook with `--no-verify`.
- `psql` opens long output in a pager (`less`); `q` exits, and `\pset pager off` in `~/.psqlrc` disables it.
- A `DATABASE_URL` breaks with stray spaces, Windows line endings or passwords with `/`, `+` or `=`; hex passwords avoid the last problem.
- uv cannot hardlink between Linux and the Windows disk; `UV_LINK_MODE=copy` avoids the warning.
- `wsl --status` shows the default WSL version for new distributions, not installed ones; `wsl --list --verbose` lists what is installed.
- A fresh WSL distribution can fail with `Wsl/Service/E_UNEXPECTED`; `wsl --shutdown`, `wsl --update` or a reboot clears it.
- Being in the `docker` group is equivalent to root on that machine: fine on a personal development machine, handled with care on servers.
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
| 2026-10-18 | 00-spec, 02-trd, 03-architecture, 05-security, 08-testing, 09-plan, 10-tasks, README | Applied the plan adjustments: F1-T00 tasks, NGINX Ingress, Terraform from F3, Sealed Secrets, CI supply chain rules, GHCR, k6, MLflow from F5, F6 promotion and quality monitoring; ADR-011 to 013 added |
| 2026-10-18 | docs/diagrams/ (new) | Planned architecture diagram (Archify) built only from `03-architecture.md` and ADR-001 to 013; arrows follow section 4 (caller to callee) |
| 2026-10-18 | .gitignore | Ignores `docs/diagrams/*.delivery.json`: Archify delivery receipts hold local absolute paths and are not needed in the repository |
| 2026-10-18 | 03-architecture | Section 4: rows for NGINX Ingress, dashboard to domain agent, HolmesGPT to Ollama, the document indexing step and the Sealed Secrets controller (unknown facts marked `[TO DEFINE]`); section 10 lists ADR-014 and 015; two open questions added |
| 2026-10-18 | decisions | ADR-014 (architecture diagrams with Archify) and ADR-015 (no AI attribution) added |
| 2026-10-18 | AGENTS.md | Rule 11: no AI attribution, one-line commit messages (ADR-015) |
| 2026-10-19 | deploy/compose, Makefile, .env.example, 03-architecture, 10-tasks | Compose file for the local database, `make db-up`, `db-down`, `db-logs`; password generation hint; database row names PostgreSQL 18 with pgvector; F1-T00c checked |
| 2026-10-19 | 00-spec, 03-architecture, 06-code-style, 10-tasks, Makefile, decisions | Python 3.14 with uv decided (ADR-016); `make setup` runs `uv sync --locked`; F1-T00b checked |
| 2026-10-19 | 10-tasks | F1-T00a installs Docker Engine inside WSL2 (no Docker Desktop) and lazydocker, used from F1-T00c to inspect the PostgreSQL container and its logs |
| 2026-10-19 | 03-architecture, README | Review: link to the Archify diagram; MLflow row aligned with the spec (Decided, from F5); PostgreSQL stores `doc_chunks`; `docs/diagrams/` and Compose profiles in the repository tree; local cluster created with Terraform; decision log intro updated. No component or connection changed, so the diagram needs no regeneration |
| 2026-10-18 | docs/diagrams/ | Diagram updated to the new section 4 rows: Sealed Secrets arrow to the Kubernetes API, Ollama moved to the left outside the cluster; sources pinned to b5b7b31 |

## 7. Session log

| Date | What was done | What is next |
| --- | --- | --- |
| 2026-10-19 | F1-T00c done: `deploy/compose/compose.yaml` with the `db` service (profile `core`, healthcheck, named volume, local-only port), `make db-up`, `db-down`, `db-logs`; real `.env` with a generated hex password, confirmed ignored by Git; connected with `psql` using the owner's credentials (PostgreSQL 18.6); image pinned by digest | F1-T00d (database roles) |
| 2026-10-19 | F1-T00a merged (PR #8). F1-T00b done: gitleaks 8.30.1 installed in Ubuntu for the pre-commit hook, Git identity and Windows credential manager configured in WSL, `core.fileMode false`; uv 0.13.3 from the release tarball after a SHA-256 check; Python 3.14.8; `uv init --bare`, `uv python pin`, `uv sync`; `make setup`; ADR-016 | F1-T00c |
| 2026-10-19 | F1-T00a done: Ubuntu installed in WSL2 (systemd on by default), Docker Engine from the official apt repository with the Compose and buildx plugins, user added to the `docker` group, `hello-world` ran without `sudo`, lazydocker v0.25.2 installed from the release tarball after a SHA-256 check | VS Code WSL extension; F1-T00b |
| 2026-10-18 | Updated the diagram to the new section 4 rows (Sealed Secrets to Kubernetes API) and pinned its sources to b5b7b31; the document indexing step stays in a card because its component is `[TO DEFINE]`; automated checks passed and captures reviewed | Owner reviews; push and open the PR when the owner decides; then F1-T00a |
| 2026-10-18 | Removed an AI co-author trailer from the diagram commit before any push; recorded ADR-014 and ADR-015 and added rule 11 to `AGENTS.md`; filled the five section 4 gaps in `03-architecture.md` | Owner reviews; update the diagram to the new section 4 rows and re-pin its sources; push and open the PR when the owner decides; then F1-T00a |
| 2026-10-18 | Built the planned architecture diagram with Archify in `docs/diagrams/` (all automated checks passed, light and dark captures reviewed). Arrows and protocols come from section 4; additions only where sections 3 and 5 or an ADR state them. Sealed Secrets is drawn without arrows because no document gives its connection. Listed five gaps in section 4 (see section 4 of this file) | Owner reviews the diagram and decides on the section 4 gaps; then F1-T00a |
| 2026-10-18 | Reviewed DevOps, DevSecOps, MLOps, LLMOps and AIOps against the project; defined the Branch C design and the local resource budget for the development machine; moved the cloud from Azure to AWS; applied the plan adjustments (F1-T00, ingress, secrets, CI supply chain); ADR-006 to 013 | Architecture diagrams as HTML with Archify; then F1-T00a |
| 2026-10-15 | Owner completed F0 by hand with guidance: installed make, PR #1 (README diagram, ADRs, CI permission fix), repository made public, ruleset `protect-main` (direct push to main rejected with GH013), local gitleaks hook (fake `github-pat` blocked), PR #2 (`make scan` with gitleaks, CI runs `make lint test`). Gate F0 passed | F1-T01: decide the first sites (strict mode) |
| 2026-10-14 | F0 review: T01, T02 confirmed done (commit ceb51f5, pushed). T03: architecture diagram added to README. T07: five ADRs written in `docs/decisions/`. Found: `make` not installed locally; repository is private (branch protection on GitHub Free needs a public repo or a paid plan) | Owner reviews ADRs; decide on installing make and gitleaks; open a PR to run CI (T05) |
| 2026-10-14 | Name chosen (Atalaya). Local repo created with remote. Starter package added (CLAUDE.md, README, Makefile stubs, .gitignore, .env.example, LICENSE, minimal CI) and project name updated in all front matter | Owner reviews and makes the first commit and push; then F0-T03 onward |
| 2026-10-14 | Applied the documentation prompt to the flagship project; drafted `00-spec` to `11-memory` and `AGENTS.md` | Owner reviews drafts; then create the repository (F0) |

## Open questions

See `00-spec.md`, section 10.

## Related documents

[00-spec.md](00-spec.md) · [09-implementation-plan.md](09-implementation-plan.md) · [10-tasks.md](10-tasks.md) · [AGENTS.md](../AGENTS.md)
