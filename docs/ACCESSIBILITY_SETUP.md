# Setting up a comfortable Termux

## 1. Calm colours and cursor
```bash
ppr a11y theme               # preview
ppr a11y theme --apply       # install (your old theme is kept)
ppr a11y theme --contrast 5.5 --apply   # softer text if 7:1 feels harsh
```

## 2. Calm builds
```bash
ppr calm -- npm install
ppr calm --print-env >> ~/.bashrc     # make most tools calmer everywhere
```

## 3. Text size
Pinch to zoom in Termux; it remembers the size.

## 4. Font
Termux uses `~/.termux/font.ttf`. Copy any monospace TTF there and run `termux-reload-settings`. Fonts designed for legibility, with clearly different similar-looking characters and generous spacing, help with astigmatism. Try a few; comfort is personal.

## 5. Line height and letter spacing
**Termux itself cannot change these.** The only route is a desktop terminal inside Termux:X11 that supports cell-size adjustment (for example kitty's `modify_font cell_height` / `cell_width`, or Alacritty's `font.offset`). Confidence that these run on a given phone is **low to medium**: both need GPU acceleration that not every device's X11 setup provides. Contributions documenting working device + terminal combinations are very welcome.

## 6. Android side
- Dark theme and "Extra dim" (Android 12+) reduce overall glare.
- Keep Termux out of battery optimisation so long builds aren't killed.
