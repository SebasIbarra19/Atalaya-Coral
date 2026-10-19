# ADR-001: Local cluster first, cloud later

- Status: Decided
- Date: 2026-10-14
- Note: the cloud provider was changed from Azure to AWS on 2026-10-18, see ADR-010

## Context

The platform must run on Kubernetes, but available hours vary and cloud credits (Student Pack) are limited. Mistakes in the cloud cost money.

## Decision

Develop and practice on a local cluster (kind or k3d). Move to Azure with Terraform only in phase F8, for demos, and destroy resources when idle.

## Alternatives discarded

- Cloud from the start: spends credits early and adds billing risk while learning.

## Consequences

Manifests must work in both environments (cloud overlays added in F8). Cloud specific services are not used before F8.
