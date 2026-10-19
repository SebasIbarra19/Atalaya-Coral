# ADR-010: AWS as the cloud provider, free plan only

- Status: Decided
- Date: 2026-10-18
- Supersedes: the Azure choice in ADR-001

## Context

Phase F8 deploys the platform to a public cloud with Terraform as a final demonstration. The first plan used Azure through the GitHub Student Pack. The project is a portfolio piece, and AWS appears more often in the job postings reviewed. The project has a zero-cost rule, and an unexpected bill is the main risk.

## Decision

- Use AWS in F8, created and destroyed with Terraform.
- Create the AWS account only when F8 starts, on the free plan, never on a paid plan, and without AWS Organizations.
- Before creating any resource: MFA on the root account and no root access keys, an AWS Budgets alert, a separate IAM identity for Terraform, and GitHub Actions authenticating through OIDC (no long-lived keys).
- `make cloud-down` runs `terraform destroy`; the console is reviewed after every session.
- EKS or k3s on EC2 is decided in F8 after checking what the free plan covers at that moment.

## Alternatives discarded

- Azure through the Student Pack: valid and with credits, but less demanded in the job postings reviewed.
- Google Cloud: not evaluated in depth; same reasoning as Azure.

## Consequences

The free plan rules are verified when F8 starts, not now, because they change. Services that bill silently (NAT Gateway, idle load balancers, forgotten instances or volumes) are avoided or destroyed at the end of each session.
