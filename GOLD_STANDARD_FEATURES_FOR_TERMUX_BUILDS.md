# GOLD STANDARD FEATURES FOR TERMUX BUILDS

Version: v0.3
Date: 2026-10-03
Status: ADDITIVE / CROSS-BUILD SUPERSET / FUTURE-BUILD CONTRACT
Authority: Operator-owned standard. Project-specific contracts still govern project-specific behavior.

## 0. PURPOSE

This document pulls the strongest proven or deliberately contracted features from the current Lokivellian Termux build family into one reusable standard. It is not a claim that every existing repository already complies. The standard is deliberately broader than any single donor build.

The rule is simple: future Termux builds should inherit the strongest applicable mechanisms already proven elsewhere instead of repeatedly rediscovering them.

Applicability labels:
- UNIVERSAL: applies to every Termux build.
- SERVICE: applies when the build starts a local server/process.
- GUI: applies when the build has a browser or graphical interface.
- API/AI: applies when the build uses external model/API providers.
- MULTI-PROCESS: applies when the build supervises multiple services/workers.
- OPTIONAL: useful when the project genuinely needs it; not a release blocker otherwise.

Implementation labels:
- IMPLEMENTED: supported by current inspected artifact/repository evidence.
- PARTIAL: some required behavior exists, but the full standard does not.
- MISSING: inspected artifact does not expose the feature.
- UNKNOWN: not safely determinable from the inspected material; live-probe rather than guess.
- N/A: feature is outside that build's purpose.

## 1. DONOR BUILD FEATURE MAP

The following current builds materially contributed to this standard.

### FORGE API + LOCAL TOOL GOLD STANDARD v0.2
Donates: GUI-first credential entry, provider/model separation, dynamic model discovery, multi-key/provider profiles, truthful fallbacks, diagnostics, import/preamble handling, persistent preferred ports, explicit collision choices, loopback/LAN/tunnel separation, tab orchestration, tab-return visual recovery, mobile accessibility, receipts, and a release gate.

### Lokivellian Termux Field Manual / Astra 1m line
Donates: one-command install, one-word launch from Termux, port ownership classification, auto-port without killing unrelated services, per-seat model dropdowns, touch-first phone pass, service discovery, local-first inventory, manifest discipline, tmux/wake-lock survival, failure atlas, backup/hash/ZIP verification, and GitHub/Termux recovery practice.

### KeyForge
Donates: authorized-root credential discovery, fingerprint deduplication, provider validation, normalized model lists, generated env profiles, project discovery, merge-not-clobber `.env` installation, timestamped rollback backups, rollback receipts, stale credential audit, aggressive secret redaction, private permissions, no telemetry, and compatibility fallback.
Known gap against this standard: no durable one-word launcher installed onto the normal Termux PATH by the inspected installer.

### Termux API Inserter v0.4.2
Donates: review-before-write, byte-preserving env edits, atomic mode-0600 writes, source-hash TOCTOU protection, single-use expiring plans, plan supersession, write locking, one-time bootstrap token exchange, HttpOnly/SameSite session cookie, URL cleanup, Host/Origin checks, path sandboxing, symlink refusal, rate limits, idle/absolute TTLs, deterministic port precedence, and explicit one-run auto-port.
Known gap against this standard: current inspected installer ends with `./start.sh`; it does not install a one-word command usable directly from `$HOME`.

### Pain Point Resolver
Donates: one-word `ppr` command, device/project fingerprinting, preflight diagnostics, failed-command diagnosis, generated INSTALL/RUNNING/TROUBLESHOOTING/AI_HANDOFF documents, low-motion output, full raw logs, append-only tamper-evident failure register, explicit accessibility doctrine, and test-proven pain-point closure.

### Three-Tool Strike
Donates: source immutability, new-output-only mutation, hashing and conflict preservation, operator conflict selection, safe ZIP/folder staging, deterministic release packages, source-coordinate provenance, explicit human promotion gate, and deliberate absence of auto-publish/deploy authority.
Known gap against this standard: it exposes several installed commands, but the inspected current package does not expose the earlier single product-level `strike` launcher.

### FRIDAY / ALYRA integrated runtime
Donates: supervisor-owned lifecycle, preflight-before-start, health-state waiting, worker separation, heartbeat/evidence collection, request/lane/boot identity receipts, owned stop order, and preserved runtime evidence.
Known gap against this standard: inspected quick start still requires a nested script path instead of a normal one-word Termux-home launcher.

### AEGIS OS
Donates: zero-runtime-dependency static fallback, preserved standalone HTML apps, no mandatory bundler/build step, direct-file fallback, snapshot import/export with secrets stripped, honest provider/CORS failures, archive byte-parity checks, secret scans, and recovery from preserved originals.
Known gap against this standard: inspected Termux start path uses `npm start` or a Python server command rather than a stable product-level one-word launcher.

### NotebookLM Hydra
Donates: serialized operator state, profile isolation, leases, durable queue, idempotency keys, rejection receipts, terminal-state immutability, deterministic dry-run, per-job artifact manifests, SHA-256 digests, and CI across tests/lint/build/smoke.
Known gap against this standard: the `hydra` command is installed inside the activated environment in the inspected workflow; a durable Termux-home PATH installation is not proven.

### Infinite Brain / Garage lineage
Donates: explicit readable/diffable/revertable persistence, changelog/schema separation, named-version intake, source-SHA receipts, verified-copy-before-purge, recoverability before deletion, and the rule that storage/promotion are separate authorities.

## 2. UNIVERSAL GOLD STANDARD

### 2.1 One-command install and visible one-word launcher - HARD REQUIREMENT
Every interactive Termux build MUST become launchable from the ordinary Termux home directory after first install.

Required behavior:
- A first-run installer MAY be `go.sh`, `install.sh`, or project-specific.
- After install, the operator MUST be able to type one stable shell token from `$HOME` without `cd` into the repo.
- The launcher MUST be on the normal Termux PATH, preferably `$PREFIX/bin/<tool>`.
- A launcher that exists only inside a repo, hidden dot-directory, private virtualenv, or shell alias does NOT satisfy this requirement.
- `.bashrc`/`.zshrc` aliases may be convenience aliases, never the only launcher.
- The installer MUST NOT silently overwrite an unrelated existing command name.
- Re-running install MUST be idempotent.
- Uninstall MUST remove only the launcher it owns.
- The launcher target and owning project/version MUST be receipt-bearing.
- `command -v <tool>` from `$HOME` MUST prove the command is discoverable.
- `<tool> --help`, `<tool> help`, or `<tool> status` MUST provide a safe non-destructive proof path.
- GUI services SHOULD open or print their local URL after successful start.

Acceptance gate:
```sh
cd "$HOME";
command -v <tool>;
<tool> --help;
```

Copy-box resilience rule: where a one-line Termux command is intended for manual copy/paste, ending the final command with `;` is acceptable. The semicolon is a harmless extra character if retained and the command remains valid if that final character is lost.

### 2.2 Installer resilience
UNIVERSAL.

The installer SHOULD:
- Detect Termux rather than assuming desktop Linux.
- Install only required packages.
- Check minimum Python/Node/runtime versions before doing expensive work.
- Prefer a private `.venv` or project-owned environment when system package policy requires it.
- Handle PEP-668-style pip restrictions honestly rather than failing mysteriously.
- Run `termux-setup-storage` only when shared storage is actually needed.
- Keep executable workspaces under `$HOME`; Android shared storage is a transfer zone, not the default npm/Python build root.
- Set executable bits explicitly after archive extraction where required.
- Never run mystery scripts solely because a filename looks plausible.

### 2.3 Stable lifecycle surface
SERVICE.

A service build SHOULD expose a stable lifecycle such as:
- `<tool>` or `<tool> start`
- `<tool> status`
- `<tool> stop`
- `<tool> doctor` or equivalent preflight/diagnostic command

Rules:
- Stop only owned processes.
- No broad `pkill`/`killall` as the normal path.
- Detect stale pidfiles.
- Flush logs/receipts before clean shutdown where practical.
- Startup success means a health probe passed, not merely that a PID was spawned.

## 3. PORT, PROCESS, AND NETWORK CONTRACT

### 3.1 Ports are preferences, not identities
SERVICE.

Required:
- Predictable project default port.
- Saved next-run preferred port when a configurable service benefits from it.
- Deterministic precedence: CLI > one-run environment/API override > saved preference > project default.
- Pre-bind collision check.
- Port ownership classification at minimum: FREE / OWNED / FOREIGN / UNKNOWN.
- OWNED means report already running rather than double-bind.
- FOREIGN/UNKNOWN must never be silently killed.
- Explicit choices: USE ONCE / SAVE NEXT-RUN / CHOOSE ANOTHER / FIND FREE PORT.
- One-run AUTO free-port mode may exist, but dependency ports may deliberately hard-fail instead of auto-bumping.
- Actual selected port must be reported and, when needed by dependents, persisted in a runtime file/registry.
- Host and port are separate authorities.

### 3.2 Exposure never widens accidentally
SERVICE.

- `127.0.0.1` is the default for local tools.
- LAN bind is explicit.
- Tunnel/internet exposure is explicit.
- Changing a port never changes bind scope.
- Chosen exposure mode and actual URL must be shown truthfully.
- A tunnel is public exposure, not "LAN with extra steps."
- Remote exposure of admin/credential/private-family surfaces requires authentication appropriate to the risk.
- Streaming transport limitations must be tested rather than assumed; fallback to polling/WebSockets when the chosen tunnel/browser path cannot sustain SSE.

## 4. API, MODEL, AND CREDENTIAL UX

### 4.1 GUI-first credential management
API/AI + GUI.

- Add / replace / delete credentials without terminal-only editing.
- Mask secrets after save; never send the full stored secret back to the browser merely to render a field.
- Provider identity, model identity, credential identity, profile identity, and seat identity remain separate.
- Multiple labeled credentials per provider.
- Custom OpenAI-compatible base URL + credential + model flow when applicable.
- OAuth-capable providers treated as first-class credential types where needed.

### 4.2 Dynamic provider/model selection
API/AI.

- Provider dropdown.
- Searchable model dropdown.
- Live model discovery/refresh where provider supports it.
- Preseed/fallback catalog may exist, but stale catalog state must be labeled.
- Favorites/pinned/recent models are desirable.
- Hide or clearly disable unavailable provider/model combinations.
- Show capability metadata when available: context window, tools, vision, reasoning, streaming, pricing, availability.
- Per-seat/per-tab model selection when roles differ.
- Temporary one-run model override without mutating defaults.
- No silent provider/model/credential substitution.
- Fallbacks are visible and receipt-bearing.

### 4.3 Provider health and key pools
API/AI.

Health states SHOULD distinguish HEALTHY, THROTTLED, QUOTA_EXHAUSTED, AUTH_FAILED, DEGRADED, OFFLINE, UNKNOWN.

Key-pool policies may include PRIMARY_ONLY, FALLBACK, ROUND_ROBIN, and later LEAST_USED/LATENCY_WEIGHTED. Never hammer a credential already known to be exhausted before its cooldown/reset.

## 5. SECRET AND ENVIRONMENT SAFETY

### 5.1 Default-deny secret handling
UNIVERSAL when secrets exist.

- Treat unknown environment values as sensitive unless positively classified otherwise.
- Never log raw API keys, Authorization headers, session cookies, OAuth tokens, or secret query parameters.
- Global redaction should scrub both registered secrets and recognizable key patterns from logs/errors/responses.
- Credential files/profiles should be mode 0600; containing directories mode 0700.
- No telemetry or cloud sync by default for local credential tools.

### 5.2 Authorized discovery only
API/AI.

- Scan only operator-authorized roots.
- Do not cross symlinks out of authorized roots.
- Skip binary/oversize files according to declared limits.
- Parse `.env`/config as data; never execute candidate files to inspect them.
- Deduplicate secrets by fingerprint, not by exposing the secret.
- Preserve source locations so the operator can see where stale credentials live.

### 5.3 Merge, backup, review, atomic write
UNIVERSAL when editing operator files.

Before modifying an existing config/env file:
- Present a review/plan or equivalent explicit change set.
- Back up the original under a namespaced timestamped filename.
- Merge only owned keys; preserve unrelated lines/comments byte-for-byte where practical.
- Detect source change between review and write using a hash or equivalent TOCTOU guard.
- Use single-use/expiring write plans for high-value local GUI mutation surfaces.
- Serialize concurrent writes with a lock.
- Write through a private temp file and atomic replace.
- Reject managed-file symlinks when they could escape the sandbox.
- Emit rollback instructions/receipt.

## 6. LOCAL WEB AUTH AND BROWSER HARDENING

GUI + SERVICE.

Where a local browser UI can mutate files/secrets:
- Use a fresh session/bootstrap secret per run.
- Do not leave reusable secrets in the URL.
- Prefer one-time bootstrap exchange into an HttpOnly, SameSite session cookie or equivalent local session mechanism.
- Clean bootstrap parameters from browser history immediately.
- Validate Host and Origin/Referer as appropriate to block cross-site local attacks.
- Bound idle and absolute session lifetime.
- Rate-limit sensitive auth/mutation endpoints.
- Keep path writes sandboxed by default.
- Non-loopback serving must be an explicit mode with a different threat model.

## 7. PREFLIGHT, DIAGNOSTICS, AND FAILURE TRUTH

UNIVERSAL.

Every serious build SHOULD provide a `doctor`, `preflight`, `verify`, or equivalent path that can separately prove:
- runtime/toolchain versions;
- storage/workspace suitability;
- dependency presence;
- port state;
- credential authentication;
- model discovery;
- selected-model access;
- bounded real inference where applicable;
- writable state/log/backup locations;
- package manifest integrity;
- service health.

Rules:
- Unknown stays UNKNOWN. Never convert a failed probe into PASS.
- Preserve provider/HTTP error class while redacting secrets.
- Tell the operator the smallest useful next action.
- Keep a human-readable raw log on disk.
- When a failure pattern is known, map symptom -> likely cause -> first action.
- Failure history SHOULD be append-only or tamper-evident when it is used as evidence.

## 8. PROCESS OWNERSHIP AND ORCHESTRATION

MULTI-PROCESS / SERVICE.

- Orchestrators wrap independent tools; they do not absorb or overwrite them.
- Child apps keep authoritative HTML/CSS/JS and remain directly runnable.
- Registry fields should include module ID, display label, URL, cwd, startup command, host, port, health path, version/hash, enabled state.
- Discovery may search for candidate start files, but discovery is not authority to execute or register.
- Start/stop/restart only owned processes/process groups.
- Health states are truthful: ONLINE / OFFLINE / STARTING / DEGRADED / UNKNOWN as appropriate.
- Duplicate ports and stale PIDs are reported, not silently rewritten.
- Local installed copy outranks a repo mirror unless the operator explicitly selects another source.

## 9. PERSISTENCE, QUEUES, IDEMPOTENCY, AND STATE

UNIVERSAL when durable state exists.

- State must be readable and exportable in an operator-owned format.
- Separate current state from changelog/audit history where practical.
- Export/import must strip secrets by default.
- Durable queues must survive process restart without conversational memory.
- Idempotency keys should return the existing job instead of duplicating it.
- Terminal job states do not transition again without an explicit new operation.
- Leases/locks must prevent two workers from claiming one exclusive resource.
- Crash/restart semantics must be defined for operations that can write, upload, publish, or delete.
- A successful write must not be reported before its durable receipt/state update is committed.

## 10. RECEIPTS, MANIFESTS, AND PROVENANCE

UNIVERSAL.

Record enough to reconstruct what actually happened without storing secrets:
- exact build/version/hash;
- source/donor identifiers and order;
- actual provider/model/seat/credential alias when applicable;
- fallback event;
- host/port/exposure mode;
- command/action performed;
- output/artifact path;
- cancellation/failure classification;
- test results;
- rollback/promotion state.

Package manifests:
- SHA-256 ledger of package files.
- Regenerate before release packaging after any approved change.
- Operator-entry files and launchers MUST be included.
- A receipt claiming a fix belongs in the same artifact/commit as the fix it certifies.
- "Manifest green" means the project verifier actually reported zero failures; a filename comparison is not enough.

## 11. BACKUP, ROLLBACK, AND RELEASE DISCIPLINE

UNIVERSAL.

- Never overwrite a known-good artifact merely to make naming prettier.
- Hash archives and verify them before deleting/moving the source.
- Test ZIP/TAR integrity before calling a package a backup.
- Preserve a top-level package directory so extraction cannot spill loose files into a workspace.
- Preserve execute bits or repair them explicitly and receipt the repair.
- Clean-extract the final package and rerun its own verifier/tests.
- Named releases require source SHA/hash plus verification receipt.
- No source purge until the recovery copy is verified.
- Publication/deployment/promotion is a separate human authority unless the project explicitly delegates it.

## 12. SOURCE IMMUTABILITY AND SAFE OUTPUTS

UNIVERSAL for transform/reconciliation tools.

- Inputs are read-only unless mutation is explicitly part of the tool contract.
- Prefer new output directories/artifacts over in-place destructive edits.
- Preserve original bytes separately from overlays, preambles, transformations, and generated results.
- Conflicting generations remain visible until the operator selects a winner.
- Exact duplicates may be deduplicated by hash, but lineage/provenance remains recorded.

## 13. MOBILE AND ACCESSIBILITY

GUI / TUI.

Minimum phone-first rules:
- Primary touch targets approximately 44x44 CSS px or larger.
- Phone body text large enough to read without precision zooming; ~18px is a good default target for narrow browser layouts.
- Long paths, URLs, model IDs, hashes, and keys wrap visually without corrupting copied values.
- No tiny-text modal/inspector islands.
- Hover interactions have keyboard/focus equivalents.
- Visible focus outline.
- Tables become horizontally safe or card-like on narrow viewports.
- Sticky bottom/thumb anchor for critical mobile navigation where useful.
- Sliders display numeric values and ideally have numeric entry alternatives.
- Drag-only workflows need non-drag alternatives where practical.
- Status must not depend on color alone.
- Honor `NO_COLOR` for terminal tools.
- Honor `prefers-reduced-motion` for web tools.
- Screen updates should be rate-limited for low-flicker terminal modes.
- Effects degrade before function degrades.
- Provide no-WebGL/compatibility fallback when the visual layer is optional.

## 14. TAB RETURN AND VISUAL STATE RECOVERY

GUI.

Browser throttling/backgrounding is a normal phone condition, not an edge case.

Required for animated/environmental surfaces:
- On visibility/tab return, re-synchronize the active semantic state.
- Verify hero/video/animation layers are actually running.
- Restart only the stale media/animation layer, not the whole application.
- Preserve form inputs, selected project/theory, imports, receipts, scroll/work state.
- Do not blindly reload the full page on every tab switch.
- Deterministic frame-zero/export surfaces get their own synchronization rule rather than random restart.
- Regression-test day/night, repeated tab changes, background pause/resume, ended/paused media, and phone memory-pressure return where practical.

## 15. LOCAL-FIRST AND GRACEFUL DEGRADATION

UNIVERSAL.

- Prefer local ownership of state, configuration, logs, artifacts, and recovery data.
- Use stdlib/zero-dependency paths where they materially reduce breakage; dependencies are allowed when they earn their weight.
- A static/direct-file fallback is desirable for browser tools where practical.
- Cloud/API features fail honestly and locally useful features keep working when possible.
- No fake sync, fake model call, fake health, fake audit participation, or fake PASS.
- Optional visual effects may fail without taking the control surface down.
- Apps remain independently runnable even when registered with a larger orchestrator.

## 16. DOCUMENTATION AND AI HANDOFF

UNIVERSAL.

Every shippable build SHOULD be able to tell the next human or model:
- what this build is;
- exact version/hash;
- how to install;
- the one-word launcher;
- how to stop/status/doctor;
- default host/port and exposure rule;
- where state/logs/backups/receipts live;
- what is implemented / partial / missing / unknown;
- known failure signatures and first actions;
- how to rollback;
- what files/areas must not be flattened or overwritten.

For complex builds, generate or ship an `AI_HANDOFF.md` containing the environment fingerprint, project layout, active rules, open findings, recent failures, and exact next actions.

## 17. TERMUX FILESYSTEM AND COPY-BOX DISCIPLINE

UNIVERSAL.

Recommended working lanes:
- `$HOME/forge-src` - executable source trees.
- `$HOME/forge-builds` - staging/build output.
- `$HOME/forge-logs` - runtime logs.
- `$HOME/forge-backups` - verified backups and donor hash ledgers.
- Android shared storage - transfer/export surface, not the default live build workspace.

Command-writing rules:
- Prefer `$HOME` over fragile escaped `~` paths.
- Quote paths.
- Show the exact cwd before destructive or packaging commands.
- Never use `rm -rf ~` or similarly ambiguous destructive shorthand.
- Use targeted shutdown and targeted cleanup.
- For copy/paste-sensitive one-line Termux commands, a trailing `;` is permitted as a harmless sacrificial final character.

## 18. TEST AND RELEASE GATE

A build may call itself GOLD STANDARD only for the applicable capability classes that pass their gates.

Universal gates:
- Fresh install from a clean checkout/archive passes.
- One-word launcher works from `$HOME` on a normal Termux PATH.
- `command -v <tool>` resolves to the owned launcher.
- Non-destructive help/status proof works.
- Secrets are absent from repository, logs, receipts, exports, and test fixtures.
- Manifest/hash verification passes.
- Backup/rollback path is proven before destructive mutation is allowed.
- Existing functional behavior passes regression.
- Exact version/hash and test results are recorded.

Service gates:
- Health endpoint/probe passes.
- Port collision with OWNED and FOREIGN occupants is tested.
- No unknown process is killed.
- Loopback default is proven.
- LAN/tunnel exposure requires explicit selection.
- Stop targets only owned processes.

API/AI gates:
- Credential auth, model discovery, selected-model access, and bounded inference are distinguishable tests.
- Provider/model/fallback identity is truthful.
- Dynamic model choice works when provider supports it.
- Stale/exhausted credentials do not get hammered indefinitely.

GUI gates:
- Phone touch pass.
- Keyboard/focus path.
- reduced-motion path.
- Long values wrap safely.
- Tab-return state recovery where applicable.
- Browser fallback does not erase operator state.

Mutation gates:
- Review/plan before write.
- Backup before write.
- Source-change/TOCTOU guard.
- Atomic write.
- Concurrent save serialization.
- Rollback receipt.

Release gates:
- Deterministic package/archive.
- Top-level folder present.
- Clean extraction test.
- In-tree test suite passes after extraction.
- Artifact hash sidecar/manifest generated.
- Promotion/publication remains human-gated unless separately authorized.

## 19. CURRENT CROSS-BUILD GAP PRIORITIES

These are not accusations; they are the highest-value standardization gaps exposed by the current inspected builds.

1. ONE-WORD LAUNCHER GAP - KeyForge, API Inserter, FRIDAY, AEGIS, and the current Hydra install path do not all prove a stable command available from ordinary Termux `$HOME`. Fix this first across future builds and as existing repos are touched.
2. PRODUCT-LEVEL LAUNCHER GAP - Three-Tool Strike has installed utility commands, but the current inspected package does not expose the simpler product-level `strike` word documented in older field-manual lineage.
3. PORT CONTRACT CONSISTENCY - some builds have excellent safe auto-port logic while others still rely on fixed ports/manual recovery. Adopt the same ownership-aware collision contract everywhere a local server exists.
4. DOCTOR/PREFLIGHT CONSISTENCY - PPR is strongest here. Every substantial build should inherit a bounded non-destructive self-diagnosis path.
5. MUTATION SAFETY CONSISTENCY - API Inserter is strongest on review/TOCTOU/locking/atomic writes. Any tool that edits operator files should inherit those mechanisms.
6. CREDENTIAL HEALTH CONSISTENCY - KeyForge is strongest on discovery/validation/stale-env replacement. API-using builds should consume the same concepts rather than inventing one-off key handling.
7. RECEIPT/MANIFEST CONSISTENCY - Astra/Strike/Hydra/FRIDAY prove different pieces. Every build should emit compatible evidence about what version ran, what changed, what tests passed, and where rollback lives.
8. MOBILE/ACCESSIBILITY CONSISTENCY - the Workshop touch pass and PPR low-motion rules should be treated as default UI engineering, not optional cleanup.
9. CRASH/RESTART SEMANTICS - durable queues, uploads, mutation, and deletion paths must record transaction state so a restart cannot duplicate work or lie about completion.
10. NO-FAKE-PASS CONSISTENCY - any UNKNOWN, unavailable dependency, empty participant set, failed model route, or unrun browser test remains explicitly UNKNOWN/PARTIAL/NOT RUN.

## 20. ADOPTION RULE

This standard is additive. It does not authorize flattening a project's UI, replacing its visual concept, deleting donor lineage, or forcing irrelevant features into a tool.

When adopting it into an existing repo:
1. Audit the repo against this document.
2. Mark each applicable item IMPLEMENTED / PARTIAL / MISSING / UNKNOWN.
3. Preserve working behavior.
4. Add missing mechanisms in bounded change sets.
5. Test the exact changed surface.
6. Regenerate manifests/receipts.
7. Do not call the build Gold Standard until the applicable release gates actually pass.

Underpromise. Overbuild. Fix forever. No silent substitutions. No fake green lights. One word from Termux home should be enough to find the damn tool.