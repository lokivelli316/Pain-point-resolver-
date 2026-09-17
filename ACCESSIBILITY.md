# Accessibility Standard for `ppr`

Terminal tools rarely have an accessibility standard. This is ours. Every command must follow it, and tests enforce the parts that can be tested.

## Why

Build output is designed for throughput, not for people. Rapid scrolling, flashing progress bars, high-glare colours and dense decorative characters cause eye strain and can trigger migraines. They make screen readers recite noise, and they overload anyone who is tired. Fixing this for the most sensitive users makes the tool calmer for everyone.

## Output rules

1. **Words carry meaning.** Status is `[ok]`, `[warn]`, `[fail]`, `[info]`, `[step]`. Colour is optional decoration only.
2. **Colour off when asked.** Honour `NO_COLOR`, `TERM=dumb`, non-tty output, and `--no-color`.
3. **No motion.** No spinners, progress bars, cursor movement or line rewriting.
4. **No decorative Unicode.** No box drawing or block glyphs. Headings are `== Title ==`.
5. **Whole lines only.** Print complete lines, one at a time, flushed.
6. **Rate-limited.** Commands that stream foreign output use `core.runner`. It caps screen updates, strips colour and carriage-return overwrites, and never hides error lines.
7. **Full record on disk.** Anything not shown on screen is still in the log file.
8. **Quiet means quiet.** `-q` hides progress but never hides warnings, failures or requested results.

## Calm mode (`ppr calm`)

- Sets `NO_COLOR`, `CI`, `TERM=dumb` and tool-specific progress switches for pip, npm and cargo.
- Shows only stage lines (Compiling, Installing, Step n…), error lines, and a heartbeat every 20 s.
- Default is at most 2 screen lines per second (`interval = 0.5`), configurable in `ppr.toml`.
- For Gradle, add `--console=plain -q` yourself.

## Termux display (`ppr a11y`)

What Termux supports:

| Need | Termux setting | ppr |
|---|---|---|
| Low-glare colours | `~/.termux/colors.properties` | `ppr a11y theme --apply` (no pure black or white; contrast target adjustable, default 7:1) |
| Steady cursor | `terminal-cursor-blink-rate=0` | added if you haven't set it |
| Visible cursor | `terminal-cursor-style=block` | added if you haven't set it |
| Font | replace `~/.termux/font.ttf` | manual; see docs/ACCESSIBILITY_SETUP.md |
| Text size | pinch-zoom (persists) | manual |
| Line height / letter spacing | **not supported by Termux** | see docs/ACCESSIBILITY_SETUP.md |

Your existing theme is kept as `colors.properties.retired-<timestamp>`, never deleted.

## Reviewing a change for accessibility

- [ ] Output reads correctly with `NO_COLOR=1`
- [ ] No new glyphs outside plain ASCII and common punctuation
- [ ] Nothing redraws or animates
- [ ] Long output goes to a file, with a summary on screen
- [ ] Error lines are never suppressed
