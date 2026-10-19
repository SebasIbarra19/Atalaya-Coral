# ADR-013: NGINX Ingress and Terraform from F3; no Ansible

- Status: Decided
- Date: 2026-10-18

## Context

The local cluster in F3 needs a reverse proxy to expose the API and the dashboard. Terraform was planned only for the cloud in F8, which would mean learning it at the same moment money is at stake. Ansible was considered because it appears in job postings.

## Decision

- NGINX Ingress is the reverse proxy in the cluster (routing, TLS, request limits).
- Terraform is used from F3: it creates the local cluster (kind or k3d) and installs NGINX Ingress, ArgoCD and Sealed Secrets. In F8 the same skills are applied to AWS.
- Ansible is not used: Kubernetes manifests and Terraform are already declarative, so it would have no real job.

## Alternatives discarded

- Traefik: valid, but NGINX is more common in job postings.
- Terraform only in F8: first contact with the tool would happen in the cloud, where mistakes cost money.
- Ansible: would be added for the label only, which is hard to defend in an interview.

## Consequences

Terraform state for the local cluster lives locally and is never committed. The F3 gate includes recreating the cluster from Terraform.
