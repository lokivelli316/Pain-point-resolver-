# Pain point lifecycle

Every pain point moves through the same five stages. Labels show where it is.

| Stage | Label | Who moves it | Exit rule |
|---|---|---|---|
| Reported | `pain:new` | automatic | A maintainer or helper checks it is understandable |
| Confirmed | `pain:confirmed` | any maintainer | **Two** people other than the reporter say "me too" with their setup, **or** it is reproduced |
| Hunting | `pain:hunting` | anyone who starts working on it | Someone comments "I'm on it", so work isn't duplicated |
| Fix proposed | `pain:fix-proposed` | the PR author | A linked pull request contains a fix **and** a test or sample |
| Resolved | `pain:resolved` | maintainer on merge | Test passes in CI; `data/pain_points.json` updated |

Side labels:
- `pain:needs-info`: we need an error text or a setup detail. Nobody is in trouble.
- `pain:workaround`: no full fix yet, but a documented way around it exists.
- `pain:cannot-automate`: human-side pain (burnout, isolation). We still track it and share what helps.
- `help wanted`, `good first issue`: an open door for newcomers.

## Numbering

The original map covers **#1–#62**. A confirmed community pain point that isn't already on the map gets the next number (#63, #64, …) in `data/pain_points.json`, with a link to its issue. Numbers are never reused or renumbered.

## Confirming ("me too")

A useful confirmation is one comment containing:
- your platform and device (or paste `ppr doctor --json` → `fingerprint`)
- how often it hits you
- anything you tried

A bare 👍 reaction helps us sort by popularity but doesn't count toward the two confirmations.

## The no-gatekeeping rule

We never close a report because it is "a beginner problem", "user error" or "already obvious". If it caused pain, the docs, the error message or the tool can be better. The worst acceptable outcome is `pain:workaround` with a clear write-up.

## Duplicates

Link the older issue and close the newer one as a duplicate, **after** copying any new setup details across. Thank the reporter; duplicates are evidence the pain is common.

## Turning a fix into something permanent

Pick the lightest form that prevents the pain from coming back:

1. A **failure pattern** in `data/patterns.toml` (the error explains itself next time)
2. A **scan check** in `core/scan.py` (caught before it happens)
3. A **doc** in `docs/` (for things tools can't catch)
4. A **command** (for pain that needs a workflow)
