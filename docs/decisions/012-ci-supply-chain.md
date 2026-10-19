# ADR-012: CI supply chain rules

- Status: Decided
- Date: 2026-10-18

## Context

CI runs third-party GitHub Actions and scanners with access to the repository. In March 2026 `trivy-action`, `setup-trivy` and Trivy v0.69.4 were compromised and used to steal CI secrets and cloud credentials. Tags can be moved to point at malicious code; commit hashes cannot.

## Decision

- Scanners: gitleaks (secrets), CodeQL (code, from F1-T00h) and Trivy (images, from F1-T11).
- Every third-party action is pinned by full commit hash, never by tag.
- Versions are pinned and updated on purpose: Dependabot proposes, the owner reviews and approves.
- Each job gets minimal permissions; scanner jobs get only `contents: read` and no secrets.
- `pull_request_target` is not used in scanner jobs.
- Known safe versions are re-verified at the moment of use, not taken from this document.
- If a compromised version ever runs, every pipeline secret is rotated.

## Alternatives discarded

- Pinning by tag: convenient but exposed to moved or hijacked tags.
- No scanners: loses the DevSecOps part of the project.

## Consequences

Updates take a manual review. The rule applies to every new workflow, including the AWS deployment in F8 (OIDC, no long-lived keys).
