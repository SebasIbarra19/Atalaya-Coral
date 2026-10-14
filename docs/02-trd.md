---
titulo: Technical Requirements Document (TRD)
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.1
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: [00-spec.md, 01-prd.md, 03-architecture.md]
---

# Technical Requirements Document (TRD)

Translates the PRD into measurable technical requirements. Numeric targets marked `[TO MEASURE]` are set after a first measurement, not before.

## 1. Technical scope and context

In scope: ingestion, storage, forecasting, read API, dashboard, agents, observability, GitOps and cloud deployment with Terraform. Out of scope: everything listed as out of scope in `00-spec.md`. The system handles only public data and has no user accounts (Proposed).

## 2. Functional technical requirements

| ID | PRD function | Technical requirement |
| --- | --- | --- |
| TR-1 | RF-1 | The ingestion job requests ERDDAP by site coordinates and date range and handles a missing or late day by recording it, not by failing the whole run |
| TR-2 | RF-2 | Writes are upserts keyed by (site_id, date). A run record is written for every execution, including failed ones |
| TR-3 | RF-3 | A backfill command loads history in bounded chunks, can resume after interruption and reports coverage per site |
| TR-4 | RF-4 | Sites are rows in `sites`; ingestion reads the active ones at start. Changes are made through the admin endpoint or a migration |
| TR-5 | RF-5 | The API is read-only for data, versioned under `/v1`, and documented through an OpenAPI schema generated from code |
| TR-6 | RF-6 | The dashboard consumes only the API and renders loading, empty and error states |
| TR-7 | RF-7, RF-8 | Training uses a fixed random seed, and every run stores parameters, metrics, data window and model version |
| TR-8 | RF-9 | A test asserts that the latest training timestamp is earlier than the first evaluation timestamp |
| TR-9 | RF-10 | Retraining and a drift check run on a schedule and write their results to MLflow and to metrics |
| TR-10 | RF-11 | Alert-level transitions are detected by comparing consecutive observations and de-duplicated per site and level |
| TR-11 | RF-12 | The domain agent has read-only access, a system prompt that forbids unsupported claims, and a per-request data context limited to the requested site |
| TR-12 | RF-13 | HolmesGPT runs with a read-only Kubernetes service account and read-only access to Prometheus and Loki |
| TR-13 | RF-14 | `make up` starts the core; `make test` runs the test suite; both are documented and tested in CI on a clean runner |

## 3. Non-functional requirements

| ID | Category | Requirement | Target | Verified by |
| --- | --- | --- | --- | --- |
| NFR-1 | Reproducibility | Clean-clone startup uses only documented steps | `[TO MEASURE]` minutes on a clean machine | Fresh clone test in CI |
| NFR-2 | Reliability | Ingestion is idempotent | Re-running a date changes zero rows | Automated test |
| NFR-3 | Reliability | Ingestion survives network errors | Retries with backoff, run recorded as failed if exhausted | Test with simulated failures |
| NFR-4 | Data quality | Values outside valid ranges are rejected and logged | Ranges `[TO DEFINE from NOAA documentation]` | Unit tests |
| NFR-5 | Data quality | An empty day raises an alert | Alert fires within the next scheduled check | Provoked missing day |
| NFR-6 | Performance | API read latency | `[TO MEASURE]` baseline first, then set a target | Load check on the local cluster |
| NFR-7 | ML quality | Forecast beats the baseline | Better than persistence on held-out period | Versioned metrics report |
| NFR-8 | Security | No secrets in the repository | Zero findings | gitleaks in CI |
| NFR-9 | Security | Least privilege per component | Read-only roles where possible | Review against `05-security-guide.md` |
| NFR-10 | Observability | Every service exposes health and basic metrics | 100% of services | Dashboard review |
| NFR-11 | Cost | Cloud spending stays within credits | Budget alert configured | Cloud cost report |
| NFR-12 | Maintainability | CI runs on every change | Lint, type check, tests and build | Green pipeline required to merge |

## 4. Interfaces and external integrations

| System | Direction | Interface | Notes |
| --- | --- | --- | --- |
| NOAA ERDDAP | Inbound | HTTPS, griddap dataset `dhw_5km` | Endpoint and variables `[TO VERIFY]` |
| GitHub | Both | Git, Actions | Source of truth and CI |
| Azure | Outbound | Terraform provider | Only in phase F8 |
| Language model provider | Outbound | HTTPS API | `[TO DEFINE in Branch C]` |
| Notification channel | Outbound | Email or webhook | `[TO DEFINE]` |

## 5. Data model and retention

The initial model is in `03-architecture.md`, section 7. All data is public, so there are no privacy retention requirements. Observations and forecasts are kept indefinitely (Proposed). Forecasts are never overwritten: a new forecast is a new row.

## 6. Infrastructure and environments

| Environment | Requirements |
| --- | --- |
| Local core | Docker and Docker Compose |
| Local cluster | kind or k3d, ArgoCD, Prometheus, Grafana, Loki, OpenTelemetry collector |
| Cloud | Azure through Terraform; shut down when idle; budget alert |

Deployment is declarative: the cluster is synced from Git by ArgoCD. Nothing is configured by hand in the cluster.

## 7. Constraints and technical assumptions

- Personal laptop resources limit how many services run at once locally.
- Available hours vary, so work is split into small tasks (see `10-tasks.md`).
- NOAA data stays available at the same endpoints `[TO VERIFY]`.
- The reference study covers 3 Florida sites; Costa Rican sites may behave differently `[TO VERIFY]`.

## 8. Technical risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 5 km pixel too coarse for a small reef | Poor forecasts for some sites | Review candidate sites before training |
| ERDDAP outage or schema change | Ingestion fails | Local copy, contract tests on the NOAA response shape |
| Local machine too small for the whole stack | Slow or crashing cluster | Start services by phase; use lighter configuration |
| Agent returns unsupported statements | Wrong guidance to a user | Read-only data context, citations, evaluation set |
| Cloud costs | Credits exhausted | Local first, destroy resources, budget alert |

## 9. Technical acceptance criteria

| Requirement | Accepted when |
| --- | --- |
| TR-1 to TR-4 | Ingestion and catalog tests pass and a clean run fills the database |
| TR-5, TR-6 | Contract tests pass and the dashboard shows all states |
| TR-7, TR-8 | The metrics report is versioned and the leakage test passes |
| TR-9, TR-10 | Scheduled jobs run and produce recorded results |
| TR-11, TR-12 | The agent evaluation set passes and permissions are verified read-only |
| TR-13 | The one-command startup works on a clean runner |

## Open questions

- [ ] Exact NOAA variable names, units and valid ranges.
- [ ] Target API latency after a first measurement.
- [ ] Notification channel.

## Related documents

[00-spec.md](00-spec.md) · [01-prd.md](01-prd.md) · [03-architecture.md](03-architecture.md) · [05-security-guide.md](05-security-guide.md) · [08-testing-guide.md](08-testing-guide.md)
