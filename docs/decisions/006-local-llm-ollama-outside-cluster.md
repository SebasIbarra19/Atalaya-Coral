# ADR-006: Local LLM with Ollama, outside the cluster

- Status: Proposed
- Date: 2026-10-18

## Context

Branch C needs a language model for the domain agent and for HolmesGPT. The project has a zero-cost rule and no paid subscriptions. The development machine has an NVIDIA RTX 3060 Laptop GPU with 6 GB of VRAM and 16 GB of RAM, and runs Windows with Docker on WSL2. Passing the GPU into a local Kubernetes cluster (kind or k3d) on Windows is fragile.

## Decision

Serve a small open-weight model (3 to 4 billion parameters, quantized) with Ollama directly on the host machine, using the GPU. The agent inside the cluster calls it over its OpenAI-compatible HTTP API, as an external service. The exact model is chosen in F7 by running the evaluation set; models of 7 to 8 billion parameters are tried only for comparison.

## Alternatives discarded

- Paid API by default: billing risk. It may be compared later, only with a spend limit set at the provider.
- Ollama inside the cluster: needs GPU passthrough into kind or k3d on Windows.
- llama.cpp directly: more control, more manual setup; Ollama uses it underneath.
- LocalAI: valid, less known.
- vLLM: production standard but needs a larger GPU.
- LM Studio: free but not open source.

## Consequences

The model endpoint is configuration, so switching to a hosted API later changes no code. In the cloud (F8) the agent needs either a hosted model with a spend limit or a CPU-only small model; decided in F8.
