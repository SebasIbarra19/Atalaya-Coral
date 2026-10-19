# ADR-011: Sealed Secrets for cluster secrets

- Status: Decided
- Date: 2026-10-18

## Context

The cluster is deployed from Git with ArgoCD, so every manifest lives in a public repository. Workloads still need secrets (database passwords, the admin API key). Plain Kubernetes Secrets are only base64, not encrypted. The project has a zero-cost rule.

## Decision

Use Sealed Secrets. Secrets are encrypted with the controller's public key and committed to Git; only the controller in the cluster can decrypt them. The controller's private key is backed up outside the repository. When F3 starts, check that the project is still actively maintained.

## Alternatives discarded

- Plain Secrets in Git: readable by anyone with access to the repository.
- External Secrets Operator: a good next step, but it needs an external store (AWS Secrets Manager, Vault) that costs money or adds another service. It can be adopted in F8 if useful.

## Consequences

Creating a secret needs the `kubeseal` CLI. If the cluster is rebuilt, the backed-up private key must be restored or every secret resealed.
