# ADR-015: No AI attribution in the repository

- Status: Decided
- Date: 2026-10-18

## Context

AI coding tools used in this project add attribution lines by default, such as a co-author trailer in commit messages or a "generated with" line in pull request descriptions. The project already decided that AI works as mentor and copilot, not author (`11-memory.md`, 2026-10-10). Commit messages in this repository are a single line.

## Decision

- Commit messages, pull request descriptions and repository files carry no AI attribution: no co-author trailers and no "generated with" lines.
- Commit messages keep the single-line format `type: summary (references)`, for example `docs: close phase F0`.
- The owner is the only author of record.

## Alternatives discarded

- A co-author trailer on AI-assisted commits: it breaks the single-line format and lists a tool as an author, against the 2026-10-10 decision.

## Consequences

The rule is also in `AGENTS.md`, so every agent reads it before committing. Messages are checked with `git log` before pushing, and a message with attribution is corrected before it leaves the machine.
