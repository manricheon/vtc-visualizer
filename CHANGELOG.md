# Changelog

All notable changes, newest first. Versions match the git tags (`v0.x`) and the version shown in the app's header.
변경 이력입니다. 최신이 위에 있고, 버전은 git 태그·앱 헤더 표시와 같습니다.

### v0.55 — the way data comes in
> v0.55 — 데이터가 들어오는 길

- **Paste is the entrance people actually use**, and it was the one with no preview. `⌘/Ctrl+V` now works anywhere on the page (it is not intercepted while you are typing in a field), and before you press `Add` the box tells you `24 rows × 5 columns — method, tokens, …`, how the delimiter and decimals were read, and whether the name matches an existing dataset (which means *update*, keeping your excluded and dimmed marks).
- **A file that could not be read used to open a browser dialog per file.** Dropping 20 files with 3 broken ones meant closing three boxes. They are now collected into the one-line report autoload already used, and parse errors in the paste box are shown in place with your text left intact.
- **Loading several files redrew the table and every chart once per file** — 10 files × 500 rows took **1,520ms; now 245ms**. The refresh happens once, at the end. Cache invalidation still happens per file (row identity must not read a stale column list).
- **When storage filled up, autosave switched off with a toast that vanished after five seconds.** Everything after that looked normal while nothing was being saved — and a refresh silently restored the older session. A `Not saving` button now stays in the top bar (click to export), and the next launch says the restored session predates those changes.

### v0.54 — the docs, rewritten to be read
> v0.54 — 읽으라고 쓴 문서

- No code paths changed. What changed is everything a reader sees first.
- **The English README opened with a broken table cell above its own title**, and the two feature descriptions cut off with it (reordering cards, per-series area fill) were missing entirely. Both are back.
- **Guide recipe ⑱ (join across files) could not be followed** — it named `models.csv` with key `model`, and neither exists. It now uses the companion file the app actually ships (`methods.csv`, key `method`, column `params_b`).
- The changelog moved out of both READMEs into this file. They now open with a five-minute walkthrough — open it, drop a file, click a recipe chip, change the axes, export — instead of a parser-exceptions table.
- **Guide recipes are numbered in the order they appear** (①–⑳), the beginner topic (choosing colours) moved forward, and every figure file is named for its recipe.
- Corrected: filters have four modes, not two; `More examples` adds five files, not three; the offline build is 4.8MB; the duplicate card row in the feature table is merged; `© mrc` is at the end of every document rather than inside a folded section.
- Documentation is now checked before release like code is: relative links and anchors resolve, guide recipes only name files that exist, recipe numbers match file order, figure names match recipe numbers.

### v0.53 — columns that vanished, failures that said nothing
> v0.53 — 사라지던 컬럼과 침묵하던 실패

- **A column named `_id` disappeared from the whole UI.** `_` is the tool's internal namespace, so a column literally named `_excluded` **dropped those rows from every chart**. Such columns are now **renamed on load** (`id`, or `id_2`) and reported. The rule is deterministic, so reloading the same file keeps your excluded/dimmed marks.
- **A file containing a column named like one of your computed columns destroyed the file's values.** Now **the file wins** — the computed column is renamed to `name (calc)` and everything that referenced it follows: **axes, error column, filters, dependent definitions, hidden columns, table sort, and the axis stamp on markers and baselines** (saved presets are left alone — they belong to other data too).
- **Autoload used to fail silently.** Unreadable files are collected and reported as `Could not read N file(s) — Details`, with the reason. A folder past the 500-file cap now says so.
- **Files that are not UTF-8** are refused with a clear message instead of rendering as `���`.
- A numeric column with one stray string **used to disappear from the axis pickers with no explanation** — the settings panel now says which column and how many values are not numeric.
- Also: the list of chart fields that hold a column name existed in **three copies, one of them missing `y2`, `size` and the error column**. Now there is one.

### v0.52 — what used to hang, and what used to be quietly wrong (all measured)
> v0.52 — 멈추던 것과 조용히 틀리던 것 (전부 실측)

- **One 200k-character cell froze the tab for 97 seconds.** The number-detection regex I added in v0.51 left a backtracking hole and ran O(n²) — **97,064ms → 36ms**. A length cap now short-circuits it (nothing that long is a number).
- **The heatmap re-scanned every row for every cell.** It already built a one-pass aggregate and then **never used it** — 50k rows across two continuous axes went **74,275ms → 45ms**. Min and max fold into the same pass.
- **A normalized computed column would not draw at 130k rows** (a stack overflow that only reached the console). Seven places that took the min/max of a row-sized array now loop instead — **error → 45ms**.
- **Excluding the largest point from the table left the bubble scale keyed to it** — exclusions do not change the data, so the cache never noticed.
- Removing a dataset, or reloading the same name through another path (melt, JSON), left `ⓘ` showing **the previous file's** reading. Fixed.
- Saving a preset with a full storage quota threw instead of reporting — it now follows the same rule as session autosave.

### v0.51 — the values it used to read wrong
> v0.51 — 조용히 틀리게 읽던 값들

- **European decimals were off by 1000×.** `1.234,5` became `1.2345` and was plotted as such. The format is now decided from the whole column — and **if European and US formats are mixed the column stays text** (picking one would make half the values wrong).
- **Semicolon and pipe CSVs** are read (what European Excel exports by default). The delimiter is chosen by which one makes the body match the header, so a comma inside a value in a single-column file is no longer mistaken for a delimiter.
- `N/A`, `NaN`, `-`, `null` and `inf` count as missing **only when the rest of the column is numeric**. One such value used to turn the whole column into text, which **removed it from every axis picker**. In a text column, `-` stays a value.
- `007` and integers of 16+ digits are **kept as text** (converting them is irreversible).
- Fixed a `"` in the middle of a field **silently deleting the quotes** (`He said "hi"`).
- Duplicate and empty headers are renamed (`name (2)`, `column 3`) instead of dropped. Rows of a different length are counted.
- The **`ⓘ`** on a dataset chip records how the file was read (delimiter, per-column format, missing count, renames, odd rows). **A file that read plainly says nothing** — you only get a line when a value was reinterpreted.
- Dropping a file that is not CSV/TSV/JSON now **says it was skipped** (it used to do nothing at all).

### v0.50 — narrow screens, and the annotation tool's dialog
> v0.50 — 좁은 화면과 주석 도구의 대화 상자

- **Popovers no longer run off-screen.** Placement used fixed constants (230×140); it now measures the popover, caps it (`min(92vw, 420px)` × `min(78vh, 620px)`) and lets it scroll. The sheet popover's chart list scrolls inside itself, so it stays usable even in a 480px window.
- The data-card header **wraps** when space runs out, instead of truncating the summary.
- The annotation tool got its **first width breakpoint** — it had no width media query at all until now.
- Its `join / replace` dialog now follows the **same rules as the main modals**: focus moves inside, Tab cannot escape the box, and Escape returns focus to the button that opened it. Clicking the backdrop closes it **without** stealing focus back — it must not grab what you just clicked.

### v0.49 — one rule for undo
> v0.49 — 되돌리기를 한 규칙으로

- Undo was **uneven** — copying the look had it, **copying filters did not**, and deleting a marker, baseline or span was final. All of these now carry `Undo`: **copying filters · deleting markers/baselines/spans · showing all columns · deleting a saved preset · importing a session · un-dimming points**.
- Deletions from a list come back **to their original position**. Re-appending at the end changes the order, which reads as "I undid it and it still changed".
- **Importing a session** replaces everything you were working on and could not be undone. The previous saved state is kept and restored on undo (the cheapest possible snapshot — no data copying).
- Copying filters and copying the look were **the same screen and nearly the same code**, so they are now one function — which is also why undo had gone missing from one of them.
- **Actions that already confirm do not also offer undo** (reset everything, remove a dataset). Asking twice devalues the question.

### v0.48 — three bugs the audit turned up
> v0.48 — 점검이 찾아낸 버그 셋

- **Fix ①**: `Reset everything` did **not clear computed-column definitions**. Right after the reset, autosave wrote them straight back into the storage it had just cleared, so they survived a refresh.
- **Fix ②**: joining an image in the annotation tool **wiped the whole undo history** (the join itself, and every mark placed before it). Undo entries only held marks, so an image change could not be represented — they now carry the image too, and `⌘Z` steps back past a join.
- **Fix ③**: in the sheet layout, switching the unit to `Screen size` **hid the gap input** along with width and dpi. The gap has nothing to do with the unit, so it now stays.

### v0.47 — the guide catches up with the tool
> v0.47 — 가이드가 도구를 따라잡음

- The visualization guide (both languages) had **stalled at v0.41.** Nothing from v0.42–v0.46 had reached the recipes, so following the guide led to places that no longer matched the screen.
- Added **two orientation lines** ahead of the recipes — build the first chart from the `Try one of these:` chips, and remember the settings panel starts in `Essentials`, so anything you cannot see is one search (or one click) away.
- New recipe **⑳ Four figures on one sheet** (panel layout), including that the width is the width of the whole sheet and that each panel keeps its own aspect ratio. One new figure (`r18-sheet.png`).
- Folded into existing recipes: **baseline names and one-sided shading** (⑰ submission spec), **per-series area fill** (④ cost breakdown), **card shortcuts and copying the look** (⑦ presentation polish).

### v0.46.1 — what the full audit turned up
> v0.46.1 — 전체 점검에서 나온 것들

- Ran a full pass over the code, docs and features: **40 suites, 736 checks green**; opened the offline file with the network cut and confirmed **all 11 chart types draw with zero outbound requests**; round-tripped **all 93 chart-config fields** through a session export/import without drift; and verified the 64 git tags line up 1:1 with the 64 changelog entries.
- Cleared the leftovers it found: a function nobody calls (`labelSetting`), an unused constant (`DARK_PALETTE`), and one dictionary string that never reached the screen.
- **Recipe chips are undoable** — `applyPreset` always had undo, but the message only said "Preset applied", so it was hard to tell what had changed. It now names the recipe you clicked, and **toasts that carry an undo stay for 9 seconds** (5 was gone before you finished reading).
- That string got a home instead of being deleted — the card keyboard shortcuts are now on the card itself (`aria-keyshortcuts` plus a tooltip). The on-screen hint line is **hidden when a card is collapsed**, so collapsed cards had no way to tell you the shortcuts.

### v0.46 — sheet layout, bulk look, shortcuts, and two images side by side
> v0.46 — 조판·일괄 적용·단축키, 그리고 두 그림 나란히

- **Export several figures on one sheet** (`Export ▾` → `Several figures on one sheet…`). The submission spec landed in v0.26, but the final layout was still done by hand. Pick columns (1–4), panel labels (`(a) (b) (c)`…), sheet width in mm/inch with a dpi, the gap, and which charts to include. **Every panel keeps the aspect ratio it has on screen** — stretching panels to equal heights would give each one a different tick spacing, which makes the comparison lie.
- **Copy the look to other charts** in one action (Settings → Style). Only "how it looks" travels — font, text size, legend position, chart size, tick format, export spec — and **axes, group and filters never do** (each chart draws different data). Since it changes several charts at once, it comes with **undo**.
- **Card shortcuts**: with focus inside a card, `Alt+↑`/`Alt+↓` reorder it and `Alt+←`/`Alt+→` collapse or expand it. No letter keys, so nothing collides with typing.
- **Two images side by side in the annotation tool.** "Before/after" or "ours vs baseline" only reads when the two captures are one image — loading a second image now asks `Join on the right / Join below / Replace`, and **joining leaves the marks you already placed exactly where they were**.

### v0.45 — a collapsible data card, and a documentation cleanup
> v0.45 — 데이터 카드 접기, 그리고 문서 정리

- **The data-input card now collapses** (`▾` in its header). Once the files are in, that card held 245px of nothing to do — collapsed it is 52px and the first chart starts at 142px instead of 335px. **Dropping files still works while collapsed** (the whole page has always been a drop target). It never collapses while there is no data — a first-time visitor would lose the place to start.
- **Documentation cleanup**: ① v0.43 moved aggregation and error into one row but left **ten stale labels** in the feature table and the guide (`Bar options → Aggregate`, `Advanced → Point aggregate`, `Error column`) — following the docs led to a setting that was no longer there. ② The 63-row feature table is now **five grouped tables** (getting data in / drawing / readability / baselines and annotations / exporting). ③ Changelog entries older than v0.40 are folded away.

### v0.44 — let baselines do their job, and fill per series
> v0.44 — 기준선이 제 몫을 하게, 채우기는 시리즈마다

- **Horizontal and vertical baselines have existed since v0.14** — but the direction picker sat *after* the x/y boxes in the add form, so nobody found it. Now you **pick the direction first**, the box that direction does not use is locked, and a one-line explanation follows.
- **Baselines can be named** (`Target 0.75`). Shaded spans had labels from day one; baselines did not, so a line's meaning was invisible on the chart.
- **One-sided shading**: above/below for a horizontal line, left/right for a vertical one. Shading used to exist only as crosshair quadrants, so "everything above this line passes" could not be drawn.
- **Shade color** is yours to pick (baselines and spans). Empty means automatic, and an `Auto` button puts it back.
- **Area fill is now per series.** Filling several series at once hides them behind each other, so usually one or two should be filled — empty follows the chart setting, and a series can also opt *out* while the chart fills. **Stacking stays chart-wide** (stacking only some series makes the "total" unreadable).

### v0.43 — put the one-click recipes up front, fold the duplicates into one row
> v0.43 — 누르면 되는 것을 앞으로, 같은 일은 한 줄로

- **Recipe chips**: the data card now shows `Try one of these: ▷ Average per item · ▷ Sweep trend · …`. The built-in presets shipped in v0.17 but lived **only in the `Presets` popover inside a chart card**, so you had to already have a chart to find them. Clicking one applies it to the **first chart**; no cards pile up.
- **Aggregation is one row.** The same verb sat in three different places (bar options, advanced point aggregate, heatmap aggregate). It is now `Data → Aggregate`, and the tool picks which field to write.
- **Error is one row** too: `none / <column> / std dev / std error`. Error only ever has one source, but it had three settings (`Error column`, `Error bars`, bar error bars).
- **Bug fix**: standard-deviation error bars and bands were also drawn for **median / min / max** aggregates. σ around a median is not that point's spread — it now draws for **mean only** (the stored setting is kept, just ignored while rendering).

### v0.42 — the settings you actually use, first
> v0.42 — 자주 쓰는 것만 먼저

- The settings panel opened with **46 rows**. With **`Essentials` (on by default)** it now shows **16** — 3,004 → 1,520px with every group expanded.
- It **hides, it does not remove**: ① **anything you have set stays visible** (hiding it would take away the only way to turn off a second axis or facet you enabled), ② **search still finds the hidden rows**, ③ `Show N more advanced settings` at the bottom opens them in one click. The choice is remembered by the browser and applies to every chart (same class as panel width and `One at a time`).
- The **11 chart types are grouped into three** — `Basic` (scatter, line, scatter+line, bar) / `Distribution` (histogram, box, violin, ECDF) / `Special` (heatmap, dumbbell, broken axis).
- **Axis tick format** (percent, thousands, scientific, fixed decimals) finally has a control. The feature shipped in v0.14 but **had no UI**, so it was reachable only by editing a session file.

### v0.41 — pick the color of dimmed points
> v0.41 — 흐리게 처리한 점의 색을 고릅니다

- Settings → Style now has **`Dimmed color`**: `Gray` (default, what it always did) or `Keep series color`.
- Dimming used to always **gray points out** — background context reads better when it drops series identity, so the highlighted side pops. But when dimming covers **several series**, you could no longer tell which faded points belonged to which series. Now you can keep the color.
- Either way the **opacity is unchanged** (0.28) — this is not a knob for how far back things recede.
- Pareto's `Fade dominated points` already kept the series color. Both kinds of fading now offer the same choice.

### v0.40.1 — collapsing did nothing while the settings were open
> v0.40.1 — 설정을 펼쳐 두면 접혀도 그대로였던 것

- **Bug fix**: collapsing hid **only the plot**, so a card with its settings panel open stayed exactly as tall (making `Collapse all` look broken). The **whole card body** now folds away, leaving one header line — 905px to 77px.
- A collapsed card shows its header summary even when the settings are open — with the body gone, that line is the only clue left.

### v0.40 — collapsing sticks, and works on all cards at once
> v0.40 — 접기가 남고, 한 번에 접힘

- **A collapsed chart stays collapsed after a refresh.** Card collapse used to be left out of the session, so reopening expanded everything — collapse is not transient state, it means "I am not looking at this chart", so it belongs in the session.
- New **`Collapse all` / `Expand all`** in the header (collapses everything if anything is open, expands everything if all are collapsed).
- A collapsed card also hides the `Drag = zoom…` hint line — there was nothing to operate on. The card goes from 105px to 77px.
- Presets do not carry the collapsed state — applying a preset should not fold your chart.

### v0.39 — what a collapsed card is showing
> v0.39 — 접어 둔 카드가 무슨 그림인지

- Collapse the settings and the card header now carries a **one-line summary** — `Scatter + line · tokens × accuracy · group method · filters 1`. No more reopening the panel just to see what the chart is.
- It hides while the panel is open (the same information is right below), follows every settings change, and follows the language.

### v0.38.1 — the search box was squeezed until its text was cut
> v0.38.1 — 검색칸이 눌려 잘리던 것

- The `One at a time` checkbox took room, so at the default width the search placeholder was **cut off**. The row now wraps instead of squeezing.
- The clipping check only ran at `Widest`, which is why it missed this — it now runs at the **default width** too.

### v0.38 — less scrolling in the settings panel
> v0.38 — 설정 스크롤 줄이기

- The panel was **capped at 640px**, so a tall window bought you nothing. It now **follows the window height** (640 → 850px in a 1000px window).
- **One group opens at a time** (turn it off with `One at a time` above the panel). Fully expanded the panel was 3,400px, so finding anything meant a long scroll.
- **The series list starts folded** — 437px of the Style group's 975px was that list, which is why Style never fit any window. It is 554px now, and the folded state is remembered.
- Together, the distance you must scroll went from **2,808px to 77px** (default width, 1000px window).
- Search still expands several groups at once — `One at a time` only reacts to an actual click.

### v0.37.1 — text clipped inside its own control
> v0.37.1 — 칸 안에서 잘리던 글자

- Fixed: the span `From` field cut its placeholder mid-character, the panel-width option `Widest` collided with the dropdown arrow, and the marker shape `triangle-up` was cut short.
- The box stays put and only the text is clipped, so the overflow check could not see it — the suite now measures text width against the room inside each control.

### v0.37 — settings panel width, and clipped labels
> v0.37 — 설정 패널 폭과 글자 잘림

- The settings panel width is now yours to pick — **`Narrow · Default · Wide · Widest`**, next to the search box. The choice is remembered by the browser, applies to **every chart at once**, and widens the label column with it.
- **Bug fix**: in tight rows, button labels **broke apart vertically** (`Pin to value`, `+ Add`, `+ Span`) and the shading select and `×` on a baseline row **overflowed the panel** and were cut off. Rows now wrap instead, and the baseline's name is no longer pushed out of view.
- Numeric inputs were too narrow for their placeholder text; widened too.

### v0.36.1 — detaching a baseline from its point
> v0.36.1 — 기준선을 점에서 떼기

- Baselines created by clicking a point now show a **`Pin to value`** button next to the `anchored to a point` badge — it freezes the line at the current value so it stays put when the data is refreshed. Until now the only way was to delete it and re-enter the number.
- The reverse is there too: a value-entered baseline gets **`Anchor to a point`** — press it, click a point, and the line follows that row.

### v0.36 — broken axis
> v0.36 — 축 끊기

- New chart type **`Broken axis`** — when values split into two far-apart groups (CPU 400 ms vs GPU 8 ms) the smaller group is pinned to the floor and its members cannot be told apart. The space between is folded away so **each group reads in its own range**.
- **Axis values stay real** — hover, the table, exported CSV and reports all report the unfolded numbers (folding the coordinates instead would make every one of them lie).
- The range is **automatic when left empty** (largest empty span, over 25% of the full range, at least two points on each side). If nothing is worth folding it draws as an ordinary chart **and says so**. You can enter a range yourself, or switch `Break` to the X axis.
- Baselines, text markers, the best-point label and shaded spans attach to **whichever panel holds their value** (a span crossing the break is drawn as two pieces).
- **Not available for bars** — a bar's length is the quantity, so breaking the axis makes the picture lie. For two different metrics, a secondary Y axis is the right tool.
- `More examples` now includes **`scales.csv`** (3 backends × 6 batch sizes) so guide recipe ⑲ can be followed as written.

### v0.35.1 — baselines vanished the moment they were created
> v0.35.1 — 기준선을 만들자마자 사라지던 것

- **Bug fix**: with two files holding the same values, or with a chart-level `Data` selection or filter, a baseline or marker made by clicking a point **disappeared immediately with "lost its anchor point"**. The anchor was looked up **across all rows instead of the rows actually drawn**, so it latched onto an identical row from another file or one removed by a filter. It now searches only the rows the chart draws.
- Anchors that were already broken are **restored when a point sits at exactly the stored coordinates**, so baselines and markers lost in earlier sessions come back. It never snaps to the nearest point — that would silently point at a different row, the very failure this machinery exists to prevent.

### v0.35 — baselines vanished when another file was loaded
> v0.35 — 파일을 더 넣으면 기준선이 사라지던 것

- **Bug fix**: loading one more data file made click-created **baselines and text markers immediately report "lost their anchor point" and disappear** (one press of `More examples` reproduces it).
- The columns that identify a row were picked from **all files merged together**. Once a second file arrived, a column that exists only in that file was empty in every other row and therefore looked like a low-cardinality condition column — so measurements like `f1` and `latency_ms` entered row identity and every stored anchor stopped matching.
- Identity is now decided **per file**: a row is identified by the schema of the file it came from, so other files coming and going cannot shift it. Re-attaching excluded/dimmed marks when the same file is reloaded is stable for the same reason.
- Anchors from older sessions still resolve — the old-style key is looked up as well.

### v0.34 — per-series display
> v0.34 — 시리즈마다 다른 표시

- Each series can now draw as **points only, line only, or points + line** independently within one chart
  (Settings → Style → Series; `Follow type` is the default). A reference curve as a line, raw data as points,
  the series you care about as points + line — until now the chart type drew every series the same way.
- Area fill, stacking, the secondary axis, the dimmed slice and small multiples all follow the per-series mode,
  so a series with no line never gets a fill band on its own.
- Old sessions open unchanged — an empty mode means "follow the chart type", exactly as before.

### v0.33 — a distribution recipe, companion data, and a dataset-scoping bug
> v0.33 — 분포 레시피와 짝 데이터, 그리고 데이터셋 선택 버그

- The guide gained **recipe ⑱, the spread of repeated runs** — the same data as box, violin and ECDF side by side, showing what a box hides.
- `More examples` now also loads **`seeds.csv`** (4 methods × 30 seeds). The basic example has only six values per method, too few to follow the recipe.
- **Bug fix**: distribution, heatmap and dumbbell charts **ignored the per-chart dataset selector** — they had done so since v0.19, silently mixing rows from other files into the picture. It surfaced while shooting the guide figures.

### v0.32.1 — violin and ECDF draw without an X axis
> v0.32.1 — 바이올린·ECDF가 X축 없이 그려지도록

- Distribution charts need only a value column, but the render guard exempted histogram and box **by name**, so the newly added violin and ECDF demanded an X axis and showed nothing until one was picked.

### v0.32 — distribution shape, series order, best point
> v0.32 — 분포 모양·시리즈 순서·최적점

- **Violin** and **ECDF** charts. A box plot shows quartiles only, so **bimodality and tails disappear** — which matters when comparing repeated seeds. An ECDF answers "what fraction is at or below this value" straight off the picture (drawn as steps — joining the points with straight lines would assign probability to values never observed).
- **Series order** is adjustable with ↑↓. Until now it followed the order values appeared in the data, so putting `baseline` first meant reordering CSV rows. **The colour does not follow** — a colour belongs to the series, not to the position.
- **Mark best** labels the highest or lowest point automatically. That was a manual click-and-annotate every time. Where Pareto describes the whole frontier, this points at one.

### v0.31.1 — version label and an internal name
> v0.31.1 — 버전 표시와 내부 이름 정리

- The image annotation page still reported `v0.30` (v0.31 bumped only the main page).
- The internal series name for an ungrouped chart was going through the translation function. No such key existed, so it was accidentally safe — but filling in that "missing key" would have made **series colours and labels vanish on every language switch**.

### v0.31 — example data for following the recipes
> v0.31 — 레시피를 바로 해 볼 예시 데이터

- The data card gained a **`More examples (join · melt · error)`** button. It loads three companion datasets (`methods.csv`, `wide.csv`, `repeat.csv`) so guide recipes ⑮ melt, ⑯ join and ⑰ error column can be followed **exactly as written**.
- Joining needs two files and melting needs a wide one, so a single bundled example could not demonstrate either.
- `example.csv` is **left untouched** — one more column there would shift the analysis golden tests and the documented description together.

### v0.30 — the guide catches up with the tool
> v0.30 — 가이드가 도구를 따라잡음

- **Three recipes added** to the visualisation guide: melting a wide CSV (⑮), attaching metadata from another file (⑯), and a figure that meets a submission spec (⑰).
- Existing recipes picked up the v0.26–v0.29 features: stacked area (④), chart as table (⑫), folder watching (⑬), plus an example of an annotated capture.
- Figures were shot **only for the new recipes.** Nothing in the palette, layout or plot face changed since r1–r10 were last captured, so re-shooting them would produce a diff and nothing else.

### v0.29.2 — drop-zone border and image replacement
> v0.29.2 — 드롭존 점선과 이미지 교체

- The **dashed border is dropped once an image is in**. "Drop here" has done its job by then and only adds noise; it returns while dragging so you still know the area accepts a file.
- **Loading a new image discards every annotation** — the one path with no undo — so it now asks first.
- (For reference: the blue dashed outline on the canvas is the **selection indicator**. It is on screen only and never lands in the export.)

### v0.29.1 — text backdrop on/off
> v0.29.1 — 글자 배경 켜고 끄기

- The white backdrop behind annotation text can now be **switched off** (`Text backdrop`) when it hides part of the picture.
- When on it is **fully opaque** — at 85% the lines and gridlines underneath showed through and muddied the text colour. A backdrop exists to make text readable, so it does not half-cover.
- Selecting a mark now **reflects its colour, width, font size and backdrop back into the inputs**.

### v0.29 — image annotation tool
> v0.29 — 이미지 주석 도구

- **There is now a page for labelling a capture** — `annotate.html`. Text, arrows, boxes, and a **redaction** block for covering sensitive values. Screenshots paste straight in.
- Coordinates are kept in original image pixels, so shrinking the view to fit your screen never shrinks **the exported file**, which comes out at full resolution (1x/2x).
- Language and theme are shared with the main page. The image never leaves the browser.
- **The file count went from 9 to 10.** This tool uses neither the chart library nor the data model, so folding it into the main page would only mix in unrelated code — the rule was relaxed once and locked again.

### v0.28 — baselines follow the data
> v0.28 — 기준선이 데이터를 따라갑니다

- **A baseline made by clicking a point is now anchored to that point (row).** It used to hold only coordinates, so reloading a file — or a folder-watch refresh — moved the point to its new value while **the baseline stayed at the old spot**, with nothing on screen to say so. Same failure that text markers had until v0.15.
- **Baselines typed in as values stay pinned to the value.** A line at exactly `0.80` means the value, not some row.
- **A baseline that loses its anchor is not drawn.** The list shows ⚠ with the reason (point is gone / axis changed) and a `Re-anchor` button. A misplaced baseline goes straight into a report, so being silently wrong is the worst outcome.
- Analysis speed was **measured and left alone** — see "Known limits" below for why.

### v0.27 — how data gets in, and out
> v0.27 — 데이터가 들어오고 나가는 길

- **Sideways CSVs are accepted now.** The input contract assumes long form (one row per measurement), so a file with `baseline, ours, ablation` as columns was **stopped at the door** — axes, groups and filters all assume one column means one thing. The `⇲` button on a dataset chip melts it into a new dataset, leaving the original alone.
- **Watch folder**: leave it on during a run and new results arrive by themselves. Reloading goes through the existing path, so **exclusions and fading you marked by hand are kept**. A file that briefly disappears (mid-write, mid-rename) is not removed from the screen — you didn't delete it, and there would be no way back.
- **Share as one HTML file**: a session JSON is only useful to someone who already has the tool. Exporting a single file with the data and settings baked in means the recipient just double-clicks. Build it from `index-offline.html` and it needs no internet either.

### v0.26 — figures you can actually submit
> v0.26 — 제출할 수 있는 그림

- **Export size is now yours to set.** Exports were the on-screen size at 3×, so hitting a paper or report spec meant fixing it up elsewhere. Presets cover **1-column (85mm), 2-column (170mm) and slides**, or set mm/inch plus dpi yourself.
- The hint reports **the pixels it will save and the pt size of body text**, making it obvious on the spot that raising dpi does not enlarge the text (raise the font size for that). Figures in the markdown report follow the same spec.
- **The error column can be named directly.** Error bars only appeared when aggregating, so data that already carried `score_std` had no way to draw it.
- **Span shading** arrived. A baseline is a line, so it could never say "this range" — recommended bands, out-of-memory regions and the like now have a form.
- **Stacked area** works on line charts. Only bars could stack, so a share-over-time chart was out of reach. Stacking draws with SVG instead of WebGL (WebGL has no stacking and would silently overlay instead).
- **Charts can be shown as a table.** It is the only way to read a chart without seeing it, and it is where you check an exact value.

### v0.25 — joining across files
> v0.25 — 파일 간 결합

- **Values from another file can be looked up by key.** Computed columns gained the kind `Look up from another file` — keep `runs.csv` (measurements) and `models.csv` (metadata such as parameters and price) separate and still use both in one chart. Until now merging files only stacked rows, so this shape was out of reach.
- **Rows are never multiplied.** Only a column is attached — growing the row set would break the notion of "the same row" that exclusions, fading, point labels and text-marker anchors all rely on. Several matches fold via first/mean/sum/min/max/count.
- **No silently empty column**: only columns present in both files are offered as keys, and picking one immediately counts how many rows will find a match. Unmatched rows get a blank, not a zero.
- Computed columns defined earlier can serve as the key — build a composite one with `Label join` and match on two columns at once (definition order is evaluation order).
- **Bug fix**: computed columns were leaking into how "the same row" is recognised, so re-loading the same file while a computed column existed **wiped every exclusion and fade you had marked by hand**. Computed columns are regenerated from the data, so they are now excluded from that identity.

### v0.24 — reachable by keyboard, a less crowded panel
> v0.24 — 키보드로 닿게, 패널은 덜 빽빽하게

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
> v0.23 — 하위 폴더 자동 로드와 실행기 정리

- **Autoload now reaches into subfolders.** Split your results across `results/a/run1.csv` and they all load at once, listed as relative paths.
- **Hidden folders (`.git`, `.venv`, `.ipynb_checkpoints`, …) and symlinks pointing outside the folder are skipped** — tool config files have no business being read as data, and following links either escapes the folder or loops forever. The list stops at 500 files.
- **The outside-the-folder guard now catches symlinks too**: paths are resolved to their real location before the check.
- `--host` picks the bind address (still `127.0.0.1` by default). Binding to **`0.0.0.0` lets anyone on your network read that folder**, so it now prints a warning at startup.
- Requests are served on threads, so reading a large file no longer freezes the page. The offline build gives up after 15 seconds with a reason when the CDN doesn't answer.
- Internal: the all-rows list is memoised, cutting repeated scans while building config panels.

### v0.22 — half-width cards and the figures in the docs
> v0.22 — 절반 폭 카드와 문서 그림 정리

- **Fixed the header buttons folding in half-width cards.** `Reset view` broke into two lines that spilled out of the button box. The buttons now keep their width and the header gains a second row when space runs out.
- **All 14 figures in the docs were re-shot.** Twelve commits had changed the UI since v0.16 while the images stood still — the Pareto figure in particular still showed the grey dashed frontier, contradicting the text beside it.

### v0.21.2 — and its colour
> v0.21.2 — 프런티어 선 색까지

- The frontier line's **colour** is selectable too. **Left blank it follows the theme** as before (light/dark automatically); set it and it stays that colour.
- Once a colour is set, an `Auto` button appears next to it to go back to the theme — a colour input cannot hold an empty value, so the way back needs its own control.
- **If you use both themes, leaving it blank is the better default:** a fixed colour stays fixed in dark mode and may lose contrast on one of them.

### v0.21.1 — choosing the frontier line style
> v0.21.1 — 프런티어 선 모양 선택

- The frontier line's **style (solid / dashed / dotted / dash-dot) and width** are now selectable (Advanced → Pareto). The default stays solid at width 2.
- On `Scatter + line` charts the series lines are solid too, so switching the frontier back to dashed keeps them apart.
- **The colour is deliberately not exposed.** The frontier is a verdict about all the points, not about one series, so a series colour would read as that group's line. It stays theme ink and follows light/dark only.

### v0.21 — a readable Pareto chart
> v0.21 — 파레토를 읽을 수 있게

- **The frontier is now a solid ink line instead of a grey dashed one.** It shared a tone with the baselines and sank into the background, and you could not tell which points it touched. Now the points it touches read as the candidates.
- **`Fade dominated points`** is a new option (Advanced → under Pareto). With it on, only the points on the frontier stay solid and the rest recede. Faded points keep their series color, so group identity is still readable.
- A faded legend swatch means that series **put nothing on the frontier** — a method that is dominated everywhere is visible at a glance.
- The frontier is computed **over all points regardless of group** (as it always was): the points it touches are the configurations worth choosing.

### v0.20.1 — Pareto re-checked
> v0.20.1 — 파레토 재점검

- **With point aggregation on, the frontier was drawn in the wrong place.** The visible points were means while the frontier came from the raw rows, so the dashed line passed through none of them. It now follows **the points actually drawn**.
- **Dimmed rows no longer define the frontier** — the same reason trend lines already skip them: a point pushed into the background should not set the boundary.
- **Not drawn in facet mode.** A frontier computed over all the data used to sit on the first panel only, inviting a wrong reading of the others (same treatment as baselines, markers and labels).
- The legend said `Pareto frontier` even in Korean; it now follows the language.
- The frontier computation itself (all four directions) was checked against an independent implementation and is **correct**.

### v0.20 — filters say what they are doing
> v0.20 — 필터가 무엇을 하는지 말해 줍니다

- Each filter now shows **how many rows it currently matches**, in words — `6 of 24 rows match — the other 18 are dropped` — and the count follows along while you type the value.
- **You pick which side is affected.** There are now four modes — `Drop others` (default) · `Drop matching` · `Dim others` · `Dim matching`. `method = baseline` + `Dim matching` fades baseline; `Dim others` does the opposite. Previously only one direction existed, which was easy to read backwards.
- The names state the target, and the sentence confirms it with live row counts — a wrong pick shows up in the numbers first.
- The cramped filter row is fixed too: the controls have minimum widths and wrap onto a second line when the panel is narrow.

### v0.19 — looking at files separately
> v0.19 — 파일별로 따로 보기

- With two or more files loaded, every chart gets a **`Data` dropdown** choosing which one it draws. Only that file's rows are used, and **the column lists narrow to that file** — no more picking a column the selected file does not have.
- Since it is per chart, **two unrelated datasets can sit side by side** on one page. `(all)` goes back to the merged view.
- Switching files **clears the axis/group/filter settings that no longer apply** and says which ones. Deleting the file a chart points at returns it to `(all)` with the same cleanup.
- Splitting by file was already possible via the `_source` column (as a facet, group or filter). This is a shortcut on top of that — for overlaying files in one chart, facet by `_source` is still the way.

### v0.18 — one column for a combination of conditions
> v0.18 — 조건 조합을 한 컬럼으로

- Computed columns gained a **`Label join`** kind: rather than computing a value it joins values from several columns into a text column — `selector` + `frames` → `sal-v3.1 · 16frm`.
- Each part takes **text before and after** (`16` → `16frm`), the parts are joined by a **separator** you choose, and you can add as many parts as you need.
- Because the result is text it drops straight into **group (color), facet, filter and the bar X axis**, so "one row per condition combination" is a couple of clicks away.
- Parts with no value are skipped, so you never get a lone separator; if every part is empty the row has no value.

### v0.17.1 — right even when the names mean nothing
> v0.17.1 — 이름을 몰라도 맞도록

- Role matching for the built-in presets moved **from name patterns to value distribution**, reusing the same column classification the analysis engine uses: categories, sweep knobs, continuous measures and identifiers are told apart by their values, and names only decide which of two continuous columns is the score and which is the cost.
- So data named `zeta` and `kv` gets sensible axes, and a `seed_id` never ends up on one.
- The trade-off preset now prefers a continuous column (latency and such) over a sweep knob for X — using the knob just reproduces the sweep preset.

### v0.17 — something to click on first open
> v0.17 — 처음 열었을 때 누를 것

- The card's `Preset` button now offers **five built-ins** (average per item, sweep trend, trade-off, two-condition grid, value distribution), so an empty preset list is no longer a dead end.
- They hard-code no column names: **roles are matched against the current data** — a categorical column, a sweep knob with few distinct values, a score-like and a cost-like numeric. A recipe whose roles cannot be filled is never listed, so clicking one never yields a blank chart.
- A log X axis is switched on only for genuinely multiplicative sweeps (judged by max/min ratio).
- Fixed alongside: **histograms and box plots refused to draw without an X column**, though they need only the one value column.

### v0.16.1 — where presets and hiding collided
> v0.16.1 — 프리셋과 숨김이 부딪히던 곳

- Applying a preset that uses a hidden column now **unhides that column**. No more half-state where the chart draws but the axis picker cannot offer the column again — the same treatment the preset's computed columns already got.
- Fixed: a preset did not carry the computed column used on its **secondary Y axis**, so that axis came up empty for whoever received it.
- What a preset application did on the side (restoring computed columns, unhiding) now rides **in the same notice**. Previously the toast was overwritten immediately and never seen.

### v0.16 — holding up when there are many columns
> v0.16 — 컬럼이 많아도 견디게

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
> v0.15 — 주석이 데이터를 따라갑니다

**Text markers are anchored to their point**
- Creating a marker now stores the **identity of the point you clicked** (its condition columns — method, tokens, …) alongside the coordinates, and every render re-reads that row's current values. Refresh the data and the callout still points at the same point. Markers from older sessions keep their coordinate behaviour.
**Nothing drifts silently**
- If the anchor row disappears (filter, exclusion, replaced data) or the axis column changes so the coordinates no longer mean anything, the marker is **not drawn**, and a toast says so. A misplaced annotation goes straight into a report, so vanishing beats sitting in the wrong spot.
- The Settings → Point labels list keeps it with a ⚠ and the reason (`axis changed` / `point is gone`); hit `Re-anchor` and click a point to attach it somewhere new.
**Notes that belong to no point**
- `＋ Pinned note` adds a note fixed to the plot area (`n=24 · measured 2026-07`, measurement conditions, provenance). It survives any data change or axis switch, and drags anywhere.

### v0.14 — refresh, distributions, second axis, safety
> v0.14 — 갱신·분포·보조축·정리

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
> v0.13.1 — 계산 컬럼 삭제

- Deleting a computed column now **lists the charts and other computed columns that use it and asks first** — the action cannot be undone.
- On delete the affected charts' axis and filter settings are **cleared too**, and a toast says what was cleared. Previously those settings kept pointing at a column that no longer existed: the chart went blank while its settings panel showed "(pick one)".
- Columns nothing depends on are still deleted straight away, without a prompt.

### v0.13 — speed
> v0.13 — 속도

Measured the slow paths on large data and fixed them (numbers at 20k rows).
- **Charts using a size column: 49.5s → 0.43s.** The size range was recomputed for every single point; it is now computed once per render (at 50k rows the chart effectively never appeared).
- **Opening a settings panel: 57ms → 2ms** — the column list, numeric detection and unique values are recomputed only when the data changes.
- **Automatic WebGL**: above 5,000 points charts render with WebGL (a 30k-point scatter goes from 949ms to 18ms of render time). Pin `High quality (SVG)` in Settings → Style → Rendering if you prefer, and **SVG export temporarily switches back to vector**, so figures for papers keep their quality.

### v0.12.1 — review fixes
> v0.12.1 — 리뷰 수정

- **Captions were silently lost**: reopening the settings panel showed an empty caption box, and typing one character there replaced the whole caption.
- **Analysis**: the trivial correlation between a computed column and its source (e.g. `accuracy` and its z-score) is no longer reported as a finding.
- **Analysis**: two-valued conditions (an A/B flag like `fp16` on/off) are now group-comparison candidates; they used to be dropped silently, producing no findings at all.
- **Analysis**: curves that rise and then fall back are no longer reported as "saturation" with a share above 100%.
- **Analysis**: the outlier list keeps the most extreme cases instead of whichever was scanned first.
- Also fixed: console errors when resizing with a collapsed chart, a possible id collision when undoing a chart deletion, and a failed chart image aborting the rest of a report export.

### v0.12 — usability, reports, computed columns
> v0.12 — 사용성 · 보고서 · 계산 컬럼

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
> v0.11.1 — 분석 정합성 수정

- Excluding or restoring rows in the table now **marks the analysis stale immediately** (previously the panel kept showing insights computed before the exclusion).
- When a folder is served by `visualizer.py`, **files that changed are re-read** instead of being skipped, so updated logs actually show up.
- Autosave failures caused by storage limits are reported instead of being swallowed.
- Dropping back to a single dataset clears axis/group/filter settings that referenced `_source`.
- Analysis: **when there is more than one design value (condition), pairing now happens on the combination** rather than the first one only. Design values that map one-to-one collapse into one representative, and the group-candidate limit is raised to 24 so comparisons across ~20 models still work.
- The panel now shows a **scan-scope line** (group candidates, design values, excluded columns and why), so an empty result explains itself.

### v0.11 — automatic analysis panel
> v0.11 — 자동 분석 패널

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
> v0.10 — 히트맵·덤벨 차트

- **Heatmap**: a grid over two discrete axes colored by a value (e.g. X=frames, Y=gazing_ratio, color=accuracy) — a 2D sweep at a glance.
- **Dumbbell (paired)**: two conditions per category (e.g. pretrained/tuned) as dots joined by a line — the difference reads directly.

### v0.9 — page width
> v0.9 — 페이지 폭

- A **width toggle** in the top bar (Normal 1280px / Wide 1660px / Full = fill the screen). Shrinks side margins on wide monitors for bigger charts. Remembered.

### v0.8 — dark mode
> v0.8 — 다크 모드

- **Light/dark theme** toggle (top-right 🌙/☀️). Follows the OS setting on first run; your choice is then remembered. Chart surface, axes and palette are tuned for dark (not a naive invert).

### v0.7 — chart size & layout
> v0.7 — 차트 크기·배치

- **Per-chart height slider** (280–820px) and **full / half width**. Set two charts to half width to place them side by side, like a mini dashboard.

### v0.6.1 — bug fix
> v0.6.1 — 버그 수정

- Adding/removing a computed column now **updates the axis/group dropdowns of open chart settings immediately** (previously you had to reopen the panel).

### v0.6 — dim filters
> v0.6 — 흐리게 필터

- **"Dim" filter mode**: instead of removing non-matching rows, fade them into the background → rule-based highlight (focus + context). Automates what used to be per-point de-emphasis.

### v0.5 — small multiples & computed columns
> v0.5 — 다중 차트·계산 컬럼

- **Facet (small multiples)**: split into a grid by column value — small multiples without repeated duplicate+filter.
- **Computed columns**: derive columns in-tool (binary ops, delta/retention vs a reference); source file untouched, saved in the session.

### v0.4 — analysis & reporting
> v0.4 — 분석·보고 기능

- **Continuous color**: color by a numeric column as a gradient (colorbar).
- **Point aggregate · error bars · band**: summarize repeated measurements at the same X by mean, etc. (line/scatter).
- **Focus / de-emphasize (focus + context)**: fade points into the background instead of excluding them, to spotlight what matters.
- **Export**: all charts as one PNG; current filtered data as CSV.

### v0.3 — legend improvements
> v0.3 — 범례 개선

- Legend placement inside the chart by **corner** (top-left/top-right/bottom-left/bottom-right).
- **Editable legend names** (display only; internal identifiers unchanged).

### v0.2 — bar charts, guide, presets
> v0.2 — 막대 차트·가이드·프리셋

- **Bar charts**: grouped/stacked, horizontal, aggregation (mean, etc.), error bars, value labels, sorting.
- **Visualization guide** (GUIDE.md/en) with example captures.
- **Chart presets**: save chart settings only → re-apply to new data.
- Baseline direction (crosshair/h/v), log-axis baseline placement fix, numeric multi-select filters, session-file-as-data guard, version badge.

### v0.1 — initial release
> v0.1 — 초기 릴리스

- Scatter/line/scatter+line, log axes, axis ranges, series styling, filters, baselines (quadrant shading), text markers, point labels, trendlines & error bands, Pareto, shape group, area fill, sessions, PNG/SVG, KO/EN, offline build, English docs.

---

© mrc
