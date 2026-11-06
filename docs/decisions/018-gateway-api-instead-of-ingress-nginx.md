# ADR-018: Gateway API instead of Ingress NGINX

- Status: Decided
- Date: 2026-11-06
- Replaces: the ingress part of ADR-013 (Terraform from F3 and no Ansible stay as decided)

## Context

ADR-013 chose NGINX Ingress as the reverse proxy of the local cluster. In November 2025 Kubernetes SIG Network announced the retirement of the community Ingress NGINX controller: best-effort maintenance until March 2026, and after that no releases, bug fixes or security patches. Installed copies keep working, but they no longer receive fixes. The Kubernetes Gateway API is the successor of the Ingress API. F3 has not started, so changing now costs only documentation.

## Decision

- Traffic into the cluster uses the Gateway API (`Gateway` and `HTTPRoute` resources) instead of `Ingress` resources.
- The responsibilities do not change: route HTTP traffic to the read API and the dashboard, terminate TLS and apply request limits.
- The implementation is chosen at the start of F3 among free, actively maintained and conformant options (for example Envoy Gateway, NGINX Gateway Fabric or Traefik). The comparison checks maintenance status, rate-limit support and memory use on the 16 GB machine, and the result is recorded in `11-memory.md`.
- If the chosen implementation cannot apply request limits through a standard resource, the limits are enforced in the API, as `04-api-guide.md` already allows.
- Terraform installs the chosen implementation in F3, as ADR-013 planned for the ingress controller.

## Alternatives discarded

- Keep Ingress NGINX: no security patches since March 2026; hard to defend in a project that cares about the supply chain.
- Another controller with `Ingress` resources (for example Traefik): valid, but the Ingress API is frozen and Gateway API is the standard that replaces it.
- Choose the implementation now: it needs a hands-on check of resources and features when F3 starts.

## Consequences

Manifests under `deploy/k8s` use `Gateway` and `HTTPRoute`. NetworkPolicies must allow the gateway's data plane to reach the API and the dashboard. The Archify diagram must be regenerated with the new component name (ADR-014).

## Sources

- Kubernetes blog, "Ingress NGINX Retirement: What You Need to Know" (2025-11-11): https://kubernetes.io/blog/2025/11/11/ingress-Nginx-retirement/
