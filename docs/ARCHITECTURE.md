# Architecture

This is a small pipeline that keeps a ranked, sourced list of what's current in a domain
and publishes it as Markdown and PDF. AI models are the first domain. Nothing in the
schema or the scripts is specific to AI, so clothing or furniture trends would use the same tables.

```
 ┌─────────────────────────┐   scripts/upsert.py   ┌──────────────────┐
 │ research                │ ────────────────────▶ │ data/trends.db   │  committed, the
 │ today: scheduled        │  item / rank / retire │ (SQLite)         │  single source of truth
 │   assistant run         │  source / change / tag└────────┬─────────┘
 │ planned: LangChain      │                                │ git push to main
 │   agents on a VPS       │                                ▼
 └─────────────────────────┘               .github/workflows/render.yml
                                                            │ scripts/render.py
                                                            ▼
                                README.md · reports/<slug>.md · reports/<slug>.pdf
                                (committed back by github-actions[bot], [skip ci])
```

## Status

| Piece | State |
|---|---|
| SQLite schema, migrations, seed for `ai-models` | built |
| `scripts/upsert.py` write CLI | built |
| `scripts/render.py` (Markdown stdlib-only, PDF via WeasyPrint) | built |
| GitHub Actions render + commit-back + PDF artifact | built |
| Weekday research for `ai-models` | done today by a scheduled assistant that calls `upsert.py` |
| LangChain research agents on a private VPS (incl. social media sources) | **planned, not built** |
| Other domains (clothing, furniture, …) | **not started**; see "Adding a domain" |

## Data model (`db/schema.sql`)

- **domains**: one row per topic. Holds the report title, description, ranking basis, table column labels (`item_label`, `vendor_label`), footer note and `last_updated`.
- **items**: the ranked things. They have a free-text `released` field, `best_for`, `why_care` (inline Markdown), `rank`, and `status` (`active` or `retired`). Retired items stay in the DB for history but drop out of the reports.
- **sources**: one or more primary URLs per item, each with a `fetched_at` date. Every item should have one.
- **tag_definitions / item_tags**: per-domain sections such as "Open weights worth running". A tag can carry a short note, such as a license.
- **changes**: dated notes for "What changed lately". The newest 5 are shown.
- **schema_migrations**: bookkeeping for `db/migrations/*.sql`.

All dates are ISO `YYYY-MM-DD` in Europe/Prague.

## Rules

1. Never hand-edit `README.md` or `reports/*`. Change the DB, push, and let Actions render.
2. Write to the DB only through `scripts/upsert.py`. Agents should shell out to it or import `scripts/trendsdb.py`, not write SQL ad hoc.
3. Schema changes go in a new `db/migrations/NNN_*.sql`. Run `python scripts/upsert.py migrate` locally, then commit the migration together with the updated `data/trends.db`. CI fails if the committed DB has unapplied migrations.
4. Every item needs a source that was actually checked. Write vendor claims as claims.

## Adding a domain

```bash
python scripts/upsert.py domain furniture --title "Furniture trends" \
  --description "What's selling and why." \
  --ranking-basis "momentum across retailers and social, availability, price band" \
  --item-label Product --vendor-label Brand \
  --footer "Refreshed weekly."
python scripts/upsert.py item furniture "Boucle armchair" --vendor "Example Co" \
  --released "Oct 2026" --best-for "Small living rooms" --why "One plain sentence." \
  --source https://example.com/source --source-label example.com
python scripts/render.py --no-pdf   # optional local preview
git add data/trends.db && git commit -m "Add furniture domain" && git push
```

The new domain gets `reports/furniture.md` and `reports/furniture.pdf` and a row in the README's
domain table. The README's main section always shows `ai-models` (set by `FEATURED` in `render.py`).

## Local development

```bash
python scripts/render.py --no-pdf          # stdlib only
python -m venv .venv && .venv/bin/pip install -r requirements-pdf.txt
.venv/bin/python scripts/render.py         # + PDFs (needs Pango, e.g. apt install libpango-1.0-0)
python scripts/render.py --check           # exit 1 if committed Markdown is stale
```

PDFs embed randomly named font subsets, so they aren't byte-identical between runs. `render.py`
writes `reports/.<slug>.pdf.sha256` (a hash of the HTML input) and skips rebuilding a PDF whose input
hasn't changed, so unchanged data doesn't produce a noisy commit.
