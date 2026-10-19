# ADR-014: Architecture diagrams as HTML with Archify

- Status: Decided
- Date: 2026-10-18

## Context

The README and `03-architecture.md` show the architecture as a Mermaid overview. The portfolio needs a richer diagram that a reviewer can explore and trust. The architecture is still planned: nothing runs yet. A diagram drawn by hand or by an AI tool can drift from the documents.

## Decision

- Architecture diagrams are standalone HTML files generated with Archify. The JSON source and the HTML live together in `docs/diagrams/` (for example `architecture.json` and `architecture.html`).
- A diagram is built only from `03-architecture.md` and the ADRs. Components come from section 3, arrows and protocols from section 4, drawn from caller to callee. A relationship stated elsewhere in the documents (sections 3 and 5, or an ADR) may be drawn; nothing else is added.
- Every node cites the document lines it comes from, pinned to a commit, so each claim can be checked on GitHub.
- While nothing runs, the diagram is marked as planned in its title.
- Archify delivery receipts (`*.delivery.json`) are not committed, because they hold local absolute paths.

## Alternatives discarded

- Mermaid only: renders on GitHub, but it is less rich, not interactive and has no source links. It stays as the quick text overview.
- Archify output in `.archify/`: hidden, timestamped folders that are hard to find and review.
- Arrows in the direction of the data, as in the section 1 overview: it would mix conventions with the section 4 table, which is the connection reference.

## Consequences

When a document changes a component or a connection, the JSON is updated, the HTML is regenerated and the pinned commit of the sources moves to the commit that holds the change. GitHub shows HTML files as source code, so the diagram is opened locally or published separately (how is `[TO DEFINE]`). Each diagram adds close to 1 MB of HTML to the repository.
