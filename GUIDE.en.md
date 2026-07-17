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

Each method's six budget measurements collapse into one mean, and the whiskers (error bars) show how much the budget swings it.
**How to read it**: overlapping error bars signal "this ranking could flip under other conditions."
For seed-repeated experiments, `±std error` is the better choice — it shows confidence in the mean itself.

### ② Budget-sweep trend — "Where do gains saturate?"

> Type=`Scatter + Line`, X axis=`tokens`, Y axis=`accuracy`, Group (color)=`method`
> Axes → X scale=`Log` · Advanced → Trendline=`Log (a+b·ln x)`, Error band=`±1σ shading`

A doubling sweep becomes evenly spaced on a log X axis, straightening the trend.
**How to read it**: the point where the curve flattens is where extra spend stops paying — drop a text marker there and the message is complete.

### ③ Speed–accuracy trade-off — "Is the latency worth it?"

> Type=`Scatter`, X axis=`latency_ms`, Y axis=`accuracy`, Group (color)=`method`
> Advanced → check Pareto, Direction=`Lower X · Higher Y is better`
> **Click** your reference point (e.g. baseline's production setting) → `📍 Add baseline` → in the settings baseline list, shading=`Upper left`

Only points on the Pareto staircase are rational choices; everything else is dominated.
Points inside the baseline shading (upper-left = faster **and** more accurate) are the settings worth switching to.

### ④ Cost breakdown — "Who contributes what to total cost per budget?"

> Type=`Bar`, X axis=`tokens`, Y axis=`cost_usd`, Group (color)=`method`
> Bar options → Layout=`Stacked`, check `X as categories`

Total bar height = the sum; each color band = one method's share. `X as categories` is what makes
500–16000 render as evenly spaced bars (unchecked, they sit at their true numeric positions and the left bars get needle-thin).

### ⑤ Ranking chart — "Throughput order at a glance"

> Type=`Bar`, X axis=`method`, Y axis=`throughput_fps`, Group (color)=`method`
> Bar options → Orientation=`Horizontal`, Aggregate=`Mean`, Sort=`Value ascending`, Value labels=`Value at bar end`

Horizontal bars keep long or numerous item names readable, and with sorting they read like a leaderboard.
(Use `Value ascending` so first place ends up on top.)

### ⑥ Seeing a third dimension — "Keep color=method, but also show frames"

With X=tokens, Y=accuracy, Group (color)=method:

1. **Shape group**=`frames` — color stays method, marker shape encodes frames (recommended; legend shows each combo)
2. **Size column**=`frames` — bigger markers for bigger values (good for continuous values)
3. **Point labels** with Label column=`frames` — the value appears next to each point
4. `Duplicate` the chart and filter each copy to one frames value — side-by-side small multiples (best once series multiply)

### ⑦ Presentation polish — turning a chart into "the slide"

- **Let the title state the conclusion**: Style → Title = "Ensemble overtakes baseline from 8k tokens", not "Accuracy vs Tokens" — the axis labels already say that.
- **Click** the key point → `💬 Add text marker` for an annotation (drag to position; style it in the Point labels group)
- Style → Font size 15–16 (back-of-the-room test); with 2–3 series move the legend to `Inside chart` to save space
- Export with `PNG` (3× resolution, for slides) or `SVG` (papers, vector editing)

## 3. Principles for effective charts (summary)

1. **One chart, one message** — want to say two things? Duplicate into two charts.
2. **Emphasis only works when it's scarce** — labels, markers, shading go on the protagonist only.
3. **Color follows the entity** — the same method keeps the same color across every chart. The tool enforces this automatically (filters don't repaint survivors); keep the principle when overriding series colors by hand.
4. **Put the reference in the picture** — "better/worse" only means something against a baseline. Click your reference point and pin it as dotted lines.
5. **Don't hide uncertainty** — if you have repeated measurements, turning on error bars/bands is what makes the chart honest.
6. **Units live in axis labels** — the column-name convention (`latency_ms`, `cost_usd`) shows up on the axes as-is; refine via Axes → X/Y label when ambiguous.

## 4. Sharing with your team

- **Share charts with their settings**: `Export session` (top bar) → one JSON file holds the data and every chart's configuration. The recipient restores the exact screen with `Import session`.
- **Converting data**: whatever your format, paste the [agent prompt](README.en.md#converting-your-data-to-this-format-agent-prompt) from the README into any LLM together with your file.
- **Offline distribution**: copying the single `index-offline.html` file is enough — it works identically with no internet.

---

© mrc
