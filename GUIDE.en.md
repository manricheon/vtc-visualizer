# VTC Visualizer — Visualization Guide

**English** | [한국어](GUIDE.md)

The feature list and controls live in [README.en.md](README.en.md). This document answers the next question:
**"Which chart, with which settings, will actually get my point across?"**
Every example can be followed along with the bundled `example.csv` (4 methods × 6 token-budget sweep).
UI labels below assume the EN toggle (top-right corner).

## 0. Start from the question, not the data

A good chart is not "a picture of all the data I have" — it is **an answer to one question**.
Before building a chart, write the question as a sentence: *"Is ensemble worth its extra cost over baseline?"*,
*"Where do gains saturate as we raise the budget?"* Once the question is fixed, the chart type almost picks itself.

## 1. Choosing a chart

Two criteria drive the choice: **the kind of question**, and **whether X is a continuous quantity (numbers) or discrete items (names)**.

| Question | Data shape | Chart | Options that pair well |
|---|---|---|---|
| "How does it **change**?" (trend, saturation, crossover) | X = continuous (tokens, steps, time) | **Line** or **Scatter + Line** | Trendline, error band (±1σ), log scale |
| "Who is **bigger**?" (magnitude, ranking) | X = item names (method, model) | **Bar** + aggregate | Sort (value descending), value labels, error bars |
| "Which combination **wins**?" (trade-off) | two continuous measures (speed vs accuracy) | **Scatter** | Pareto frontier, baseline + quadrant shading |
| "What is it **made of**?" (breakdown, contribution) | parts that sum meaningfully (cost, time) | **Bar → Stacked** | X as categories |
| "How **reliable** is it?" (repeated-measure spread) | multiple rows per condition (per seed) | **Bar** + aggregate = Mean | Error bars (±std dev/±std error) |
| X is numeric but only **a few settings** (budget 500/1k/…/16k) | discrete numbers | **Line** to stress the trend, **Bar** to stress the gaps | with bars, check "X as categories" |
| **6+ items** or long names | long category list | **Bar → Orientation = Horizontal** | sort to make it a ranking |
| "Which **combination** is good?" (a whole 2D sweep) | two discrete axes + one value (method × budget → accuracy) | **Heatmap** | show cell values, aggregate = Mean |
| "How much does A→B **shift things**?" (paired comparison) | two conditions per item (before/after, 500 vs 16k) | **Dumbbell (paired)** | filter down to the two conditions |

One-line summary: **change → line, magnitude → bar, trade-off → scatter.**

### What to avoid (anti-patterns)

- **Don't stack measures whose sum is meaningless** — a stack of four accuracies "totaling 2.7" says nothing. Stack only quantities where parts genuinely add up (cost, time).
- **Don't put 8+ series in one chart** — colors stop being distinguishable. Filter down to what matters, or `Duplicate` the chart and split by condition (small multiples).
- **Don't label every point** — when everything is highlighted, nothing is. Reserve text markers for the protagonist (the peak, the crossover, your method).
- **Log scale only when "how many times" is the question** — great for axes spanning orders of magnitude, but it hides small absolute differences.
- **Bar value axes start at 0** — bars are read by length, so truncating the axis exaggerates differences (bars already do this by default). Lines/scatter care about change, so zooming to the data range is fine there.

## 2. Recipes by scenario

Recipes use the UI labels verbatim. `Settings → …` refers to each chart card's `⚙ Settings` panel.

### ① Mean performance per method — "Which method is best?"

> Type=`Bar`, X axis=`method`, Y axis=`accuracy`, Group (color)=`method`
> Bar options → Aggregate=`Mean`, Error bars=`±std dev`, Value labels=`Value at bar end`, Sort=`Value descending`

![Mean accuracy per method — error bars, value labels, sorted descending](assets/guide/r1-bar-mean.png)

Each method's six budget measurements collapse into one mean, and the whiskers (error bars) show how much the budget swings it.
**How to read it**: overlapping error bars signal "this ranking could flip under other conditions."
For seed-repeated experiments, `±std error` is the better choice — it shows confidence in the mean itself.

### ② Budget-sweep trend — "Where do gains saturate?"

> Type=`Scatter + Line`, X axis=`tokens`, Y axis=`accuracy`, Group (color)=`method`
> Axes → X scale=`Log` · Advanced → Trendline=`Log (a+b·ln x)`, Error band=`±1σ shading`

![Budget sweep on a log X axis — per-series log trendlines with ±1σ bands](assets/guide/r2-trend.png)

A doubling sweep becomes evenly spaced on a log X axis, straightening the trend.
**How to read it**: the point where the curve flattens is where extra spend stops paying — drop a text marker there and the message is complete.

### ③ Speed–accuracy trade-off — "Is the latency worth it?"

> Type=`Scatter`, X axis=`latency_ms`, Y axis=`accuracy`, Group (color)=`method`
> Advanced → check Pareto, Direction=`Lower X · Higher Y is better`
> **Click** your reference point (e.g. baseline's production setting) → `📍 Add baseline` → in the settings baseline list, shading=`Upper left`

![Latency–accuracy scatter — Pareto staircase and upper-left baseline shading](assets/guide/r3-pareto.png)

Only points on the Pareto staircase are rational choices; everything else is dominated.
Points inside the baseline shading (upper-left = faster **and** more accurate) are the settings worth switching to.

### ④ Cost breakdown — "Who contributes what to total cost per budget?"

> Type=`Bar`, X axis=`tokens`, Y axis=`cost_usd`, Group (color)=`method`
> Bar options → Layout=`Stacked`, check `X as categories`

![Stacked cost per budget — evenly spaced thanks to X as categories](assets/guide/r4-stack.png)

Total bar height = the sum; each color band = one method's share. `X as categories` is what makes
500–16000 render as evenly spaced bars (unchecked, they sit at their true numeric positions and the left bars get needle-thin).

### ⑤ Ranking chart — "Throughput order at a glance"

> Type=`Bar`, X axis=`method`, Y axis=`throughput_fps`, Group (color)=`method`
> Bar options → Orientation=`Horizontal`, Aggregate=`Mean`, Sort=`Value ascending`, Value labels=`Value at bar end`

![Horizontal throughput ranking — value ascending puts first place on top](assets/guide/r5-ranking.png)

Horizontal bars keep long or numerous item names readable, and with sorting they read like a leaderboard.
(Use `Value ascending` so first place ends up on top.)

### ⑥ Seeing a third dimension — "Keep color=method, but also show frames"

With X=tokens, Y=accuracy, Group (color)=method:

1. **Shape group**=`frames` — color stays method, marker shape encodes frames (recommended; legend shows each combo)
2. **Size column**=`frames` — bigger markers for bigger values (good for continuous values)
3. **Continuous color**=`frames` — a light→dark gradient by value, with a colorbar. **Note: clear Group (color) to "(None)" first** — it can't run alongside group color. Best for a continuous numeric third dimension (not a few categories)
4. **Point labels** with Label column=`frames` — the value appears next to each point
5. **Facet**=`frames` — Settings → Data → Facet: a small chart per frames value, auto-arranged in a grid (no more repeated duplicate+filter)

When the secondary group has many unique values (e.g. 6 frames values → 24 combos) the legend explodes — **filter down to 2–3 contrasting values** before using the shape group:

![Color=method, shape=frames (filtered to 8·64) — shape separates the budget tiers](assets/guide/r6-shape-group.png)

### ⑦ Presentation polish — turning a chart into "the slide"

- **Let the title state the conclusion**: Style → Title = "Ensemble overtakes baseline from 8k tokens", not "Accuracy vs Tokens" — the axis labels already say that.
- **Click** the key point → `💬 Add text marker` for an annotation (drag to position; style it in the Point labels group)
- Style → Font size 15–16 (back-of-the-room test); with 2–3 series move the legend to `Inside chart` to save space
- Export with `PNG` (3× resolution, for slides) or `SVG` (papers, vector editing)

![A presentation-ready chart — the title states the conclusion and a text marker points at the saturation point](assets/guide/r7-presentation.png)

### ⑧ Build "vs reference" values in the tool — computed columns

Want to see how each setting does **against a reference** (e.g. accuracy difference vs baseline/dense) but the data has no such column? You don't need to regenerate the data — make it on the spot with **computed columns** (the "Computed columns" panel below the data input):

- **Binary op**: new column = A [−, +, ×, ÷] B, or against a **constant** (e.g. `used_tokens ÷ input_tokens` = actual usage ratio, `latency_ms ÷ 1000` = seconds). Which unit reads better depends on the data and the audience — this only adds a column, so you can keep both and pick per chart.
- **Normalize / z-score**: compare metrics on different scales in one chart (0–1, % of max, z-score), optionally **within each group** — "how good is this relative to its own method"
- **Rank**: position inside a group (e.g. the ranking of methods at each budget)
- **Bin**: cut a continuous column into N bins; the labels are strings, so they work directly as groups, filters or colors
- **Group aggregate**: attach a group's mean/sum to every row; combined with the reference delta this gives "how far is this row from its group average"
- **Delta vs reference**: **difference** or **retention %** vs the reference row with the same match keys (e.g. value=`accuracy`, reference = rows where `method`=`baseline`, match=`tokens` → "how many pt above baseline at the same tokens")

A computed column can feed another one (use `↑`/`↓` in the list to fix the **calculation order**), and `✎` edits a definition.
Deleting one with `×` first tells you which charts use it, and clears their axis and filter settings along with it.
The new column doesn't change your source file, is saved in the session, and is usable immediately as an axis/filter. Presets carry the definitions they need, so teammates get them too. If you don't need it, just collapse the panel — no effect on the view.

### ⑨ A whole 2D sweep in one picture — heatmap

> Type=`Heatmap`, X axis=`method`, Y axis=`tokens`, Color value (column)=`accuracy`, Aggregate=`Mean`, check `Show cell value`

![Heatmap of the method × token-budget grid, encoded as colour](assets/guide/r8-heatmap.png)

This puts **every combination** of two discrete axes on one canvas. It shines when four overlapping lines become unreadable, or when
you want to expose which cells were never measured. **How to read it**: the point where the colour stops deepening is the point where
more budget stops buying anything. Colour only conveys magnitude, so it is **poor for fine comparisons** — use bars when the exact ranking matters.

### ⑩ The gap between two conditions — dumbbell (paired)

> Type=`Dumbbell (paired)`, Category (X)=`method`, Value (Y)=`accuracy`, Pair group=`tokens`
> Filters → check only `500` and `16000` under `tokens` (dumbbells read best with exactly two conditions)

![Dumbbell chart showing each method's accuracy moving from 500 to 16000 tokens](assets/guide/r9-dumbbell.png)

Instead of two bars side by side, this draws **two dots and a connecting line**, so "how much was gained" is read directly as line length.
**How to read it**: longer line = bigger effect of that condition change. Unlike bars, you see both the starting level and the size of the move.

### ⑪ When you do not know where to start — the `Analyze` button

Just received a dataset and unsure what to plot first? Press `Analyze` in the header. The tool scans the data and reports
**data problems → interpretation cautions → findings**, and each row's `＋ Chart` builds the chart that backs it up.

![The automatic analysis panel — findings tagged Data/Caution/Finding, plus the column profile table](assets/guide/r10-analysis.png)

- **Data** (grey) — constant or empty columns, non-numeric values mixed into numbers (a single `OOM` drops the whole column out of the
  axis candidates), duplicate rows, missing values concentrated in one group, combinations that were never measured. **Fix these first**;
  everything below depends on them.
- **Caution** (red) — relationships that reverse when pooled (Simpson's paradox) and crossovers where the winner changes with the condition.
  These are what stop you from writing a wrong one-line summary.
- **Finding** (grey) — correlations, group differences, saturation points, outliers.

Each tier carries a one-line note on how to check it. The order of how objectively verifiable they are is **Data → Caution → Finding**: data items are counts you can confirm in the table, caution items report a disagreement between two computations that one chart can refute, and findings involve threshold judgements, so they come last. That is why each finding prints **its chart recipe (type · X · Y · group) in grey**, and `＋ Chart` opens exactly that chart — if one with the same setup is already open, the button becomes `Go to chart` and jumps there instead of duplicating it.

#### How to read the findings (and what not to claim)

- **Correlation is not causation.** "A and B move together" does not mean A produces B. Do not convert these into causal claims in a paper or report.
- **Handle "Caution" items before the findings below them.** If the pooled correlation is −0.23 while every method is +0.8 internally,
  the per-method number is the one to report — the pooled figure flipped only because the methods sit at different levels.
- **When a crossover is reported, do not summarise it as one mean.** "A beats B by +0.2pp on average" may only hold below budget 4000.
- **p-values are deliberately absent.** Benchmark rows are not independent (a budget sweep for one method is a connected series) and the
  number of repeats is arbitrary, so significance tests read more generously than the data supports. Instead you get the **raw difference plus
  direction consistency across conditions** (e.g. "6 of 6 conditions agree") — a more useful signal for whether a finding will reproduce.
  Group differences also carry a **bootstrap interval (95%)**: how much the difference would move had the measured conditions been drawn
  again. Findings whose interval spans zero are not reported at all. Read it as spread, not as a significance verdict — "difference 103,
  interval 28 to 198" means the direction is clear but the size depends heavily on the condition, while "difference 10, interval 9.98 to
  10.02" means it barely varies at all.
- **Outliers are flagged, never removed.** They may be measurement errors or real behaviour, so inspect the value and exclude it yourself
  with the table checkbox if you decide to.
- **Finding nothing is also a result.** It means nothing cleared the thresholds, and relationships dug up by lowering them rarely reproduce.

The analysis runs on **the rows still in the table** (rows excluded from charts are left out) and is discarded whenever the data changes. It is never stored in the session.
If nothing at all is reported, read the **scan scope** line at the top of the panel: it lists which columns were treated as groups and conditions and what was excluded and why, which tells you whether the relationships were weak or there were simply no conditions to compare.

### ⑫ Exporting a report — figures with their sentences

Once the charts are polished, write one or two sentences into Settings → Style → **Caption** for each ("what this figure says") and press `Report MD`.
You get one markdown file plus the chart PNGs; every chart section carries its **caption, setup and the filters in effect**, and if the analysis has been run, its findings summary and caveat are appended.

**Why the filter conditions must travel with the figure**: a conclusion that only holds for tokens ≤ 4000, screenshotted with the filter on and pasted without stating it, will be read as a conclusion about the whole dataset. The report writes that condition down for you.
When moving findings into prose, do not convert them into causal claims (see "How to read the findings" in ⑪) and keep only what you need.

## 3. Principles for effective charts (summary)

1. **One chart, one message** — want to say two things? Duplicate into two charts.
2. **Emphasis only works when it's scarce** — labels, markers, shading go on the protagonist only.
3. **Color follows the entity** — the same method keeps the same color across every chart. The tool enforces this automatically (filters don't repaint survivors); keep the principle when overriding series colors by hand.
4. **Put the reference in the picture** — "better/worse" only means something against a baseline. Click your reference point and pin it as dotted lines.
5. **Don't hide uncertainty** — if you have repeated measurements, turning on error bars/bands is what makes the chart honest.
6. **Units live in axis labels** — the column-name convention (`latency_ms`, `cost_usd`) shows up on the axes as-is; refine via Axes → X/Y label when ambiguous.

## 4. Sharing with your team

- **Share charts with their settings**: `Export session` (top bar) → one JSON file holds the data and every chart's configuration. The recipient restores the exact screen with `Import session`.
- **Presets vs sessions**: a session = data + charts; a **preset = chart settings only** (the `Presets` button on each card). When the data changes but the schema stays the same — weekly experiment logs, say — a saved preset redraws the same chart on new data in one click.
- **Converting data**: whatever your format, paste the [agent prompt](README.en.md#converting-your-data-to-this-format-agent-prompt) from the README into any LLM together with your file.
- **Offline distribution**: copying the single `index-offline.html` file is enough — it works identically with no internet.

---

© mrc
