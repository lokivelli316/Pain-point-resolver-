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
