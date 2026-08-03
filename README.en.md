. **Reorder** with ↑↓ — legend and draw order change, **the colour stays with the series** |# VTC Visualizer

**English** | [한국어](README.md)

A general-purpose visualizer that turns CSV/JSON data into paper-style interactive charts, right in your browser.
Build fully customizable benchmark comparisons — performance vs. token budget, performance vs. speed, and so on.
All data is processed entirely in your browser and never sent anywhere.

> 📊 **Which chart, when, and how to make it land?** — see the **[Visualization Guide (GUIDE.en.md)](GUIDE.en.md)** for chart-choice criteria and per-scenario recipes.

## Preview

Every setting re-renders the chart live — hop between scatter, line and bar, and drop a trendline on top:

![Live editing: scatter → trendline → bar chart](assets/readme/hero-v2.gif)

| Bar charts (mean · sort · horizontal · error bars) | Highlight by dimming (focus + context) | Small multiples (facet) |
|:---:|:---:|:---:|
| ![bar charts](assets/readme/bars-v2.gif) | ![dim filter](assets/readme/dim-filter-v2.gif) | ![facet](assets/readme/facet-v2.gif) |

## Quick start

Any of these three:

1. **Double-click** — open `index.html` in a browser and drag & drop your files (needs internet: the chart library loads from a CDN)
2. **Fully offline** — double-click `index-offline.html` (no internet needed; copy this single file anywhere)
3. **Folder autoload** — run the server pointing at a data folder:

   ```bash
   python visualizer.py .                 # first time? try the bundled example.csv
   python visualizer.py results/          # autoloads *.csv, *.json from results/
   python visualizer.py                   # start empty
   python visualizer.py results/ --port 8765
   python visualizer.py results/ --host 0.0.0.0   # reach it from another machine (exposes the folder)
   ```

   Tick `Watch folder` on the page and changes to those files load by themselves.

   Subfolders are included too (they show up as relative paths like `sub/run1.csv`).
   Hidden folders (`.git`, `.venv`, …) and symlinks pointing outside the folder are skipped, and the list stops at 500 files.

The UI is bilingual — use the **KO/EN toggle** in the top-right corner (your choice is remembered).

Try dragging in the bundled `example.csv` first — 24 rows sweeping 4 methods × token budgets (500–16k, no duplicates),
with common-sense trends baked in: accuracy rises with a saturating curve while latency and cost grow with tokens
(e.g. X=tokens, Y=accuracy, group=method gives clean curves with no filters).

## Adding data

- **Drag & drop** CSV/JSON files (multiple at once)
- **Open files… / Open folder…** buttons
- **Paste data…** button → paste CSV/JSON text
- When launched via `visualizer.py`, files in the given folder load automatically

Files keep merging as you add them. Re-adding the same filename replaces it.

## Data format (input contract)

- **CSV**: first line is the header, then one row = one measurement point. (TSV also works)
- **JSON**: an array of objects `[{"method": "ours", "tokens": 4000, "score": 0.744}, …]`
- **No required columns.** Numeric columns automatically become axis candidates; string columns become group (color) / filter candidates.
- Column names are free-form, and files may have different columns (merged as a union; missing cells show as `–`).
- With two or more files loaded, the source filename appears as a `_source` column usable for grouping/filtering (hidden with a single file).

Recommended shape (long-form / tidy — one measurement per row):

```csv
method,tokens,latency_s,score,dataset
baseline,1000,1.2,0.612,MMLU
baseline,4000,3.8,0.681,MMLU
ours,1000,1.4,0.641,MMLU
ours,4000,4.1,0.744,MMLU
```

## Features

| Feature | How |
|---|---|
| Add/duplicate/delete charts | `＋ Add chart` at the top, `Duplicate`/`Delete` on each card (**undo** from the toast) — multiple charts per page |
| **Reorder & collapse cards** | `↑`/`↓` in the card header reorder, `▾` folds the plot. Zoom and settings-panel state survive adding charts or switching language |
| **Chart types** | scatter · line · scatter+line · bar · **heatmap** (2D grid by color) · **dumbbell** (paired per category) · **histogram** · **box plot** (distributions) · **violin** (the shape, not just the quartiles) · **ECDF** (what fraction sits at or below a value) · **broken axis** (fold away the gap when values split into two far-apart groups — axis values stay real) |
| **Chart palette** | Top-bar picker: Default · Carbon · Okabe-Ito · Ink — all validated colorblind-safe, with separate light/dark steps |
| **Second Y axis** | Settings → Data → Second Y axis: two metrics on different scales in one chart (right axis, dotted line, × markers) |
| **Option search** | Type an option name in the search box above the settings panel to filter it down |
| **Automatic analysis** | `Analyze` in the top bar → a column profile (kind, missing, quantiles) plus findings ordered **data problems → interpretation cautions → findings**. Each tier carries a one-line note on **how to verify it**, and `＋ Chart` (or `Go to chart` when one already matches) opens the supporting chart. Findings also print their chart recipe (type · X · Y · group) so they are easy to line up against a chart. Duplicate columns, Simpson's paradox and crossovers are filtered out, and instead of p-values you get raw differences with direction consistency |
| **Chart controls** | drag = zoom to area · wheel = zoom · double-click = reset view · pan via the crosshair in the mode bar · `Reset view` button. Zoom survives style changes |
| Axes & scales | Settings → Axes: labels, linear/log toggle, min/max range (**either side alone is fine**), grid |
| Series styling | Settings → Style: per-series color, **editable legend name**, marker symbol/size, **line style (solid/dash/dot) and width**, **display mode (points / line / points + line)**, font |
| **Chart size & layout** | Settings → Style → Chart size: height slider + **full/half width** (half places two charts side by side). A top-bar **width toggle** (normal/wide/full) sets the whole page width The **settings panel width** (narrow/default/wide/widest) is picked above the panel and applies to every chart. The panel height follows the window, and `One at a time` keeps a single group open (the series list starts folded) |
| Legend position | Settings → Style → Legend: right · top · **inside corner (top-left/top-right/bottom-left/bottom-right)** · hidden |
| Copy filters | Settings → Filters → `Copy these filters to…` — apply the same conditions to one or all charts |
| Filters | Settings → Filters: pick a column → categorical columns get **value checkboxes (multi-select** — e.g. check just baseline & ensemble), numeric columns get comparisons (>, ≥, …) **or the "Select" operator for multi-select values**. Each filter runs in **Exclude** (drop non-matching rows) or **Dim** (fade non-matching rows into the background = rule-based highlight) mode |
| **Language (KO/EN)** | Toggle button in the top-right corner (persisted) |
| **Dark mode** | 🌙/☀️ button (top-right) toggles light↔dark. Follows the OS setting first, then remembers your choice; charts adapt to the theme |
| **Baselines** | **Click** a point → "Add baseline" → thin dashed h/v lines. **Multiple baselines**, each switchable between **crosshair / horizontal only / vertical only** (e.g. a horizontal 0-line for delta metrics), quadrant shading in crosshair mode, removable from the settings panel, and it is **anchored to that point (row)** so it follows the new value when data is refreshed (baselines typed in as values stay pinned to the value). If the anchor point disappears it is not drawn in the wrong place — a ⚠ appears and you can `Re-anchor` it |
| **Mark best** | Settings → Point labels → Mark best: labels the highest or lowest Y automatically (one overall, or one per series). It is **re-picked from the current data on every draw**, so it moves when the data changes — unlike a hand-placed text marker |
| **Text markers** | **Click** a point → "Add text marker" → an arrowed callout. Drag to move, click to edit/delete. Each marker is **anchored to that point (row)**, so it follows the new value when the data is refreshed. `＋ Text marker` under Settings → Point labels builds one **by picking a row** instead (no mouse needed) |
| **Pinned notes** | Settings → Point labels → `＋ Pinned note`: a note tied to no data point, parked in a corner of the chart (`n=24 · measured 2026-07`). It stays put when the data or axes change, and can be dragged anywhere |
| **Lost-anchor warning** | If the anchor row disappears (filter, exclusion, deletion) or the axis column changes, the marker is **hidden rather than drawn in the wrong place**, and you're told. The settings list keeps it with a ⚠ and a reason, plus `Re-anchor` to attach it to another point |
| **Exclude a point** | **Click** a point → "Exclude this point" → removed from every chart. Roll back via the toast's `Undo`, the table checkboxes, or `Restore all excluded` |
| **Trend lines** | Settings → Advanced: linear / quadratic / log / exponential / power / moving-average fits per series (dash & width adjustable), optional **error band (±1σ/±2σ)** shading |
| **Shape group (3rd dimension)** | Settings → Data → Shape group: color = group 1, **marker shape = group 2**. E.g. color=method, shape=frames keeps method colors while distinguishing frames by shape |
| Text marker styling | Global font size/color/background/arrow in the Point labels group; per-marker color/size override in the click-to-edit popup |
| Line smoothing | Settings → Style → line shape: straight/spline, solid/dash/dot |
| **Area fill** | Settings → Style → Area fill: soft pastel band under each line in the series color |
| **Bar charts** | Type → Bar: **grouped/stacked**, **vertical/horizontal**, **aggregation** of rows sharing the same X (mean · sum · median · min · max · count), **error bars (±std dev/±std error)** with mean, **value labels** at bar ends, name/value **sorting**, opacity, **treat numeric X as categories** (even spacing) — Settings → Bar options. E.g. X=method, Y=accuracy, aggregate=mean |
| Point labels | Settings → Point labels: **drag** to fine-tune positions, **click** to hide individually. Duplicates collapse to one; overlaps auto-avoid |
| Pareto frontier | Settings → Advanced: pick the "better" direction (e.g. lower X · higher Y) |
| **Facet (small multiples)** | Settings → Data → Facet: split into a small chart per column value, laid out in a grid (small multiples without duplicate+filter) |
| **Per-chart data** | With two or more files loaded, each chart's settings start with a `Data` dropdown. Pick a file and the chart draws **only that file's rows**, with the axis, group and filter lists narrowed to **the columns that file actually has**. Different charts can point at different files, so unrelated datasets sit side by side (`(all)` merges them again) |
| **Label-join column** | Computed columns → kind `Label join`: instead of computing a value, it **joins values from several columns into a text column**, with per-part prefix/suffix text and a separator between them (e.g. `method` + `frames` → `baseline · 8frm`). The result works straight away as a group, facet, filter or bar X axis |
| **Computed columns** | "Computed columns" below the data input: derive a new column — binary op (A−B, A/B, …) or **delta/retention vs a reference** (e.g. vs dense). Source file untouched; usable directly as axis/filter |
| **Example data** | `Load example data` brings the 24-row basic set; `More examples` adds five companions (metadata, a wide CSV, standard deviations, repeated seeds, two backends orders of magnitude apart) so guide recipes ⑮⑯⑰ can be followed as written |
| **Melt (wide → long)** | The `⇲` button on a dataset chip: turns a file whose columns are spread sideways (`baseline, ours, ablation`) into **one row per measurement** as a new dataset. The original is untouched, and the new name column works as a group/facet/filter straight away |
| **Watch folder** | The `Watch folder` checkbox, shown when running via `visualizer.py`: **reloads files as they change**. Leave it on while a run is in progress — exclusions and fading survive, and a file that briefly disappears is not dropped from the screen |
| **Share as one HTML file** | `Export ▾` → `Share as one HTML file`: writes the current data and every chart setting **into a single file**. The recipient just double-clicks it — no tool, no session file. Build it from `index-offline.html` and it opens without internet too |
| **Join across files** | Computed columns → kind `Look up from another file`: finds a value in another file **by key and attaches it as one column** (e.g. `params_b` from `models.csv` onto `runs.csv`). Only columns present in **both** files are offered as keys, and picking one immediately tells you **how many rows will find a match**. Several matches fold via first/mean/sum/min/max/count. **Rows are never multiplied** |
| **Continuous color** | Settings → Data → Continuous color: color by a numeric column as a gradient (colorbar) — mutually exclusive with group color, scatter/line only |
| **Point aggregate · error bars** | Settings → Advanced → Point aggregate: summarize points sharing the same X (e.g. seed repeats) by mean/median/… + **error bars (±σ/SE) · error band** |
| **Focus / de-emphasize** | **Click** a point → "De-emphasize (fade)" → not excluded, just receded into a light-gray backdrop (focus + context). Keeps only the highlighted points/lines prominent. Restore via toast/table |
| **Export size** | Settings → Export size: presets for **paper 1-column (85mm), 2-column (170mm) and slides**, or mm/inch directly, plus dpi. The hint shows **the pixels it will save and the pt size of body text** (raising dpi does not change the physical text size — raise the font size for that). Report figures follow the same spec |
| **Error column** | Settings → Data → Error column: when the ± value **already exists as a column** (e.g. `score_std`), it is drawn as error bars directly. Ignored while aggregating (the aggregate error bars take over there) |
| **Span shading** | Settings → Baselines → `＋ Span`: paints a **range** on one axis and labels it (a recommended band, an out-of-memory region…). If a baseline is "one line", this is "this range" |
| **Stacked area** | Settings → Style → Area fill → `Stack`: stacks the series so the total and each share read together (line types only) |
| **Chart as table** | The card's `Table` button: shows the chart's own columns and filtered rows as a table. The only way to read the chart without seeing it, and handy for checking exact values |
| **Annotate an image** | `Export ▾` → `Annotate an image…`: a separate page (`annotate.html`) for putting **text, arrows, boxes and redactions** on a capture and saving it as PNG. Paste a screenshot straight in (⌘/Ctrl+V). The image never leaves the browser. **It is a separate file, so keep it next to `index.html`** |
| Export | `PNG` (3×) / `SVG` per card, `All charts PNG` (whole page in one image) in the top-bar `Export ▾` menu, `Export CSV` (current filtered data) in the table |
| **Rendering speed** | Settings → Style → Rendering: `Auto` (WebGL above 5,000 points) / `High quality (SVG)` / `Fast (WebGL)`. SVG export stays vector even in WebGL mode |
| Raw data | Bottom table: search, click-to-sort (**or Enter on the header**), per-dataset delete, **uncheck a row to exclude it from charts**, **`Fade` column to de-emphasise it**. Numeric columns are right-aligned so digits line up |
| **Keyboard & accessibility** | Usable without a mouse: a **skip-to-charts** link on the first Tab, a real label on every settings control, popovers and the modal move focus inside on open and back to the opening button on Escape (Tab cannot leak out of the modal), table headers sort on Enter. **Fade** — previously point-click only — has a table column, and **baselines can be added by value** from the settings panel |
| **Hide columns** | The table's `Columns n/m` button: unchecking one drops it from the table, axis pickers, filters and the analysis at once. **The data is untouched** and existing charts keep drawing (references are never cleared). For logs with 20-40 columns — `In use only` keeps just what the charts reference, `Show all` puts everything back |
| Sessions | Autosave (localStorage) + `Export/Import session` (JSON file, in the `Export ▾` menu) for sharing |
| **Built-in presets** | Top of the card's `Preset` button: average per item (bar), sweep trend (line), trade-off (Pareto), two-condition grid (heatmap), value distribution (box). They **assume no column names** — roles (category, sweep knob, score, cost) are matched against your current data by **value distribution**, so domain abbreviations work and identifier/seed columns are never used as axes, and a recipe whose roles cannot be filled is simply not listed |
| **Chart presets** | `Presets` button on each card: save the current chart's **settings only** (no data) under a name → re-apply with one click to any data using the same column names. Share via JSON `Export/Import` |

### Tip: which chart, when?

Chart-choice criteria (trend → line, magnitude → bar, trade-off → scatter), per-scenario recipes (mean + error bars,
stacked, rankings, Pareto…), third-dimension techniques, and presentation polish are collected in the
**[Visualization Guide (GUIDE.en.md)](GUIDE.en.md)**.

## Converting your data to this format (agent prompt)

Whatever format your logs or experiment results are in, copy the prompt below into any LLM agent (Claude, etc.)
together with your data file (or its path):

```text
Convert my data into a CSV or JSON file that satisfies the "input contract" below.

[Input contract — VTC Visualizer]
1. CSV (header on the first line) or a JSON array of objects. UTF-8 encoded.
2. Long-form (tidy): one row = one measurement point. Repeat rows for repeated measurements.
   (e.g. scores per method × token budget become rows with 3 columns: method,tokens,score)
3. No required columns, but follow these guidelines:
   - Put the thing being compared (method/model/config name) in one string column (e.g. "method")
     → it becomes the color group in charts.
   - Put each measure used as an axis (token count, time, score, …) in its own numeric column.
     Encode units in the column name (e.g. latency_s, cost_usd).
   - Put each condition (dataset, GPU type, …) in its own column → usable as filters.
4. Numeric columns must contain numbers only (no unit strings, no thousands separators; leave missing values empty).
5. Prefer lowercase_with_underscores column names. The name "_source" is reserved — do not use it.

Save the result as *.csv or *.json. Ask me if any conversion rule is ambiguous.
```

If you convert often, consider writing your own conversion script targeting the same contract.

## Rebuilding the offline version

If you modify `index.html`, regenerate the offline build:

```bash
python visualizer.py build-offline    # → index-offline.html (~4.6MB)
```

## Known limits (left this way on purpose)

Things that could be fixed but did not look worth it. Writing down the reason beats making the same call again later.

- **Analysis takes a while** — about 3 s on 50k rows with 20 continuous columns. The obvious target (regrouping rows per correlation pair) was precomputed as an experiment and only bought **10%** (3,177 → 2,865 ms) while adding a subtle ordering invariant, so it was reverted. A CPU profile shows the cost spread across many functions rather than concentrated. It is a press-a-button-and-wait operation, and the scan samples rows so it stays nearly flat as data grows.
- **Many open charts can hit the browser's WebGL context limit** — that is a browser cap. Pin Settings → Style → Rendering to `High quality (SVG)` to avoid it.
- **Built-in presets offer one set per dataset** — even with several continuous columns, one score and one cost are chosen. Offering every candidate makes the list unusable fast. Apply one and change the axes.
- **Folder watching polls every 4 seconds** — enough for a local folder.
- **A join definition produces one column** — attaching four metadata fields means four definitions. Letting one definition emit several would break the "one definition, one name" assumption behind deletion, name-collision checks and usage lookup.

## Requirements

- A modern browser (Chrome/Edge/Safari/Firefox)
- Python 3.8+ for `visualizer.py` (standard library only, nothing to install)

## Changelog

The version shows next to the title (top-right) and in the footer, matching the git tag (`v0.x`).

### v0.38.1 — the search box was squeezed until its text was cut

- The `One at a time` checkbox took room, so at the default width the search placeholder was **cut off**. The row now wraps instead of squeezing.
- The clipping check only ran at `Widest`, which is why it missed this — it now runs at the **default width** too.

### v0.38 — less scrolling in the settings panel

- The panel was **capped at 640px**, so a tall window bought you nothing. It now **follows the window height** (640 → 850px in a 1000px window).
- **One group opens at a time** (turn it off with `One at a time` above the panel). Fully expanded the panel was 3,400px, so finding anything meant a long scroll.
- **The series list starts folded** — 437px of the Style group's 975px was that list, which is why Style never fit any window. It is 554px now, and the folded state is remembered.
- Together, the distance you must scroll went from **2,808px to 77px** (default width, 1000px window).
- Search still expands several groups at once — `One at a time` only reacts to an actual click.

### v0.37.1 — text clipped inside its own control

- Fixed: the span `From` field cut its placeholder mid-character, the panel-width option `Widest` collided with the dropdown arrow, and the marker shape `triangle-up` was cut short.
- The box stays put and only the text is clipped, so the overflow check could not see it — the suite now measures text width against the room inside each control.

### v0.37 — settings panel width, and clipped labels

- The settings panel width is now yours to pick — **`Narrow · Default · Wide · Widest`**, next to the search box. The choice is remembered by the browser, applies to **every chart at once**, and widens the label column with it.
- **Bug fix**: in tight rows, button labels **broke apart vertically** (`Pin to value`, `+ Add`, `+ Span`) and the shading select and `×` on a baseline row **overflowed the panel** and were cut off. Rows now wrap instead, and the baseline's name is no longer pushed out of view.
- Numeric inputs were too narrow for their placeholder text; widened too.

### v0.36.1 — detaching a baseline from its point

- Baselines created by clicking a point now show a **`Pin to value`** button next to the `anchored to a point` badge — it freezes the line at the current value so it stays put when the data is refreshed. Until now the only way was to delete it and re-enter the number.
- The reverse is there too: a value-entered baseline gets **`Anchor to a point`** — press it, click a point, and the line follows that row.

### v0.36 — broken axis

- New chart type **`Broken axis`** — when values split into two far-apart groups (CPU 400 ms vs GPU 8 ms) the smaller group is pinned to the floor and its members cannot be told apart. The space between is folded away so **each group reads in its own range**.
- **Axis values stay real** — hover, the table, exported CSV and reports all report the unfolded numbers (folding the coordinates instead would make every one of them lie).
- The range is **automatic when left empty** (largest empty span, over 25% of the full range, at least two points on each side). If nothing is worth folding it draws as an ordinary chart **and says so**. You can enter a range yourself, or switch `Break` to the X axis.
- Baselines, text markers, the best-point label and shaded spans attach to **whichever panel holds their value** (a span crossing the break is drawn as two pieces).
- **Not available for bars** — a bar's length is the quantity, so breaking the axis makes the picture lie. For two different metrics, a secondary Y axis is the right tool.
- `More examples` now includes **`scales.csv`** (3 backends × 6 batch sizes) so guide recipe ⑲ can be followed as written.

### v0.35.1 — baselines vanished the moment they were created

- **Bug fix**: with two files holding the same values, or with a chart-level `Data` selection or filter, a baseline or marker made by clicking a point **disappeared immediately with "lost its anchor point"**. The anchor was looked up **across all rows instead of the rows actually drawn**, so it latched onto an identical row from another file or one removed by a filter. It now searches only the rows the chart draws.
- Anchors that were already broken are **restored when a point sits at exactly the stored coordinates**, so baselines and markers lost in earlier sessions come back. It never snaps to the nearest point — that would silently point at a different row, the very failure this machinery exists to prevent.

### v0.35 — baselines vanished when another file was loaded

- **Bug fix**: loading one more data file made click-created **baselines and text markers immediately report "lost their anchor point" and disappear** (one press of `More examples` reproduces it).
- The columns that identify a row were picked from **all files merged together**. Once a second file arrived, a column that exists only in that file was empty in every other row and therefore looked like a low-cardinality condition column — so measurements like `f1` and `latency_ms` entered row identity and every stored anchor stopped matching.
- Identity is now decided **per file**: a row is identified by the schema of the file it came from, so other files coming and going cannot shift it. Re-attaching excluded/dimmed marks when the same file is reloaded is stable for the same reason.
- Anchors from older sessions still resolve — the old-style key is looked up as well.

### v0.34 — per-series display

- Each series can now draw as **points only, line only, or points + line** independently within one chart
  (Settings → Style → Series; `Follow type` is the default). A reference curve as a line, raw data as points,
  the series you care about as points + line — until now the chart type drew every series the same way.
- Area fill, stacking, the secondary axis, the dimmed slice and small multiples all follow the per-series mode,
  so a series with no line never gets a fill band on its own.
- Old sessions open unchanged — an empty mode means "follow the chart type", exactly as before.

### v0.33 — a distribution recipe, companion data, and a dataset-scoping bug
- The guide gained **recipe ⑱, the spread of repeated runs** — the same data as box, violin and ECDF side by side, showing what a box hides.
- `More examples` now also loads **`seeds.csv`** (4 methods × 30 seeds). The basic example has only six values per method, too few to follow the recipe.
- **Bug fix**: distribution, heatmap and dumbbell charts **ignored the per-chart dataset selector** — they had done so since v0.19, silently mixing rows from other files into the picture. It surfaced while shooting the guide figures.

### v0.32.1 — violin and ECDF draw without an X axis
- Distribution charts need only a value column, but the render guard exempted histogram and box **by name**, so the newly added violin and ECDF demanded an X axis and showed nothing until one was picked.

### v0.32 — distribution shape, series order, best point
- **Violin** and **ECDF** charts. A box plot shows quartiles only, so **bimodality and tails disappear** — which matters when comparing repeated seeds. An ECDF answers "what fraction is at or below this value" straight off the picture (drawn as steps — joining the points with straight lines would assign probability to values never observed).
- **Series order** is adjustable with ↑↓. Until now it followed the order values appeared in the data, so putting `baseline` first meant reordering CSV rows. **The colour does not follow** — a colour belongs to the series, not to the position.
- **Mark best** labels the highest or lowest point automatically. That was a manual click-and-annotate every time. Where Pareto describes the whole frontier, this points at one.

### v0.31.1 — version label and an internal name
- The image annotation page still reported `v0.30` (v0.31 bumped only the main page).
- The internal series name for an ungrouped chart was going through the translation function. No such key existed, so it was accidentally safe — but filling in that "missing key" would have made **series colours and labels vanish on every language switch**.

### v0.31 — example data for following the recipes
- The data card gained a **`More examples (join · melt · error)`** button. It loads three companion datasets (`methods.csv`, `wide.csv`, `repeat.csv`) so guide recipes ⑮ melt, ⑯ join and ⑰ error column can be followed **exactly as written**.
- Joining needs two files and melting needs a wide one, so a single bundled example could not demonstrate either.
- `example.csv` is **left untouched** — one more column there would shift the analysis golden tests and the documented description together.

### v0.30 — the guide catches up with the tool
- **Three recipes added** to the visualisation guide: melting a wide CSV (⑮), attaching metadata from another file (⑯), and a figure that meets a submission spec (⑰).
- Existing recipes picked up the v0.26–v0.29 features: stacked area (④), chart as table (⑫), folder watching (⑬), plus an example of an annotated capture.
- Figures were shot **only for the new recipes.** Nothing in the palette, layout or plot face changed since r1–r10 were last captured, so re-shooting them would produce a diff and nothing else.

### v0.29.2 — drop-zone border and image replacement
- The **dashed border is dropped once an image is in**. "Drop here" has done its job by then and only adds noise; it returns while dragging so you still know the area accepts a file.
- **Loading a new image discards every annotation** — the one path with no undo — so it now asks first.
- (For reference: the blue dashed outline on the canvas is the **selection indicator**. It is on screen only and never lands in the export.)

### v0.29.1 — text backdrop on/off
- The white backdrop behind annotation text can now be **switched off** (`Text backdrop`) when it hides part of the picture.
- When on it is **fully opaque** — at 85% the lines and gridlines underneath showed through and muddied the text colour. A backdrop exists to make text readable, so it does not half-cover.
- Selecting a mark now **reflects its colour, width, font size and backdrop back into the inputs**.

### v0.29 — image annotation tool
- **There is now a page for labelling a capture** — `annotate.html`. Text, arrows, boxes, and a **redaction** block for covering sensitive values. Screenshots paste straight in.
- Coordinates are kept in original image pixels, so shrinking the view to fit your screen never shrinks **the exported file**, which comes out at full resolution (1x/2x).
- Language and theme are shared with the main page. The image never leaves the browser.
- **The file count went from 9 to 10.** This tool uses neither the chart library nor the data model, so folding it into the main page would only mix in unrelated code — the rule was relaxed once and locked again.

### v0.28 — baselines follow the data
- **A baseline made by clicking a point is now anchored to that point (row).** It used to hold only coordinates, so reloading a file — or a folder-watch refresh — moved the point to its new value while **the baseline stayed at the old spot**, with nothing on screen to say so. Same failure that text markers had until v0.15.
- **Baselines typed in as values stay pinned to the value.** A line at exactly `0.80` means the value, not some row.
- **A baseline that loses its anchor is not drawn.** The list shows ⚠ with the reason (point is gone / axis changed) and a `Re-anchor` button. A misplaced baseline goes straight into a report, so being silently wrong is the worst outcome.
- Analysis speed was **measured and left alone** — see "Known limits" below for why.

### v0.27 — how data gets in, and out
- **Sideways CSVs are accepted now.** The input contract assumes long form (one row per measurement), so a file with `baseline, ours, ablation` as columns was **stopped at the door** — axes, groups and filters all assume one column means one thing. The `⇲` button on a dataset chip melts it into a new dataset, leaving the original alone.
- **Watch folder**: leave it on during a run and new results arrive by themselves. Reloading goes through the existing path, so **exclusions and fading you marked by hand are kept**. A file that briefly disappears (mid-write, mid-rename) is not removed from the screen — you didn't delete it, and there would be no way back.
- **Share as one HTML file**: a session JSON is only useful to someone who already has the tool. Exporting a single file with the data and settings baked in means the recipient just double-clicks. Build it from `index-offline.html` and it needs no internet either.

### v0.26 — figures you can actually submit
- **Export size is now yours to set.** Exports were the on-screen size at 3×, so hitting a paper or report spec meant fixing it up elsewhere. Presets cover **1-column (85mm), 2-column (170mm) and slides**, or set mm/inch plus dpi yourself.
- The hint reports **the pixels it will save and the pt size of body text**, making it obvious on the spot that raising dpi does not enlarge the text (raise the font size for that). Figures in the markdown report follow the same spec.
- **The error column can be named directly.** Error bars only appeared when aggregating, so data that already carried `score_std` had no way to draw it.
- **Span shading** arrived. A baseline is a line, so it could never say "this range" — recommended bands, out-of-memory regions and the like now have a form.
- **Stacked area** works on line charts. Only bars could stack, so a share-over-time chart was out of reach. Stacking draws with SVG instead of WebGL (WebGL has no stacking and would silently overlay instead).
- **Charts can be shown as a table.** It is the only way to read a chart without seeing it, and it is where you check an exact value.

### v0.25 — joining across files
- **Values from another file can be looked up by key.** Computed columns gained the kind `Look up from another file` — keep `runs.csv` (measurements) and `models.csv` (metadata such as parameters and price) separate and still use both in one chart. Until now merging files only stacked rows, so this shape was out of reach.
- **Rows are never multiplied.** Only a column is attached — growing the row set would break the notion of "the same row" that exclusions, fading, point labels and text-marker anchors all rely on. Several matches fold via first/mean/sum/min/max/count.
- **No silently empty column**: only columns present in both files are offered as keys, and picking one immediately counts how many rows will find a match. Unmatched rows get a blank, not a zero.
- Computed columns defined earlier can serve as the key — build a composite one with `Label join` and match on two columns at once (definition order is evaluation order).
- **Bug fix**: computed columns were leaking into how "the same row" is recognised, so re-loading the same file while a computed column existed **wiped every exclusion and fade you had marked by hand**. Computed columns are regenerated from the data, so they are now excluded from that identity.

### v0.24 — reachable by keyboard, a less crowded panel
- **The tool now works without a mouse.** Until now most settings controls had a visible label but no programmatic one (zero `<label>` associations), popovers could not be tabbed into, and sorting the table was click-only.
- **Fade (de-emphasise) now has a checkbox in the table.** Clicking a point was previously the only way to reach it at all.
- **Baselines can be added by value** from the settings panel (`＋ Add` in the baseline group). Clicking could only place one on an existing data point, so a line at exactly `0.80` was impossible.
- Table headers **take focus and sort on Enter**, announce their sort direction, and keep focus after sorting.
- Popovers and the modal **move focus inside when opened and return it to the button that opened them on Escape.** Tabbing out of a popover closes it, and Tab no longer leaks out of the modal.
- **Text markers can be created by picking a row** (Settings → Point labels → `＋ Text marker`). Clicking a point is the natural gesture, but the anchor is a row either way — this is the same choice through a different door. Past 300 rows it points you back to clicking.
- The body is wrapped in a `main` landmark, there is a **skip-to-charts** link, and every chart card carries a name.
- **Settings groups remember whether they were open** — no more re-expanding them after every reload.
- Settings search also matches **option names** (e.g. `log`), and says so instead of going blank when nothing matches. Series style lists fold up once there are more than six series.

### v0.23 — subfolder autoload and launcher cleanup
- **Autoload now reaches into subfolders.** Split your results across `results/a/run1.csv` and they all load at once, listed as relative paths.
- **Hidden folders (`.git`, `.venv`, `.ipynb_checkpoints`, …) and symlinks pointing outside the folder are skipped** — tool config files have no business being read as data, and following links either escapes the folder or loops forever. The list stops at 500 files.
- **The outside-the-folder guard now catches symlinks too**: paths are resolved to their real location before the check.
- `--host` picks the bind address (still `127.0.0.1` by default). Binding to **`0.0.0.0` lets anyone on your network read that folder**, so it now prints a warning at startup.
- Requests are served on threads, so reading a large file no longer freezes the page. The offline build gives up after 15 seconds with a reason when the CDN doesn't answer.
- Internal: the all-rows list is memoised, cutting repeated scans while building config panels.

### v0.22 — half-width cards and the figures in the docs
- **Fixed the header buttons folding in half-width cards.** `Reset view` broke into two lines that spilled out of the button box. The buttons now keep their width and the header gains a second row when space runs out.
- **All 14 figures in the docs were re-shot.** Twelve commits had changed the UI since v0.16 while the images stood still — the Pareto figure in particular still showed the grey dashed frontier, contradicting the text beside it.

### v0.21.2 — and its colour
- The frontier line's **colour** is selectable too. **Left blank it follows the theme** as before (light/dark automatically); set it and it stays that colour.
- Once a colour is set, an `Auto` button appears next to it to go back to the theme — a colour input cannot hold an empty value, so the way back needs its own control.
- **If you use both themes, leaving it blank is the better default:** a fixed colour stays fixed in dark mode and may lose contrast on one of them.

### v0.21.1 — choosing the frontier line style
- The frontier line's **style (solid / dashed / dotted / dash-dot) and width** are now selectable (Advanced → Pareto). The default stays solid at width 2.
- On `Scatter + line` charts the series lines are solid too, so switching the frontier back to dashed keeps them apart.
- **The colour is deliberately not exposed.** The frontier is a verdict about all the points, not about one series, so a series colour would read as that group's line. It stays theme ink and follows light/dark only.

### v0.21 — a readable Pareto chart
- **The frontier is now a solid ink line instead of a grey dashed one.** It shared a tone with the baselines and sank into the background, and you could not tell which points it touched. Now the points it touches read as the candidates.
- **`Fade dominated points`** is a new option (Advanced → under Pareto). With it on, only the points on the frontier stay solid and the rest recede. Faded points keep their series color, so group identity is still readable.
- A faded legend swatch means that series **put nothing on the frontier** — a method that is dominated everywhere is visible at a glance.
- The frontier is computed **over all points regardless of group** (as it always was): the points it touches are the configurations worth choosing.

### v0.20.1 — Pareto re-checked
- **With point aggregation on, the frontier was drawn in the wrong place.** The visible points were means while the frontier came from the raw rows, so the dashed line passed through none of them. It now follows **the points actually drawn**.
- **Dimmed rows no longer define the frontier** — the same reason trend lines already skip them: a point pushed into the background should not set the boundary.
- **Not drawn in facet mode.** A frontier computed over all the data used to sit on the first panel only, inviting a wrong reading of the others (same treatment as baselines, markers and labels).
- The legend said `Pareto frontier` even in Korean; it now follows the language.
- The frontier computation itself (all four directions) was checked against an independent implementation and is **correct**.

### v0.20 — filters say what they are doing
- Each filter now shows **how many rows it currently matches**, in words — `6 of 24 rows match — the other 18 are dropped` — and the count follows along while you type the value.
- **You pick which side is affected.** There are now four modes — `Drop others` (default) · `Drop matching` · `Dim others` · `Dim matching`. `method = baseline` + `Dim matching` fades baseline; `Dim others` does the opposite. Previously only one direction existed, which was easy to read backwards.
- The names state the target, and the sentence confirms it with live row counts — a wrong pick shows up in the numbers first.
- The cramped filter row is fixed too: the controls have minimum widths and wrap onto a second line when the panel is narrow.

### v0.19 — looking at files separately
- With two or more files loaded, every chart gets a **`Data` dropdown** choosing which one it draws. Only that file's rows are used, and **the column lists narrow to that file** — no more picking a column the selected file does not have.
- Since it is per chart, **two unrelated datasets can sit side by side** on one page. `(all)` goes back to the merged view.
- Switching files **clears the axis/group/filter settings that no longer apply** and says which ones. Deleting the file a chart points at returns it to `(all)` with the same cleanup.
- Splitting by file was already possible via the `_source` column (as a facet, group or filter). This is a shortcut on top of that — for overlaying files in one chart, facet by `_source` is still the way.

### v0.18 — one column for a combination of conditions
- Computed columns gained a **`Label join`** kind: rather than computing a value it joins values from several columns into a text column — `selector` + `frames` → `sal-v3.1 · 16frm`.
- Each part takes **text before and after** (`16` → `16frm`), the parts are joined by a **separator** you choose, and you can add as many parts as you need.
- Because the result is text it drops straight into **group (color), facet, filter and the bar X axis**, so "one row per condition combination" is a couple of clicks away.
- Parts with no value are skipped, so you never get a lone separator; if every part is empty the row has no value.

### v0.17.1 — right even when the names mean nothing
- Role matching for the built-in presets moved **from name patterns to value distribution**, reusing the same column classification the analysis engine uses: categories, sweep knobs, continuous measures and identifiers are told apart by their values, and names only decide which of two continuous columns is the score and which is the cost.
- So data named `zeta` and `kv` gets sensible axes, and a `seed_id` never ends up on one.
- The trade-off preset now prefers a continuous column (latency and such) over a sweep knob for X — using the knob just reproduces the sweep preset.

### v0.17 — something to click on first open
- The card's `Preset` button now offers **five built-ins** (average per item, sweep trend, trade-off, two-condition grid, value distribution), so an empty preset list is no longer a dead end.
- They hard-code no column names: **roles are matched against the current data** — a categorical column, a sweep knob with few distinct values, a score-like and a cost-like numeric. A recipe whose roles cannot be filled is never listed, so clicking one never yields a blank chart.
- A log X axis is switched on only for genuinely multiplicative sweeps (judged by max/min ratio).
- Fixed alongside: **histograms and box plots refused to draw without an X column**, though they need only the one value column.

### v0.16.1 — where presets and hiding collided
- Applying a preset that uses a hidden column now **unhides that column**. No more half-state where the chart draws but the axis picker cannot offer the column again — the same treatment the preset's computed columns already got.
- Fixed: a preset did not carry the computed column used on its **secondary Y axis**, so that axis came up empty for whoever received it.
- What a preset application did on the side (restoring computed columns, unhiding) now rides **in the same notice**. Previously the toast was overwritten immediately and never seen.

### v0.16 — holding up when there are many columns
**Hiding columns**
- Unchecking a column in the table's `Columns n/m` button drops it from **the table, axis pickers, filters and the analysis at once**. No more scrolling a 40-entry dropdown to pick an axis.
- **Hiding is not deleting.** The rows are untouched and no reference is cleared, so a chart already drawn on a hidden column keeps drawing. The list shows where each column is used (`Chart 1`, computed-column names).
- There is deliberately no way to **delete** a column from the data. Rows are identified by the combination of their condition columns, so removing one would misalign exclusions, point labels and text-marker anchors. The original is in your file — reload it.

**Table and chrome**
- Numeric columns are right-aligned, so digits line up (`150` vs `23412.3`).
- The four header export buttons collapsed into one `Export ▾` menu.
- The file drop area shrinks to a single line once data is loaded.
- Fixed alongside: a computed column used as the **secondary axis** was not detected when deleting it.

### v0.15 — annotations follow the data
**Text markers are anchored to their point**
- Creating a marker now stores the **identity of the point you clicked** (its condition columns — method, tokens, …) alongside the coordinates, and every render re-reads that row's current values. Refresh the data and the callout still points at the same point. Markers from older sessions keep their coordinate behaviour.

**Nothing drifts silently**
- If the anchor row disappears (filter, exclusion, replaced data) or the axis column changes so the coordinates no longer mean anything, the marker is **not drawn**, and a toast says so. A misplaced annotation goes straight into a report, so vanishing beats sitting in the wrong spot.
- The Settings → Point labels list keeps it with a ⚠ and the reason (`axis changed` / `point is gone`); hit `Re-anchor` and click a point to attach it somewhere new.

**Notes that belong to no point**
- `＋ Pinned note` adds a note fixed to the plot area (`n=24 · measured 2026-07`, measurement conditions, provenance). It survives any data change or axis switch, and drags anywhere.

### v0.14 — refresh, distributions, second axis, safety
**Hand work survives a data refresh**
- Reloading the same file **carries over excluded/faded rows and label positions**. Rows are matched by their condition columns (method, tokens…), so updated values still map to the same row. Previously this had to be redone every week.

**New charts and axes**
- **Histogram · box plot** for the spread of repeated measurements; a group overlays one distribution per level.
- **Second Y axis (right)** for two metrics on different scales (accuracy vs latency), drawn with a dotted line and × markers.
- **Tick formats**: percent, thousands, scientific, fixed decimals.
- **Trendline fit readout**: R², slope and n in the corner of the chart (can be turned off in Settings → Advanced).

**Legend fixes**
- **A shape group alone now splits the series.** With no color group set, the shape group used to be ignored entirely, collapsing everything into one series with no legend.
- **The legend disappears only when set to `Hidden`.** Single-series charts show one too, labelled with the column being plotted.
- Charts with only a second Y axis, and histograms/box plots, now follow the legend position and hide settings like every other type.

**Themes and screen polish**
- **Pick a chart palette** from the top bar. The default is the palette you have been using; `Carbon` (IBM design system), `Okabe-Ito` (the colorblind-safe academic standard) and `Ink` (print-leaning) are available. The choice persists and travels with the session.
- **The dark palette was corrected.** The previous dark colors sat above the lightness band for a dark surface (0.68–0.81); hues are unchanged, only lightness and chroma moved back into range.
- All four palettes pass **lightness band · chroma floor · CVD (red-green/blue-yellow) adjacent separation · normal-vision separation · surface contrast**, in light and dark separately.
- **Plot face**: Settings → Axes → Plot face (`None` / `Very light` / `Light`). Tinting the data area switches the grid to white so it recedes behind the marks (the ggplot/Economist treatment); each palette has its own tone, and dark mode lightens the face instead. Default is `None` — figures for papers usually want a white face.
- Screen: header buttons grouped into **primary / export / view**, four type sizes instead of a mix, spacing on a 4px rhythm, one control height and radius, a soft shadow so charts read as paper, and an empty state that leads with `Load example data`.
- Turning on the second Y axis now shows a **caution note** — two scales can manufacture a correlation depending on how each axis is framed.

**Safety and housekeeping**
- Deleting a dataset now asks first and can be undone; applying a preset can be undone.
- **Option search** in the settings panel: type "legend" or "log" and only matching options remain.
- **One file to share**: presets and view settings (language, theme, width) travel inside the session. Presets with the same name are kept, and view settings apply only where the recipient has not chosen one yet.
- `python visualizer.py logs/ --offline` serves the **offline build with folder autoload**, which used to be mutually exclusive.
- Analysis: group comparisons state how many levels were compared, Simpson warnings split into "reversed" and "diluted" wordings, and large-data sampling moved from systematic to deterministic random.

### v0.13.1 — deleting computed columns
- Deleting a computed column now **lists the charts and other computed columns that use it and asks first** — the action cannot be undone.
- On delete the affected charts' axis and filter settings are **cleared too**, and a toast says what was cleared. Previously those settings kept pointing at a column that no longer existed: the chart went blank while its settings panel showed "(pick one)".
- Columns nothing depends on are still deleted straight away, without a prompt.

### v0.13 — speed
Measured the slow paths on large data and fixed them (numbers at 20k rows).
- **Charts using a size column: 49.5s → 0.43s.** The size range was recomputed for every single point; it is now computed once per render (at 50k rows the chart effectively never appeared).
- **Opening a settings panel: 57ms → 2ms** — the column list, numeric detection and unique values are recomputed only when the data changes.
- **Automatic WebGL**: above 5,000 points charts render with WebGL (a 30k-point scatter goes from 949ms to 18ms of render time). Pin `High quality (SVG)` in Settings → Style → Rendering if you prefer, and **SVG export temporarily switches back to vector**, so figures for papers keep their quality.

### v0.12.1 — review fixes
- **Captions were silently lost**: reopening the settings panel showed an empty caption box, and typing one character there replaced the whole caption.
- **Analysis**: the trivial correlation between a computed column and its source (e.g. `accuracy` and its z-score) is no longer reported as a finding.
- **Analysis**: two-valued conditions (an A/B flag like `fp16` on/off) are now group-comparison candidates; they used to be dropped silently, producing no findings at all.
- **Analysis**: curves that rise and then fall back are no longer reported as "saturation" with a share above 100%.
- **Analysis**: the outlier list keeps the most extreme cases instead of whichever was scanned first.
- Also fixed: console errors when resizing with a collapsed chart, a possible id collision when undoing a chart deletion, and a failed chart image aborting the rest of a report export.

### v0.12 — usability, reports, computed columns

**Usability**
- **State is preserved**: adding a chart or switching language no longer resets **zoom and the collapsed/expanded state of settings groups** (previously every card was rebuilt from scratch).
- **Undo chart deletion**: the toast's `Undo` restores the chart with its axes, colors and baselines intact.
- **Reorder and collapse cards**: `↑`/`↓` in the card header change the order, `▾` folds the plot away so long pages read as a list.
- **Copy filters to other charts**: `Copy these filters to…` in Settings → Filters applies the same conditions to one or all charts.
- **Example data button**: with no data loaded, `Load example data` gets you a chart in one click — it works even when the file is opened by double-clicking.
- Keyboard & accessibility: `ESC` closes modals and popovers, the paste box takes focus when opened, focus outlines, titles on icon-only buttons, screen-reader announcements for toasts.

**From charts to a report**
- **Chart captions**: Settings → Style → Caption. Shown under the chart and carried into the report.
- **`Export ▾` → `Report MD`**: saves a markdown report (.md) together with the chart PNGs. Each chart section carries its **caption, chart setup (type/axes/group) and the filters in effect**, and if you ran the analysis, the **findings summary and its caveat** are appended.
- **`Copy findings`**: copies the analysis findings as a markdown list (works in the offline file too).

**Richer computed columns**
- **Constant operands**: type a number in the second slot of a binary operation (e.g. `latency_ms ÷ 1000`, `cost_usd × 1000`). Which unit reads better depends on your data and your audience — the tool does not push either way.
- **Normalize**: 0–1, % of max, or z-score — **over the whole data or within a group**.
- **Rank**: ascending/descending, overall or within a group (e.g. rank inside each method).
- **Bin**: equal-width bins whose labels are strings, so they can be used directly as groups or filters.
- **Group aggregate**: broadcast a group's mean/sum/min/max/count onto every row (combine with reference-delta for relative values).
- Definitions can be **edited** (`✎`) and **reordered** (`↑`/`↓`), which matters when one computed column feeds another.
- **Presets now carry the computed-column definitions they use**, so a preset built on a derived axis also works for whoever you send it to (missing definitions are recreated).

### v0.11.1 — analysis consistency fixes
- Excluding or restoring rows in the table now **marks the analysis stale immediately** (previously the panel kept showing insights computed before the exclusion).
- When a folder is served by `visualizer.py`, **files that changed are re-read** instead of being skipped, so updated logs actually show up.
- Autosave failures caused by storage limits are reported instead of being swallowed.
- Dropping back to a single dataset clears axis/group/filter settings that referenced `_source`.
- Analysis: **when there is more than one design value (condition), pairing now happens on the combination** rather than the first one only. Design values that map one-to-one collapse into one representative, and the group-candidate limit is raised to 24 so comparisons across ~20 models still work.
- The panel now shows a **scan-scope line** (group candidates, design values, excluded columns and why), so an empty result explains itself.

### v0.11 — automatic analysis panel
- An **`Analyze` button** in the top bar: column profile (kind, missing, unique, min/median/max/mean/sd), automatic findings, and a profile CSV export.
- Findings come in three tiers — **Data (integrity) → Caution (confounding) → Finding**: constant/empty columns, non-numeric values mixed into
  numbers, duplicate rows, group-biased missingness, unmeasured combinations / Simpson's paradox and crossovers / correlations, group
  differences, saturation points, outliers.
- **Suppressing false findings is the core of it**: columns that are definitionally the same (e.g. cost = latency × 5e-4) collapse into one
  representative, design knobs are never correlated against each other, and a pooled correlation that disagrees with the per-group ones is
  reported as a warning instead of a number. Outliers are judged by MAD within repeated cells or on local trend residuals, and never auto-removed.
- **No p-values and no "significant"** — reliability is shown as the raw difference, direction consistency across conditions (e.g. 6 of 6 agree) and a **bootstrap interval (95%)**. Resampling happens over measured conditions (blocks), not rows, because benchmark rows are not independent; a deterministic RNG keeps the interval identical for identical data. Findings whose interval spans zero are not reported.
- Results are never stored in the session and are discarded when the data changes. All finding sentences exist in both KO and EN.

### v0.10 — heatmap & dumbbell charts
- **Heatmap**: a grid over two discrete axes colored by a value (e.g. X=frames, Y=gazing_ratio, color=accuracy) — a 2D sweep at a glance.
- **Dumbbell (paired)**: two conditions per category (e.g. pretrained/tuned) as dots joined by a line — the difference reads directly.

### v0.9 — page width
- A **width toggle** in the top bar (Normal 1280px / Wide 1660px / Full = fill the screen). Shrinks side margins on wide monitors for bigger charts. Remembered.

### v0.8 — dark mode
- **Light/dark theme** toggle (top-right 🌙/☀️). Follows the OS setting on first run; your choice is then remembered. Chart surface, axes and palette are tuned for dark (not a naive invert).

### v0.7 — chart size & layout
- **Per-chart height slider** (280–820px) and **full / half width**. Set two charts to half width to place them side by side, like a mini dashboard.

### v0.6.1 — bug fix
- Adding/removing a computed column now **updates the axis/group dropdowns of open chart settings immediately** (previously you had to reopen the panel).

### v0.6 — dim filters
- **"Dim" filter mode**: instead of removing non-matching rows, fade them into the background → rule-based highlight (focus + context). Automates what used to be per-point de-emphasis.

### v0.5 — small multiples & computed columns
- **Facet (small multiples)**: split into a grid by column value — small multiples without repeated duplicate+filter.
- **Computed columns**: derive columns in-tool (binary ops, delta/retention vs a reference); source file untouched, saved in the session.

### v0.4 — analysis & reporting
- **Continuous color**: color by a numeric column as a gradient (colorbar).
- **Point aggregate · error bars · band**: summarize repeated measurements at the same X by mean, etc. (line/scatter).
- **Focus / de-emphasize (focus + context)**: fade points into the background instead of excluding them, to spotlight what matters.
- **Export**: all charts as one PNG; current filtered data as CSV.

### v0.3 — legend improvements
- Legend placement inside the chart by **corner** (top-left/top-right/bottom-left/bottom-right).
- **Editable legend names** (display only; internal identifiers unchanged).

### v0.2 — bar charts, guide, presets
- **Bar charts**: grouped/stacked, horizontal, aggregation (mean, etc.), error bars, value labels, sorting.
- **Visualization guide** (GUIDE.md/en) with example captures.
- **Chart presets**: save chart settings only → re-apply to new data.
- Baseline direction (crosshair/h/v), log-axis baseline placement fix, numeric multi-select filters, session-file-as-data guard, version badge.

### v0.1 — initial release
- Scatter/line/scatter+line, log axes, axis ranges, series styling, filters, baselines (quadrant shading), text markers, point labels, trendlines & error bands, Pareto, shape group, area fill, sessions, PNG/SVG, KO/EN, offline build, English docs.

---

© mrc
