---
titulo: Project Specification
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.2
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: []
---

# Project Specification

This is the parent document. It answers "why" and "what" at a high level. Detail lives in the PRD, TRD and the other documents, and those link back here instead of copying it.

> Source of truth: this Markdown file replaces the first Spanish working draft that lived in Claude Docs. If the two ever disagree, this file wins.

## 1. Vision and problem

The platform downloads public satellite data from NOAA Coral Reef Watch, forecasts the thermal stress of Costa Rican reef sites with machine learning, and explains the result to non-technical people. It runs on reproducible infrastructure (containers, Kubernetes, GitOps) with full observability.

**The problem.** Accumulated thermal stress anticipates coral bleaching. NOAA publishes the data daily at 5 km, but in formats designed for scientists and not tied to the sites a local organization cares about. Academic models exist, for example Arcodia, Karp and Barnes (2025) for 3 sites in Florida, but there are almost no open, operational platforms in this domain.

**Dual purpose.** As a product, a tool that could be useful to CoraMar if they ever want it (the project stays independent for now). As a portfolio piece, one project that demonstrates data engineering, ML, DevOps, security and AI agents on a real domain.

## 2. Goals and success criteria

The project succeeds if an outsider can start it with one command, see the forecast for a Costa Rican site, and understand why each decision was made. It does not aim to beat the state of the art in ML. It aims for a complete, honest and well-documented system.

| Type | Goal | Met when |
| --- | --- | --- |
| Product | Automatic daily ingestion of NOAA data for Costa Rican sites | Yesterday's data is in the database with no manual step |
| Product | Thermal-stress forecast: baseline model, then XGBoost with SHAP | Metrics beat a trivial model (persistence) on held-out data |
| Product | An agent that explains a site's status to non-technical people | It answers only from real data and passes an evaluation set |
| Operations | Reproducible startup and a CI pipeline | A clean clone starts on another machine following only the README |
| Learning | Move from theory to practice in Kubernetes, GitOps, observability and MLOps | The owner can explain and rebuild each piece without AI help |
| Portfolio | README with diagram, decisions and lessons learned | A recruiter understands the project within a few minutes |

## 3. Scope

The core and Branch A are the minimum deliverable. Branches B and C are added in that order. Branch D only if time remains.

| Module | What it includes | Priority |
| --- | --- | --- |
| Core | NOAA ingestion through ERDDAP, PostgreSQL database, read API, simple dashboard, Docker Compose and CI | Required |
| Branch A: forecast | Baseline model, then XGBoost with SHAP, replicating the approach of Arcodia et al. (2025) for Costa Rica | Required |
| Branch B: MLOps | Experiment tracking, scheduled retraining and drift detection | After A |
| Branch C: agents | HolmesGPT for operations and an own domain agent that explains reef status: read-only tools through an MCP server, retrieval over reference documents (RAG with pgvector), structured outputs, guardrails, evaluations and LLM observability | After B |
| Platform | Local Kubernetes, GitOps with ArgoCD, observability (Prometheus, Grafana, Loki, OpenTelemetry), then cloud with Terraform | In layers, alongside the phases |
| Branch D: optional | Simulated sensors in streaming | Only if time remains |

**Out of scope**

- The jiu-jitsu app as a workload of this platform (decided: it lives separately).
- Scientific or operational use of the forecast. This is a learning and portfolio project and does not replace official NOAA alerts (Proposed).
- Multi-region high availability and production-grade cloud costs (Proposed).

## 4. Users and user stories

| User | What they need |
| --- | --- |
| Conservation practitioner (for example at an NGO) | To know which sites are at risk and how far ahead, without reading raw data |
| Researcher | Historical series, forecasts with their uncertainty, and the factors behind each prediction |
| Operator (the system owner) | To know whether ingestion, model and cluster are working, and to hear about failures first |
| Technical reviewer (recruiters and mentors) | To understand the project, run it, and see reasoned decisions |

| ID | As a | I want | So that |
| --- | --- | --- | --- |
| HU-1 | Conservation practitioner | To see the current alert level of each site | I can prioritize field monitoring |
| HU-2 | Conservation practitioner | To be notified when a site moves to a higher alert level | I can act in time |
| HU-3 | Conservation practitioner | To ask in plain language why a site is at risk | I can understand without technical knowledge |
| HU-4 | Researcher | To query history and download data by site and date | I can analyze it myself |
| HU-5 | Researcher | To see the forecast with its error margin and main factors (SHAP) | I can trust or doubt it with judgment |
| HU-6 | Operator | To see dashboards and health alerts | I can detect ingestion or model failures |
| HU-7 | Operator | An agent that investigates an alert and proposes a probable cause | I save diagnosis time |
| HU-8 | Technical reviewer | To start everything with one command and see a diagram and the decisions | I can evaluate the work quickly |

## 5. Functional requirements (high level)

Detail and acceptance criteria live in `01-prd.md`. Sites and forecast horizon are still to be defined.

| ID | Module | Requirement | Story |
| --- | --- | --- | --- |
| RF-1 | Core | Download daily from ERDDAP the NOAA variables (sea surface temperature, anomaly, HotSpot, DHW and alert level) for the defined sites | HU-1 |
| RF-2 | Core | Idempotent ingestion: with retries, no duplicate data and a record of every run | HU-6 |
| RF-3 | Core | Historical load for training (the reference study uses 1985 to 2024) | HU-4 |
| RF-4 | Core | Editable site catalog with name and coordinates | HU-1 |
| RF-5 | Core | Read API: current status, historical series and forecast per site | HU-1, HU-4 |
| RF-6 | Core | Dashboard with the list or map of sites, their alert level and each site's series | HU-1 |
| RF-7 | A | Simple baseline model (for example, persistence) as a point of comparison | HU-5 |
| RF-8 | A | XGBoost with SHAP explanation; horizon to be defined (the reference study reaches 6 weeks) | HU-5 |
| RF-9 | A | Temporal validation: never train on data later than the data being evaluated | HU-5 |
| RF-10 | B | Record every training run (parameters, metrics, artifacts), retrain on a schedule and detect data drift | HU-6 |
| RF-11 | B | Notify when a site moves to a higher alert level | HU-2 |
| RF-12 | C | Domain agent that answers about a site using only database data, cites its source and does not invent | HU-3 |
| RF-13 | C | Operations agent (HolmesGPT) that investigates an alert by reading metrics, logs and the Kubernetes API | HU-7 |
| RF-14 | Core | Full local startup with a single command | HU-8 |

## 6. Non-functional requirements (high level)

Numeric targets are set once a first measurement exists, not before. Detail lives in `02-trd.md`.

| Category | Requirement | Verified by |
| --- | --- | --- |
| Reproducibility | The whole system starts from scratch with one command, no hidden manual steps | A clean clone on another machine, following only the README |
| Infrastructure as code | Containers, Kubernetes manifests and Terraform versioned in Git | Nothing is configured by hand in the cluster |
| Security | No secrets in the repository, least privilege, secret scanner in CI | gitleaks and review before each publication |
| Observability | Metrics, logs and traces for each service, with alerts on ingestion and the model | Dashboards and a provoked failure that raises an alert |
| Reliability | Ingestion tolerates network failures and missing data without corrupting the database | Tests with simulated failures |
| Data quality | Validate ranges and dates before storing, and warn if a day arrives empty | Automated tests and a missing-data alert |
| ML quality | Temporal evaluation and comparison with a baseline; reproducible results with fixed seeds | Versioned metrics report |
| Cost | The local version costs nothing; the cloud uses the AWS free plan only, never a paid plan, and is destroyed when done | AWS Budgets alert and a console review after each session |
| Maintainability | Layered code, automated tests, CI on every change and recorded decisions | Green CI and an up-to-date decisions folder |
| Agent safety | The agent only reads data, performs no destructive actions and has usage limits | Evaluations and read-only permissions |

## 7. Architecture and data (summary)

Data enters through a daily ingestion job, is stored in PostgreSQL, and feeds the forecast, the API and the agents. Everything runs in a cluster and is deployed from Git. The core is: ingestion, database, API and dashboard. The rest is added by branch and by platform layer. The full diagram and detail live in `03-architecture.md`.

Initial data model (Proposed): `sites`, `observations`, `forecasts`, `ingestion_runs`.

## 8. Stack and decisions

Four choices are decided. The rest are proposals confirmed when each phase is reached. Each important decision is recorded in the repository (`docs/decisions/`) with its discarded alternatives.

| Layer | Choice | Status | Alternative and why not |
| --- | --- | --- | --- |
| Data source | NOAA Coral Reef Watch 5 km, through ERDDAP | Decided | Own data: does not exist yet |
| Model | XGBoost with SHAP, replicating Arcodia et al. (2025), starting from a baseline | Decided | Neural networks: more complex and less explainable at this data size (Proposed) |
| Environment | Local cluster first, cloud afterwards | Decided | Cloud from the start: adds billing risk while learning |
| Operations agent | HolmesGPT | Decided | k8sgpt: another LLM-based option to compare later |
| Data and ML language | Python | Proposed | R: not the owner's stack |
| Database | PostgreSQL | Proposed | A specialized time-series database: evaluated if volume demands it |
| Scheduled ingestion | Kubernetes CronJob | Proposed | Airflow: too heavy for one daily task |
| API | FastAPI | Proposed | Next.js API routes: would mix data and presentation |
| Dashboard | Next.js | Proposed | Streamlit or Grafana: fast, but show less of the owner's own code |
| ML tracking | MLflow | Proposed | Loose files: no comparable history |
| Containers and local cluster | Docker, and kind or k3d | Proposed | Minikube: heavier |
| GitOps | ArgoCD | Proposed | Flux: valid alternative, may be compared later |
| Observability | Prometheus, Grafana, Loki and OpenTelemetry | Proposed | Paid services: outside the budget |
| Infrastructure as code | Terraform | Proposed | Pulumi: valid, but Terraform appeared among the skills seen in job postings |
| Cloud provider | AWS on the free plan, only in F8 (ADR-010) | Decided | Azure through the Student Pack: AWS appears more often in the job postings reviewed |
| CI | GitHub Actions | Proposed | Other providers: already in use |
| Language model | Small open-weight model served by Ollama on the host machine; exact model chosen in F7 by evaluations (ADR-006) | Proposed | Paid API by default: billing risk; may be compared later only with a provider spend limit |
| Agent tools | MCP server exposing read-only tools (ADR-007) | Proposed | Data pasted into the prompt: harder to control and evaluate |
| Document retrieval | pgvector in the same PostgreSQL (ADR-007) | Proposed | A separate vector database: one more service for little data |
| Model adaptation | RAG and prompting, no fine-tuning (ADR-007) | Proposed | Fine-tuning: there is no training set and the data changes daily |
| LLM observability | Arize Phoenix, built on OpenTelemetry (ADR-008) | Proposed | Langfuse self-hosted: needs several extra services, too heavy for the laptop |
| Documentation language | English | Decided | Spanish: less readable for international recruiters |
| Relationship with CoraMar | Independent for now | Decided | Connected from the start: depends on their answer |
| License | MIT | Proposed | Apache 2.0: adds patent clause, not needed here |
| Project name | To be defined | Open | Use a working title in the documents |

## 9. Phased plan

There are no dates: since available hours vary by semester, each phase is measured by its exit gate. Phase 0 is the documentation.

| Stage | Phases | Exit gate |
| --- | --- | --- |
| 1. Core | F0 Repo and documents, F1 Ingestion and database, F2 API and dashboard | The core starts with a single command |
| 2. Platform | F3 Kubernetes and GitOps, F4 Observability | A change in Git is deployed and visible on the dashboards |
| 3. ML and agents | F5 Forecast (A), F6 MLOps (B), F7 Agents (C) | Retrainable model and evaluated agent |
| 4. Cloud | F8 Cloud with Terraform | It is created and destroyed with Terraform |

The core and Branch A (F5) are the minimum deliverable. Per-phase deliverables and mentor modes live in `09-implementation-plan.md` and `10-tasks.md`.

## 10. Risks, assumptions and open questions

| Risk | Mitigation |
| --- | --- |
| Scope is larger than the available time | Core plus Branch A is a publishable project on its own; B and C are added without breaking it |
| Using AI without actually learning | Mentor mode per phase, and the test of explaining and rebuilding each piece without help |
| ERDDAP or NOAA product changes or outages | Keep a local copy of what is downloaded and test with sample data |
| A 5 km pixel can be coarse for small coastal reefs (to verify) | Review candidate sites before training |
| The model gives modest results | Success is measured by the complete system and an honest comparison against the baseline |
| Unexpected cloud costs | Local first; AWS account created only when F8 starts, free plan only; AWS Budgets alert; destroy with Terraform after each session; avoid services that bill silently (NAT Gateway, load balancers, forgotten instances) |
| Free plan or Student Pack benefits that expire | Activate each one only when it is going to be used |
| The agent invents answers | It only reads database data, cites its source and is evaluated before publishing |
| The laptop runs out of memory with the whole stack | Compose profiles, only the services in use run, WSL2 memory capped (ADR-009) |

**Assumption.** NOAA data stays publicly available at the same endpoints. `[TO VERIFY]`

**Open questions**

- [ ] Which Costa Rican sites are included?
- [ ] What forecast horizon is prioritized (weeks)?
- [ ] What is the project and repository name?
- [ ] How are alerts delivered (email, webhook or other)?
- [ ] Is a second documentation language needed later (Spanish summary)?

## 11. Sources and glossary

Sources collected on 2026-10-10.

- [NOAA Coral Reef Watch, 5 km products](https://coralreefwatch.noaa.gov/product/5km/)
- [ERDDAP, dhw_5km dataset](https://upwell.pfeg.noaa.gov/erddap/griddap/dhw_5km.html)
- [Summary of the study by Arcodia, Karp and Barnes (2025)](https://ecomagazine.com/news/coastal/new-ai-model-can-assist-with-early-warning-for-coral-bleaching-risk/)
- [HolmesGPT, operations agent](https://themenonlab.blog/blog/ai-error-monitoring-agent-open-source)
- [OpenTelemetry Demo](https://github.com/open-telemetry/opentelemetry-demo)
- [mlops-airflow-on-eks, structure reference with Terraform](https://github.com/seblum/mlops-airflow-on-eks)
- [machine-learning-mlops, MLOps reference with MLflow](https://github.com/JIAZHEN/machine-learning-mlops)

| Term | Meaning |
| --- | --- |
| ERDDAP | Scientific data server that lets you request subsets by URL |
| SST | Sea surface temperature |
| HotSpot | How much the temperature exceeds the maximum of the warmest month of the average year |
| DHW | Degree Heating Weeks: accumulated heat stress over the last weeks |
| SHAP | Method that explains how much each variable contributed to a prediction |
| GitOps | Operating infrastructure from Git, where the repository is the source of truth |
| MLOps | Practices to train, deploy and monitor models in a repeatable way |
| Data drift | Change in input data that degrades a model over time |
| ADR | Short record of a technical decision with its alternatives |

## Open questions

See section 10.

## Related documents

[01-prd.md](01-prd.md) · [02-trd.md](02-trd.md) · [03-architecture.md](03-architecture.md) · [09-implementation-plan.md](09-implementation-plan.md) · [11-memory.md](11-memory.md)
