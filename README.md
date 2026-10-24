# skills

Reusable AI agent skills in the open `SKILL.md` format (a folder with a `SKILL.md`
that has `name` / `description` frontmatter, plus optional supporting files).
Any agent that loads skills from a directory can use them (Claude Code, Hermes, ...).

## Skills

| Skill | Language | What it does | Output |
|-------|----------|--------------|--------|
| [`stock-analysis`](skills/stock-analysis) | Bulgarian | Fundamental analysis of a ticker scored against six fixed thresholds: D/E <= 0.50, P/E <= 20 (<= 30 for high quality), ROE > 15%, ROIC > 12%, Debt/EBITDA < 1.5, Current Ratio > 1.0. Data from stockanalysis.com. | `<TICKER>_fundamental_analysis.html` |
| [`financial-report-analysis`](skills/financial-report-analysis) | English | Latest filed earnings report for a ticker: consensus vs. actuals (beat/miss), segment revenue, cash flow and capital allocation, and an analyst "special attention" take. Primary source is the 8-K / press release. | `<TICKER>_<Q>_<Year>_Earnings_Report.html` |

They are complementary: `financial-report-analysis` covers the most recent report;
`stock-analysis` is a multi-year screen against personal criteria.

## Install

Requires only bash (and Python 3 for packaging).

    git clone https://github.com/MDimitroff/skills.git
    cd skills
    ./install.sh                         # all skills -> ~/.claude/skills
    ./install.sh --target hermes         # -> ~/.hermes/skills
    ./install.sh --target /some/dir      # any skills directory
    ./install.sh stock-analysis          # a single skill
    ./install.sh --link                  # symlink instead of copy (for editing)

Re-running replaces the installed copy. Restart the agent session afterwards so it
rescans skills. Manual install is equally valid: copy a folder from `skills/` into
your agent's skills directory.

## Distribute as zip files

    python3 scripts/package.py

Writes `dist/<skill>.zip` (git-ignored), one per skill, with the skill folder at the
zip root (`stock-analysis/SKILL.md`, ...). The build is deterministic and fails if a
skill's frontmatter `name` does not match its folder name. Attach the zips to a
GitHub Release, or send them directly; recipients unzip into their skills directory
or use their client's "upload skill" feature where available.

## Usage

    /stock-analysis MSFT
    How did AAPL do last quarter? Did they beat estimates?

Skills trigger from their `description` text, so natural-language requests work too.

## Requirements and caveats

- **Network access:** both skills research the live web (stockanalysis.com, SEC EDGAR,
  investor-relations pages, news). The agent needs web fetch/search tools.
- **Chart.js via CDN:** the `stock-analysis` HTML report loads Chart.js 4.4.1 from
  cdnjs.cloudflare.com, so charts need internet when the report is opened.
  `financial-report-analysis` output is fully self-contained.
- **`stock-analysis` is personalised:** thresholds and the Bulgarian output language are
  the author's preferences, hard-coded in `SKILL.md`. Edit the criteria table to adapt it.
- **Tool names:** `stock-analysis` mentions `WebFetch`, `WebSearch` and `present_files`.
  On agents with different tool names, the agent maps them to its equivalents.
- **Not investment advice.** Reports are analytical information. Data comes from third
  parties and can be wrong or stale; verify before acting.

## Repository layout

    .
    |-- README.md
    |-- install.sh                      # copy/symlink skills into an agent's skills dir
    |-- scripts/
    |   `-- package.py                  # build dist/<skill>.zip (stdlib only)
    `-- skills/
        |-- stock-analysis/
        |   |-- SKILL.md
        |   `-- templates/report_template.html
        `-- financial-report-analysis/
            |-- SKILL.md
            `-- assets/template.html

## Adding a skill

1. Create `skills/<name>/SKILL.md` with `name` (identical to the folder name) and a
   `description` that states when to trigger.
2. Put templates under `templates/` or `assets/`; keep secrets and personal data out.
3. Run `python3 scripts/package.py` to validate, and update the table above.
