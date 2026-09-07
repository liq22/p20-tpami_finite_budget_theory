# Helper scripts

Local copies of upstream helper scripts, vendored for offline use. Both are
pure-Python, stdlib-only except for `matplotlib`/`numpy` imports at call time.

## figure_export.py
- **Purpose:** Save a matplotlib figure in multiple publication formats at
  correct DPI, with journal-aware width/size checks.
- **Inputs:** a `matplotlib.figure.Figure`, a base name, target formats
  (`pdf`, `png`, `tiff`, `eps`, `svg`), DPI, optional target journal.
- **Outputs:** image files written to the current working directory (or a path
  you pass). No other files written.
- **Network:** none. No outbound calls.
- **Writes:** only the figure files you ask it to write. Does not touch
  `paper/` unless you point its output there explicitly.

## style_presets.py
- **Purpose:** Apply pre-configured matplotlib rcParams for publication /
  journal-specific styling (Nature, Science, Cell, presentation), and switch
  colorblind-safe palettes.
- **Inputs:** a style name string (e.g. `'default'`, `'nature'`,
  `'science'`, `'cell'`) and an optional figure-width keyword.
- **Outputs:** mutates the global `matplotlib.rcParams` in the running process;
  returns nothing. No files written.
- **Network:** none. No outbound calls.
- **Writes:** nothing.

Run either file directly (`python figure_export.py`) to print a small demo.
