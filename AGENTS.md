---
titulo: Guide for AI Agents
proyecto: Atalaya (coral reef thermal-stress platform)
version: 0.1
estado: borrador
fecha: 2026-10-14
duenio: Sebastián Ibarra Herrera
depende_de: [docs/00-spec.md, docs/10-tasks.md, docs/11-memory.md]
---

# AGENTS.md

This is the first file an AI agent reads. Keep it short. Details live in `docs/`. If you use Claude Code, a `CLAUDE.md` can import this file (check the current import syntax in the documentation).

## 1. Before you start

Read in this order:

1. This file.
2. `docs/11-memory.md` (current state, decisions, blockers).
3. `docs/10-tasks.md` (find the current task and its "Done when").
4. Only the documents the task touches (`03-architecture.md`, `04-api-guide.md`, `06-code-style-guide.md`, and so on).

Then check:

- [ ] You are on the right branch and the working tree is clean (`git status`).
- [ ] You know which task you are doing and its mentor mode.
- [ ] You know which requirement the task covers.

If the task is unclear, ask before starting.

## 2. General rules

1. **Do only the task asked.** Minimum scope. No extra refactors or "while I'm here" changes.
2. **Do not invent.** If a fact is missing, say so and mark it `[TO DEFINE]`. Never guess values, endpoints or names.
3. **Ask when it is ambiguous.** A short question is cheaper than a wrong change.
4. **One change at a time.** Small, reviewable steps.
5. **Respect the mentor mode of the phase** (section 5). The goal is that the owner learns.
6. **Follow the style guide** (`docs/06-code-style-guide.md`) and the security guide (`docs/05-security-guide.md`).
7. **Tests with the change.** New behavior comes with a test; a fix comes with a regression test.
8. **Documents have owners.** Change a fact in the document that owns it, and log it in `docs/11-memory.md`.
9. **Never put real secrets** in code, docs, logs or commits.
10. **Writing style for text meant for the owner:** do not use long dashes (— or –); use commas or parentheses. No emojis unless asked.

## 3. Allowed commands

Commands below assume the Makefile from phase F0. Adjust when it exists.

**Allowed without asking**

- Read files, list folders, search the repository.
- `git status`, `git diff`, `git log`, `git branch`.
- `make lint`, `make test`, `make typecheck`, `make check`.
- Run the formatter on files you changed.
- `docker compose up` and `down` for the local core stack.
- Read-only `kubectl` commands (`get`, `describe`, `logs`) against the local cluster context only.

**Ask first**

- Installing or upgrading dependencies.
- Creating commits, branches or pull requests.
- Changing CI, the Makefile, Dockerfiles or manifests.
- Database migrations, including running them locally.
- Running a backfill or any long job.
- `kubectl apply` or `delete`, even on the local cluster.
- Any call to a paid or external API.

**Never**

- `git push --force`, rewriting shared history, or pushing directly to main.
- Reading, printing or editing `.env` files or secrets.
- `terraform apply` or `destroy`, or any cloud change, unless the owner gives that exact instruction.
- Deleting data or files outside the task's scope, or `rm -rf` outside a temporary folder.
- Disabling tests, linters or security checks to make something pass.
- Publishing anything (repository, packages, posts).

## 4. If you need help

Stop and ask when:

- The task conflicts with a document, or two documents conflict with each other.
- A requirement is missing or ambiguous.
- A change would need something from the "Ask first" or "Never" lists.
- You tried twice and the same error remains.
- You notice a security problem.

How to ask:

1. One sentence of context.
2. The options, each with a short trade-off.
3. Your recommendation and why.
4. What exactly is blocking you.

If a document is wrong or out of date, say so and propose the fix. Do not silently work around it.

## 5. Mentor mode

| Mode | What the owner does | What the AI does |
| --- | --- | --- |
| Strict | Writes the code and makes the decisions | Asks questions, gives options, explains, reviews, points out mistakes without fixing them |
| Mixed | Writes the core logic | May generate repetitive parts (configuration, boilerplate) after the owner explains the idea; reviews |
| Flexible | Reviews, decides and must be able to explain the result | May generate configuration and templates |

Phase defaults: F0 flexible, F1 strict, F2 mixed, F3 flexible, F4 mixed, F5 strict, F6 mixed, F7 mixed (agent logic strict), F8 flexible in configuration and strict in understanding cost. The task's own mode in `docs/10-tasks.md` wins.

In strict mode, do not paste a full solution unless the owner asks for it. Prefer a hint, a question or a small example that does not solve the task.

## 6. End of session

Before you finish:

1. Update the task checkboxes in `docs/10-tasks.md`.
2. Add an entry to `docs/11-memory.md` (what was done, decisions, blockers, next step).
3. Note any document you changed and why.
4. Tell the owner what is ready to review and what is left.

## Related documents

[docs/00-spec.md](docs/00-spec.md) · [docs/05-security-guide.md](docs/05-security-guide.md) · [docs/06-code-style-guide.md](docs/06-code-style-guide.md) · [docs/10-tasks.md](docs/10-tasks.md) · [docs/11-memory.md](docs/11-memory.md)
