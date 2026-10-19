---
titulo: Security Guide
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.1
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: [02-trd.md, 03-architecture.md, 04-api-guide.md]
---

# Security Guide

## 1. Purpose and scope

This guide defines how the platform is kept safe, even though it only handles public data. The project is public and a portfolio piece, so good security practice is part of what it demonstrates. It covers the repository, the services, the agents, the cluster and the cloud.

## 2. Fundamental principles

1. **Least privilege.** Every component gets the minimum access it needs, and read-only wherever possible.
2. **Defense in depth.** No single control is trusted alone. Check at more than one layer.
3. **Secure by default.** New components start closed and are opened deliberately.
4. **Never trust the client.** Validate all input at the server, including dashboard and agent input.
5. **Secrets stay out of code.** Anything secret lives in a secret store or environment, never in Git.
6. **Fix what you find.** Do not publish a description of a weakness that is still open.

## 3. Authentication and authorization

| Area | Rule |
| --- | --- |
| Public read endpoints | No credential; protected by rate limits (see `04-api-guide.md`) |
| Admin endpoints | API key, checked on every request in the API layer, not only at the ingress |
| Database roles | Separate roles: ingestion (write observations), training (write forecasts), API (read-only) |
| Kubernetes | One service account per workload; HolmesGPT and the domain agent get read-only roles |
| GitHub | Branch protection on the main branch; no direct pushes `[TO CONFIGURE in F0]` |
| Cloud | Separate cloud identity for Terraform; no personal admin credentials inside the cluster |

## 4. Environment and secrets

- Environment variables hold configuration. A `.env.example` lists names with fake values.
- Real `.env` files are in `.gitignore` and never committed.
- A secret scanner (gitleaks) runs in CI and as a pre-commit hook.
- A leaked secret is revoked and rotated first, and only then removed from history.
- In the cluster, secrets come from a secret mechanism `[TO DEFINE: Kubernetes Secrets, Sealed Secrets or External Secrets]`, never from manifests in plain text.
- Documents in this repository never contain real keys, tokens or passwords.

## 5. Data protection

| Topic | Rule |
| --- | --- |
| Classification | All data is public NOAA data (Proposed); there is no personal data |
| In transit | HTTPS for every external connection; TLS between services in the cloud `[TO DEFINE]` |
| At rest | Cloud disks encrypted by default; local development has no extra requirement |
| Backups | Database dump scheduled in the cloud environment `[TO DEFINE]` |
| Logs | Never log secrets, tokens or full request bodies from agents |

If the project ever stores personal data (for example user accounts), this section is revised before building it.

## 6. API and backend security

- Validate every parameter and body with explicit schemas; reject unknown fields on writes.
- Use parameterized queries only; no SQL built by string concatenation.
- Rate limit all endpoints and return the standard error format without internals.
- Configure CORS with an explicit allow list of origins `[TO DEFINE]`.
- Set security headers on the dashboard (CSP, no sniffing, frame restrictions).
- Run containers as a non-root user and keep images minimal.
- Agent-specific rules: the domain agent has no write tools; user text is treated as untrusted; answers cite data; the system prompt and tool list are versioned; usage limits are enforced. Tools exist only in the MCP server, as a fixed allowlist of read-only tools. Retrieved documents are untrusted data, like user text (prompt injection). Model output is validated against a schema before it reaches the dashboard. Ollama is reachable only from the local machine and the cluster, never from the network.

## 7. Dependencies

- Pin versions and commit lockfiles.
- Enable automated update proposals (Dependabot or Renovate `[TO DEFINE]`).
- Run dependency audits in CI (`pip-audit`, `npm audit` or equivalents).
- Review the base images of containers and rebuild periodically.
- Prefer maintained projects; record why each major dependency was chosen in an ADR.

## 8. Incident reporting and response

The project has one owner, so the process is short.

| Step | Action |
| --- | --- |
| Detect | An alert, a CI finding or an external report through the repository's security contact `[TO DEFINE]` |
| Contain | Revoke exposed credentials, disable the affected endpoint or workload |
| Fix | Patch, add a test that would have caught it |
| Record | Add an entry to `11-memory.md` and, if useful, a short post-mortem in `docs/decisions/` |
| Learn | Update this guide if a rule was missing |

## 9. Pre-release security checklist

- [ ] Secret scan passes and no `.env` is tracked.
- [ ] Dependency audit shows no unreviewed high-severity findings.
- [ ] Admin endpoints require the key and fail closed.
- [ ] Database roles are least-privilege and the API role is read-only.
- [ ] Containers run as non-root.
- [ ] Agents have read-only access and their evaluations pass.
- [ ] Cloud resources have a budget alert and an owner.
- [ ] No weakness described in the docs is still open.

## Open questions

- [ ] Secret mechanism in the cluster.
- [ ] Security contact for external reports.
- [ ] Dependency update tool.

## Related documents

[02-trd.md](02-trd.md) · [03-architecture.md](03-architecture.md) · [04-api-guide.md](04-api-guide.md) · [08-testing-guide.md](08-testing-guide.md) · [AGENTS.md](../AGENTS.md)
