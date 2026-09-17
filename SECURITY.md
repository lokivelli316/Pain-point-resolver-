# Security Policy

## Reporting

Please report vulnerabilities privately through GitHub's **Report a vulnerability** button (Security tab → Advisories), not in a public issue. Expect an acknowledgement within 7 days.

## Scope notes

- `ppr hunt` and `ppr calm` run the command you give them, with your permissions. They do not add privileges.
- Reports and registers can contain command lines, paths and output. **Check them for tokens and personal paths before sharing** a report or an `AI_HANDOFF.md`.
- `ppr` makes no network requests.
- The register hash chain detects accidental or casual edits. It is not a signature; anyone who can write the file can rebuild the chain.

## Supported versions

Only the latest release receives fixes during the 0.x series.
