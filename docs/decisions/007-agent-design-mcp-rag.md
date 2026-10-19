# ADR-007: Agent design: MCP tools, RAG with pgvector, structured outputs, no fine-tuning

- Status: Proposed
- Date: 2026-10-18

## Context

The domain agent must answer only from real data, cite its sources and pass an evaluation set (RF-12). It also needs to explain what NOAA terms mean (DHW, HotSpot, alert levels), which is not in the numeric data.

## Decision

- Tools: an MCP server exposes a fixed allowlist of read-only tools (`get_site_status`, `get_forecast`, `search_docs`). The agent gets data only through them.
- Retrieval (RAG): public reference documents are split into chunks, embedded with a local embedding model and stored in PostgreSQL with pgvector (`doc_chunks`). `search_docs` queries them with a read-only role.
- Structured outputs: every answer is JSON with text, sources and data used, validated against a schema before it reaches the dashboard.
- No fine-tuning: behavior is shaped with the system prompt, tools and retrieval.

## Alternatives discarded

- Pasting the data into the prompt: harder to control, evaluate and limit.
- A separate vector database (Pinecone, Chroma): one more service for very little data.
- Fine-tuning: there is no training set of questions and answers, and the data changes daily, so a fine-tuned model would be out of date. RAG keeps answers tied to current data.

## Consequences

The evaluation set covers grounding, refusal, schema validity and prompt injection (TC-15, TC-16, TC-22 to TC-24). Retrieved text is treated as untrusted input.
