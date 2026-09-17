# Working with AI collaborators

Humans and AI systems both contribute here. These rules keep that collaboration trustworthy.

## For people using an AI assistant

1. **Disclose it.** Tick the box in the pull request template and say roughly what the AI did.
2. **You own the change.** Read it, run the tests, and be ready to explain it.
3. **Give the AI the context.** Paste `.ppr/RULES.md` and the output of `ppr docs .` (the `AI_HANDOFF.md` file) at the start of the session.
4. **Check the facts.** AI tools can invent flags, settings and package names. Confirm them against real output before committing, and set pattern `confidence` honestly.
5. **No secrets in prompts.** Strip tokens and personal paths from logs before sharing them with any tool.

## For AI agents acting on this repository

- Follow `.ppr/RULES.md` exactly: stdlib only, upgrade-only outputs, append-only registers, nothing self-certifies, accessible output, samples for every pattern, honest confidence.
- Open pull requests, never push to `main`.
- Keep each pull request to one change, and include the test output.
- Do not mark any pain point `resolved`; only a maintainer does that, after CI passes.
- Do not open issues or comments in bulk. One well-evidenced report beats ten guesses.
- When unsure, ask in the issue rather than guessing.

## Why this matters

AI can read a thousand error logs without getting tired. People know which of those errors actually ruined their afternoon. Put together, that is how a shared list of pain points gets squashed for good.

## Floor access (appended 2026-09-17)

The floor is the branch. `main` stays the call.

Agents may push feature branches and open pull requests. They may not push `main`, force-push `main`, or mark a pain point resolved. CI is the first reviewer. Protected paths (`.ppr/RULES.md`, `ACCESSIBILITY.md`, `core/`) still need a human look.
