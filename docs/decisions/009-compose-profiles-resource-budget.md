# ADR-009: Compose profiles and a local resource budget

- Status: Proposed
- Date: 2026-10-18

## Context

Development machine: Intel i7-11800H (8 cores), 16 GB RAM, RTX 3060 Laptop GPU with 6 GB of VRAM, Windows with Docker on WSL2. The full stack (cluster, database, observability, MLflow, Phoenix, Ollama) plus the editor and browser does not fit comfortably in 16 GB. RAM is the real limit, not the GPU or the CPU.

## Decision

- Docker Compose uses profiles (`core`, `ml`, `agent`, `obs`); `make up` starts only `core`.
- In the cluster, only the components of the current phase run; the rest are scaled to zero.
- WSL2 memory is capped with `.wslconfig` (value set in F3 after a first measurement).

## Alternatives discarded

- Running everything at once: slow or crashing machine.
- Buying hardware or renting machines: outside the zero-cost rule and not needed.

## Consequences

Each profile and phase documents which services it needs. The README explains how to start each profile.
