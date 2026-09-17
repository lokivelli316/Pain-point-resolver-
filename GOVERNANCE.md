# Governance

## Roles

- **Maintainer / project lead:** Robert M. Earlywine-Lucas (GitHub: `@lokivelli316`). Final say on scope, releases and the rules in `.ppr/RULES.md`.
- **Module owners:** anyone who builds a command can be listed as its owner in `.github/CODEOWNERS` and reviews changes to it.
- **Contributors:** everyone else. All are welcome.

## How decisions are made

1. Small changes: a pull request with one approving review from the maintainer or the module owner.
2. Design changes (new command, new contract, config format, anything affecting output rules): open an issue with the `proposal` label, then record the outcome as an ADR in `docs/adr/`.
3. ADRs are append-only. A reversed decision gets a new ADR that supersedes the old one.

## Becoming a module owner

Build or substantially maintain a command, then ask. Owners are added to CODEOWNERS.

## Releases

Semantic versioning. The maintainer tags releases; every release has a CHANGELOG entry.

## Scope

This repository is public. It contains the generic tool only. Private configurations, personal profiles and any unrelated work stay out of it.

## Open shop (appended 2026-09-17)

Claude's roles and decision rules above stay in force. This section opens the floor so the founder is not the only person who can move a building block.

- The shop is open to everybody.
- `main` is the call: report → confirm → hunt → fix with a test → resolved.
- Branches are open. Anyone may push a branch or open a fork and a pull request: amateur, professional, or AI collaborator.
- No direct push to `main`. No force-push to `main`. CI must pass.
- An amateur and a professional can share the same plague. A proven fix removes it for both.
- CODEOWNERS covers only protected paths (rules, accessibility, core). Patterns, samples, docs, and device reports do not wait on a catch-all owner.
- Write access means: branch + pull request. It does not mean skip the call.
- No coder or developer gets left behind.
