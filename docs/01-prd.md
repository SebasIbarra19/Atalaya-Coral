---
titulo: Product Requirements Document (PRD)
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.1
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: [00-spec.md]
---

# Product Requirements Document (PRD)

## 1. Product summary

A web platform that ingests daily NOAA Coral Reef Watch satellite data for Costa Rican reef sites, forecasts their thermal stress with machine learning, and explains the result in plain language. It is a learning and portfolio project. It does not replace official NOAA alerts.

## 2. Problem and opportunity

Thermal stress anticipates coral bleaching. NOAA publishes the data, but in formats for scientists and not tied to local sites. There are academic forecasting models and few open, operational platforms. The opportunity is a complete, documented system on a real domain that a non-technical person can read. (See `00-spec.md`, section 1.)

## 3. Target users

| User | Need |
| --- | --- |
| Conservation practitioner | Know which sites are at risk and how far ahead, without raw data |
| Researcher | History, forecasts with uncertainty, and the reasons behind each prediction |
| Operator (owner) | Know that ingestion, model and cluster work, and hear about failures first |
| Technical reviewer | Understand, run and evaluate the project quickly |

User stories HU-1 to HU-8 are defined in `00-spec.md`, section 4, and are not repeated here.

## 4. Product functions

IDs match the specification so traceability stays simple. Priority uses MoSCoW: Must, Should, Could, Won't now. Acceptance criteria are written to be verified.

| ID | Function | Description | Priority | Acceptance criteria |
| --- | --- | --- | --- | --- |
| RF-1 | Daily NOAA ingestion | Download SST, anomaly, HotSpot, DHW and alert level for each defined site | Must | After a run, a row exists per site for the latest available date; missing days are flagged, not silently skipped |
| RF-2 | Idempotent ingestion | Retries, no duplicates, run log | Must | Running the job twice for the same date leaves identical row counts; every run writes a record with start, end, rows and errors |
| RF-3 | Historical load | Backfill history for training | Must | History from the chosen start year is present for every site and a coverage report shows gaps `[start year TO DEFINE; reference study: 1985 to 2024]` |
| RF-4 | Site catalog | Editable list of sites with name and coordinates | Must | A site can be added or changed and the next ingestion picks it up without code changes |
| RF-5 | Read API | Current status, history and forecast per site | Must | Each endpoint in `04-api-guide.md` returns the documented format and passes its contract tests |
| RF-6 | Dashboard | List or map of sites, alert level and series per site | Must | A user sees every site's latest alert level and a time series, with loading, empty and error states |
| RF-7 | Baseline model | Simple persistence-style baseline | Must | Baseline metrics are computed on a held-out period and stored |
| RF-8 | XGBoost forecast with SHAP | Forecast at one or more horizons with explanations | Must | Forecast beats the baseline on the held-out period; each forecast exposes its top contributing factors |
| RF-9 | Temporal validation | No training on future data | Must | An automated test fails if any training row is later than the first evaluation row |
| RF-10 | MLOps | Tracked training runs, scheduled retraining, drift detection | Should | Every training run is recorded with parameters, metrics and artifacts; a drift check runs on schedule and reports a result |
| RF-11 | Alert notifications | Notify when a site's alert level rises | Should | A simulated rise produces exactly one notification through the chosen channel `[channel TO DEFINE]` |
| RF-12 | Domain agent | Explains a site's status in plain language | Should | Answers use only database data, cite the site and date, and refuse questions outside the data; passes the evaluation set in `08-testing-guide.md` |
| RF-13 | Operations agent | Investigates an alert using metrics, logs and the Kubernetes API | Should | For a provoked failure, the agent returns a probable cause using read-only access |
| RF-14 | One-command startup | Start everything locally | Must | On a clean clone, the documented command starts the system and the README steps are enough |

## 5. Main user flows

**Check a site's status (HU-1)**

1. The user opens the dashboard.
2. The system shows the list or map of sites with their latest alert level.
3. The user selects a site.
4. The system shows the series and the forecast with its explanation.

**Ask why a site is at risk (HU-3)**

1. The user opens the explanation panel for a site.
2. The user asks a question in plain language.
3. The agent reads the site's data and replies, citing site and date.
4. If the question is outside the data, the agent says so.

**Investigate a failed ingestion (HU-6, HU-7)**

1. An alert fires on a missing day or a failed run.
2. The operator opens the observability dashboards.
3. The operations agent proposes a probable cause from metrics, logs and cluster state.
4. The operator verifies and fixes it.

## 6. Out of scope

- The jiu-jitsu app as a workload of this platform.
- Scientific or operational use of the forecast.
- Multi-region high availability and production-grade cloud costs.
- User accounts and personalization (Proposed, since all data is public).

## 7. Product success metrics

| Metric | Target |
| --- | --- |
| Ingestion freshness | Latest NOAA date available is in the database `[target TO MEASURE after first month of runs]` |
| Forecast skill | Beats the baseline on the held-out period |
| Agent accuracy | Passes the evaluation set with no invented figures |
| Reviewer experience | A reviewer starts the project from the README alone |

## 8. Assumptions, dependencies and constraints

- NOAA data stays publicly available at the same endpoints `[TO VERIFY]`.
- Available hours vary by semester, so there are no dates.
- Budget is close to zero: local first, cloud with Student Pack credits.
- The agents depend on a language model: a small open-weight model served locally by Ollama (Proposed, exact model chosen in F7 by evaluations).

## 9. Releases

| Release | Contents |
| --- | --- |
| v0.1 | Core: RF-1 to RF-6 and RF-14 |
| v0.2 | Forecast: RF-7 to RF-9 |
| v0.3 | MLOps and notifications: RF-10, RF-11 |
| v0.4 | Agents: RF-12, RF-13 |
| v1.0 | Everything running in the cloud with Terraform |

## Open questions

- [ ] Which Costa Rican sites are included?
- [ ] Which forecast horizon is prioritized?
- [ ] Which notification channel?
- [ ] From which year is history loaded?

## Related documents

[00-spec.md](00-spec.md) · [02-trd.md](02-trd.md) · [04-api-guide.md](04-api-guide.md) · [08-testing-guide.md](08-testing-guide.md) · [10-tasks.md](10-tasks.md)
