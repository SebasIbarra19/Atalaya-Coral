---
titulo: Implementation Plan
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.1
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: [00-spec.md, 01-prd.md, 02-trd.md, 03-architecture.md]
---

# Implementation Plan

There are no dates. Available hours vary by semester, so progress is measured by exit gates. Work is split into small tasks in `10-tasks.md`.

## 1. Key milestones

| Milestone | Phases | Deliverable | Exit gate | Depends on |
| --- | --- | --- | --- | --- |
| M1: Core | F0, F1, F2 | Repository with documentation, ingestion into PostgreSQL, read API and dashboard (release v0.1) | The core starts with a single command on a clean clone | None |
| M2: Platform | F3, F4 | Local Kubernetes, GitOps deployment, observability for ingestion and API | A change in Git is deployed and is visible on the dashboards | M1 |
| M3a: Forecast | F5 | Baseline and XGBoost with SHAP (release v0.2) | Forecast beats the baseline on the held-out period; leakage test passes | M1 |
| M3b: MLOps | F6 | Tracked runs, scheduled retraining, drift check, notifications (release v0.3) | A retrain runs on schedule and its result is recorded | M2, M3a |
| M3c: Agents | F7 | HolmesGPT and the domain agent with evaluations (release v0.4) | Agent evaluation set passes; read-only access verified | M2, M3a |
| M4: Cloud | F8 | Everything on Azure through Terraform (release v1.0) | Created and destroyed with Terraform within budget | M2, M3b |

The minimum deliverable is M1 plus M3a. M3a depends only on the core, so it can run before or alongside M2 if the learning order is changed (decision for the owner, logged in `11-memory.md`).

## 2. Implementation details by phase

| Phase | Technical order | Prior decisions needed | Main risk | Verified by |
| --- | --- | --- | --- | --- |
| F0 | Create repository, README skeleton, `docs/`, Makefile, minimal CI, secret scan, ADRs 001 to 005 | License confirmation | Over-engineering the setup | CI green on an empty project |
| F1 | Choose sites; study the ERDDAP dataset; schema migrations; ingestion with idempotent writes and run log; backfill | Sites; exact variables; start year | Coarse pixels for small reefs; NOAA schema surprises | TC-1 to TC-6 |
| F2 | Read API with contract tests; dashboard with all states; Docker Compose; `make up` | API conventions; dashboard overview (map or list) | Mixing data and presentation | TC-7 to TC-10, TC-18 |
| F3 | Dockerfiles; local cluster; manifests; ArgoCD syncing `deploy/k8s` | Helm or Kustomize | Local resource limits | A change in Git reaches the cluster |
| F4 | Metrics, logs and traces for ingestion and API; dashboards and alert rules as code | Alert thresholds after first measurement | Alert noise | A provoked failure raises an alert |
| F5 | Features; baseline; XGBoost; temporal validation; SHAP; forecasts into the database | Horizon; evaluation window | Leakage; modest results | TC-11 to TC-13 |
| F6 | MLflow; scheduled retraining; drift check; notifications | Notification channel; drift method | Complexity for little data | TC-14 |
| F7 | Ollama on the host; MCP server with read-only tools; document corpus into pgvector; domain agent with structured outputs; Phoenix traces; evaluation set in CI; HolmesGPT on the local cluster with read-only access | Exact local model (chosen by evaluations); document corpus | Unsupported answers; prompt injection; VRAM limits | TC-15 to TC-17, TC-21 to TC-25 |
| F8 | Terraform modules; deploy through GitOps; budget alert; teardown | Region; cost limits | Unexpected cost | Create and destroy cycle |

Each phase ends by publishing its result in the repository and updating `11-memory.md`.

## 3. Environments and deployment step by step

1. **Local core:** `make up` starts the Compose stack (database, ingestion, API, dashboard).
2. **Local cluster:** create the cluster, install ArgoCD, point it at `deploy/k8s`, and let it sync.
3. **Observability:** deploy the stack through GitOps; import dashboards and alert rules from `observability/`.
4. **Cloud:** run Terraform for the infrastructure, then let ArgoCD in the cloud cluster sync the same manifests with cloud overlays.
5. **Teardown:** destroy cloud resources when idle; record the cost in `11-memory.md`.

Never change the cluster by hand. If a manual change is needed to investigate, revert it and commit the real fix.

## 4. Post-launch plan

| Area | Plan |
| --- | --- |
| Monitoring | Keep dashboards and alerts on ingestion freshness, API errors and forecast age |
| Maintenance | Monthly dependency updates; yearly review of the NOAA product version `[TO DEFINE]` |
| Feedback | Collect comments from CoraMar or reviewers if they engage; log them in `11-memory.md` |
| Technical debt | Keep a short list in `11-memory.md`; schedule it after each stage |
| Cost | Cloud environment is created for demos and destroyed afterwards |
| Retrospective | After each stage, write what worked, what failed and what was learned |
| Portfolio | After M1 and again after M4, update the README, the CV and the LinkedIn featured section |

## Open questions

- [ ] Run F5 before F3 and F4, or after?
- [ ] License confirmation (repository name decided: Atalaya-Coral).
- [ ] Cloud region and cost limit.

## Related documents

[00-spec.md](00-spec.md) · [02-trd.md](02-trd.md) · [03-architecture.md](03-architecture.md) · [10-tasks.md](10-tasks.md) · [11-memory.md](11-memory.md)
