---
name: financial-report-analysis
description: "Analyze the most recently filed financial report (quarterly or annual earnings release) for any publicly traded company given its ticker, and produce a polished single-file dynamic HTML report: overview, an expectations-vs-actuals table (analyst consensus vs. reported figures with beat/miss/in-line calls), a segment/product-line revenue breakdown, capital allocation and cash-flow highlights, and an opinionated \"special attention\" analyst take. Use whenever the user gives a ticker (e.g. GOOG, AAPL, TSLA) and asks for earnings analysis, a financial report review, quarterly/annual results, \"how did $TICKER do last quarter\", beat-or-miss vs. estimates, an earnings summary, or a report/dashboard/HTML on a company's latest results \u2014 even without saying \"financial report\", e.g. \"what happened with Tesla's earnings\" or \"did Amazon beat estimates\". Not for deep multi-year fundamental/valuation screens against personal criteria \u2014 that's a different workflow."
---

# Custom Financial Report Analysis

Turn a bare ticker into a decision-useful earnings briefing: what the company reported, how it stacked up against what Wall Street expected, and the one thing about the quarter that actually deserves the reader's attention. The output is a single self-contained HTML file the user can open in any browser.

This skill was distilled from a real earnings walkthrough (Alphabet's Q2 2026 report) — the pattern that worked was: research thoroughly from primary sources first, separate the "headline" number from the "real" number when they diverge, and end with a genuine point of view rather than a recap.

## Step 1 — Identify the report

Search first; these figures are always more recent than any training data, and guessing at them is worse than saying you looked.

1. Search for `<TICKER> latest quarterly earnings report <current year>` to find the most recently submitted financial report and confirm its fiscal period (e.g. "Q2 2026", "fiscal Q1 2027") and filing/release date.
2. Most large-cap US issuers announce results via an 8-K with an earnings-release exhibit (Exhibit 99.1) — fetch that primary source (company investor-relations site or the SEC EDGAR filing) for the authoritative GAAP numbers rather than relying only on secondary summaries. Secondary sources (Yahoo Finance, CNBC, Zacks, StreetAccount, TradingKey, Reuters, etc.) are still valuable for analyst consensus estimates and market-reaction color that the press release itself won't contain.
3. Handle non-standard cadences gracefully: foreign private issuers may file a 6-K or 20-F with semi-annual results instead of quarterly ones; smaller companies may lag on 10-Q timing. Report the actual period covered rather than assuming "quarterly" is universal.
4. If the ticker doesn't resolve to a real, currently-reporting public company (delisted, private, ticker collision across exchanges), say so plainly instead of fabricating a report.

## Step 2 — Gather the comparison data

The centerpiece of this skill is the expectations-vs-actuals table, so this is the step worth the most care.

- Collect Wall Street consensus for total revenue and EPS. Most companies report both a GAAP EPS and a non-GAAP/adjusted EPS — capture both, because they can tell very different stories (see Step 4).
- Collect segment- or product-line-level consensus where analysts publish it (e.g. cloud revenue, a specific product line, same-store sales) — this is usually where the more interesting beats/misses hide, not in the topline.
- Cross-check figures across at least two sources when you can. Consensus numbers genuinely vary by aggregator (Zacks vs. StreetAccount vs. a bank's estimate can differ by a percent or two) — if sources disagree, use a representative figure and say "~" rather than presenting one aggregator's number as an exact, uncontested truth.
- Note the actual reported figures precisely from the primary source, in the same units and GAAP/non-GAAP framing as the estimate you're comparing against. Comparing a GAAP actual to a non-GAAP estimate (or vice versa) produces a nonsense "beat" or "miss."

## Step 3 — Find the market-reaction and structural context

Pull whatever's available on: how the stock actually moved after the report, any guidance raised/lowered/withdrawn, and any one-time items sitting in the income statement or cash-flow statement that distort the headline (asset sales, equity-stake mark-to-market gains, restructuring charges, tax true-ups, litigation reserves). This context is what makes Step 5's callout possible — without it, the "special attention" section degenerates into restating the headline.

## Step 4 — Decide what the segment breakdown should show

Most large companies report distinct operating segments — use those for the revenue-by-segment visualization. If a company doesn't have meaningfully distinct segments (a single-product or single-line business), repurpose that section for a geographic or product-line breakdown instead, or drop it entirely rather than forcing a chart onto data that doesn't have parts worth comparing.

## Step 5 — Build the HTML report

Use `assets/template.html` as the starting point — it's a complete, tested dashboard shell with the visual design already solved (dark theme, KPI cards, animated segment bars, styled comparison table with beat/miss pills, capital-allocation grid, callout box). Read it, copy it, and fill in every `{{PLACEHOLDER}}` token — do not leave any unfilled, and do not rebuild the CSS/layout from scratch each time; that work is already done and reusing it keeps quality consistent across tickers.

Placeholder reference:

| Token | What goes there |
|---|---|
| `{{COMPANY_NAME}}` | Full legal/common name, e.g. "Alphabet Inc." |
| `{{TICKER_LINE}}` | Exchange + ticker(s), e.g. "NASDAQ: GOOG / GOOGL" |
| `{{QUARTER_LABEL}}` | e.g. "Q2 2026" |
| `{{PERIOD_LINE}}` | e.g. "Quarter ended June 30, 2026 · Reported July 22, 2026" |
| `{{STREAK_BADGE}}` | A short factual highlight badge (growth streak, record quarter, etc.) — if nothing notable applies, use a neutral phrase like "Latest filed report" |
| `{{ACCENT}}` | A hex accent color. Default `#4285F4` (blue) is safe and neutral; feel free to nudge it toward an unmistakable brand color (e.g. a well-known retailer's or automaker's signature color) only when doing so is obviously fitting and not a stretch |
| `{{MONOGRAM}}` | 1–2 letters for the avatar circle, usually the primary ticker's first letter(s) |
| `{{KPI1_LABEL}}` / `{{KPI1_VALUE}}` / `{{KPI1_DELTA}}` / `{{KPI1_DIR}}` (and KPI2–4) | Four headline metrics. `{{KPIn_DIR}}` must be exactly `up`, `down`, or `neutral` (controls color). Good default choices: revenue, operating income or margin, primary EPS figure, and one metric that captures the quarter's real story (free cash flow, a guidance change, a segment inflection — whatever a sharp analyst would flag first) |
| `{{OVERVIEW_HTML}}` | 3–4 tight `<p>` paragraphs. Lead with the topline beat/miss and why, explain the main segment drivers, and explicitly flag any accounting distortion in headline profit (don't bury this) |
| `{{TABLE_ROWS_HTML}}` | One `<tr>` per comparison metric — see table format below |
| `{{TABLE_FOOTNOTE}}` | Cite where estimates came from and note any GAAP/non-GAAP framing caveats |
| `{{SEGMENTS_JS_ARRAY}}` | JS array literal of `{ label, value, color }` objects for the bar chart, values in the same unit (e.g. millions) |
| `{{SEGMENTS_FOOTNOTE}}` | One line explaining what the bars represent and their scale |
| `{{LEFT_COLUMN_TITLE}}` / `{{LEFT_STATS_HTML}}` | Usually "Capital & Cash Flow" — capex, free cash flow, cash position, debt, buybacks, dividend |
| `{{RIGHT_COLUMN_TITLE}}` / `{{RIGHT_STATS_HTML}}` | Usually "Segment Operating Income" or "Operating Highlights" — adapt the actual rows (`.mini-stat` divs) to whatever the company actually reports; don't invent line items it doesn't have |
| `{{SPECIAL_ATTENTION_TAG}}` | Usually "Analyst take" |
| `{{SPECIAL_ATTENTION_TITLE}}` | A one-line headline for the insight, ideally with a touch of specificity, not "Key takeaways" |
| `{{SPECIAL_ATTENTION_HTML}}` | See below |
| `{{SOURCES_LINE}}` | Plain-text list of where the data came from (press release/filing + estimate sources), with the as-of date |

If the segment breakdown doesn't apply (Step 4), delete the whole block between `<!-- SEGMENTS_SECTION_START -->` and `<!-- SEGMENTS_SECTION_END -->` (including the script block that populates it) rather than leaving an empty chart.

**Expectations-vs-actuals table format** — each row needs a metric name, the estimate, the actual, and a result pill:
```html
<tr>
  <td>Total revenue</td>
  <td class="num">~$117.0B</td>
  <td class="num">$119.80B</td>
  <td class="num"><span class="result-pill beat">▲ Beat +2.4%</span></td>
</tr>
```
Use `class="beat"` / `class="miss"` / `class="flat"` on the pill, and `▲` / `▼` / `≈` accordingly. Compute the percentage difference yourself rather than eyeballing it. Include every metric you have a genuine estimate for — don't pad the table with rows that just say "n/a" across the board, but a row noting "topped estimates" without an exact consensus figure is fine when that's genuinely all that's available.

**The "special attention" section is the part most worth getting right.** It should not restate the headline number or the overview in different words — it should read like a sharp analyst's one real point about the quarter, the thing that would make someone say "huh, I hadn't thought about it that way." Good candidates: a headline profit number that's mostly a one-time gain in disguise, a capital-structure or funding shift (e.g. free cash flow turning negative, buybacks pausing, debt/equity raises), a segment quietly inflecting up or down, a guidance signal buried in the call, or a KPI moving in a direction that contradicts the narrative the press release is telling. Write it with a clear point of view and back it with the specific numbers from Steps 2–3, not vague hedging.

## Step 6 — Deliver

Save the file as `{TICKER}_{Quarter}_{Year}_Earnings_Report.html` (e.g. `GOOG_Q2_2026_Earnings_Report.html`) to the outputs location, then present it to the user. Keep the chat response itself short — the file is the deliverable, the surrounding message is not an essay recapping the file.

Always include a Sources section (per standard citation practice) listing the primary filing/press release and the estimate sources used, since this analysis is built entirely from web research.

## Tone and quality bar

Write for a financially literate reader who doesn't need basic terms defined but does want precision: exact figures with units, explicit YoY/QoQ framing, no hype adjectives, no filler caveats. State beats/misses and percentages confidently when the underlying data supports it; flag genuine uncertainty (estimate disagreement, non-comparable GAAP/non-GAAP framing) explicitly rather than smoothing over it.

## Edge cases

- **No consensus estimates exist** (thinly covered small-caps): say so in the table rather than inventing a number — a row can legitimately read "No analyst consensus published" in the estimate column.
- **Report not yet released this cycle**: if the user asks during a quiet period before the next report, use the most recently *actually filed* report and say which period that covers, rather than assuming the user meant something not yet public.
- **Multiple share classes / tickers** (e.g. GOOG vs. GOOGL): note both in `{{TICKER_LINE}}` but treat the company as one entity for the analysis.
- **Loss-making or pre-revenue companies**: the KPI cards and table should flex to whatever metrics are actually meaningful (e.g. cash runway, bookings, ARR) rather than forcing EPS/revenue framing where it doesn't fit.
