---
titulo: API Guide
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.1
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: [01-prd.md, 02-trd.md, 03-architecture.md]
---

# API Guide

The read API serves sites, history and forecasts. Everything here is Proposed until the API is built. Values marked `[TO MEASURE]` are set after a first measurement.

## 1. Base configuration

| Item | Value |
| --- | --- |
| Base URL (local) | `http://localhost:8000/v1` |
| Base URL (cloud) | `[TO DEFINE]` |
| Versioning | Path prefix (`/v1`). Breaking changes create `/v2` |
| Format | JSON, UTF-8 |
| Dates | ISO 8601 (`2026-10-14` for dates, `2026-10-14T06:00:00Z` for timestamps, UTC) |
| Documentation | OpenAPI schema generated from code, served at `/docs` |

## 2. Authentication and authorization

| Endpoint group | Access | Notes |
| --- | --- | --- |
| Read endpoints | Public, no credential (Proposed, since the data is public) | Protected by rate limits |
| Admin endpoints (site catalog changes) | API key in the `Authorization` header | Key stored as a secret, never in the repository |
| Health and metrics | Cluster-internal only | Not exposed publicly |

If a public deployment later needs accounts, this section is revised and the change is logged in `11-memory.md`.

## 3. Common headers

| Header | Direction | Required | Purpose |
| --- | --- | --- | --- |
| `Accept: application/json` | Request | Yes | Response format |
| `Authorization: Bearer <api-key>` | Request | Admin endpoints only | Admin authentication |
| `X-Request-ID` | Request and response | Optional in, always out | Correlates a request across logs and traces |
| `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` | Response | Always | Current rate limit state |
| `Retry-After` | Response | On 429 and 503 | Seconds before retrying |
| `Cache-Control` | Response | Read endpoints | How long a response may be cached |

## 4. Endpoint structure

Conventions: plural nouns, lowercase, kebab-case when multi-word, no verbs in paths, nesting only one level deep.

| Method | Path | Description | Auth | Requirement |
| --- | --- | --- | --- | --- |
| GET | `/sites` | List sites with their latest alert level | Public | RF-1, RF-5 |
| GET | `/sites/{site_id}` | One site with its latest observation | Public | RF-5 |
| GET | `/sites/{site_id}/observations` | History by date range | Public | RF-4, RF-5 |
| GET | `/sites/{site_id}/forecasts` | Latest forecast, optionally by horizon | Public | RF-8 |
| GET | `/sites/{site_id}/forecasts/{forecast_id}/explanation` | SHAP factors of a forecast | Public | RF-8 |
| POST | `/admin/sites` | Create a site | API key | RF-4 |
| PATCH | `/admin/sites/{site_id}` | Update or deactivate a site | API key | RF-4 |
| GET | `/health` | Liveness and readiness | Internal | NFR-10 |

## 5. Request and response format

**Collection response**

```json
{
  "data": [
    { "id": "site-001", "name": "Example site", "alert_level": "watch", "as_of": "2026-10-14" }
  ],
  "meta": { "count": 1, "next_cursor": null }
}
```

**Single resource response**

```json
{
  "data": {
    "id": "site-001",
    "name": "Example site",
    "latitude": 0.0,
    "longitude": 0.0,
    "latest": { "date": "2026-10-14", "sst": 0.0, "dhw": 0.0, "alert_level": "watch" }
  }
}
```

The values above are placeholders, not real data.

**Pagination.** Cursor-based: `?limit=100&cursor=<opaque>`. Default and maximum limit `[TO DEFINE]`.

**Filtering and ordering.** Date range with `?from=2026-01-01&to=2026-03-31`. Ordering by date ascending by default; `?order=desc` reverses it.

## 6. Error handling

A single error format for every failure:

```json
{
  "error": {
    "code": "site_not_found",
    "message": "No site with id site-999.",
    "request_id": "<id>",
    "details": []
  }
}
```

| Status | Code examples | Retry | Meaning |
| --- | --- | --- | --- |
| 400 | `invalid_parameter` | No | Malformed or out-of-range parameter |
| 401 | `missing_credentials`, `invalid_credentials` | No | Admin credential missing or wrong |
| 403 | `forbidden` | No | Credential lacks permission |
| 404 | `site_not_found` | No | Resource does not exist |
| 409 | `site_exists` | No | Conflict with an existing resource |
| 422 | `validation_error` | No | Body fails validation |
| 429 | `rate_limited` | Yes, after `Retry-After` | Too many requests |
| 500 | `internal_error` | Yes, with backoff | Unexpected server error; never exposes internals |
| 503 | `unavailable` | Yes, after `Retry-After` | Dependency down or starting |

Messages are written for humans and never include stack traces, SQL or secrets.

## 7. Rate limits

| Scope | Limit | Notes |
| --- | --- | --- |
| Read endpoints, per client IP | `[TO MEASURE]` | Set after a baseline; start conservative |
| Admin endpoints, per key | `[TO MEASURE]` | Lower than read limits |

The limit is enforced at the ingress or in the API and always reported through the `RateLimit-*` headers.

## 8. Best practices

- **Idempotency.** GET is safe and repeatable. Admin writes use PATCH or PUT semantics so repeats are harmless.
- **Compatibility.** Adding fields is not breaking; removing or renaming them is.
- **Caching.** Observations change once a day, so responses can carry a short `Cache-Control` `[TO DEFINE]`.
- **Validation.** Validate every parameter; reject unknown ones for admin endpoints.
- **Contract tests.** Each endpoint has a test that checks the documented format.
- **Documentation.** The OpenAPI schema is the contract; this guide explains conventions, not every field.
- **No secrets in URLs.** Credentials go in headers.

## Open questions

- [ ] Public cloud base URL and whether read endpoints stay public.
- [ ] Pagination limits.
- [ ] Rate limit values after measurement.

## Related documents

[01-prd.md](01-prd.md) · [02-trd.md](02-trd.md) · [03-architecture.md](03-architecture.md) · [05-security-guide.md](05-security-guide.md) · [08-testing-guide.md](08-testing-guide.md)
