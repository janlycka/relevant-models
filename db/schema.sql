-- Trend-tracking pipeline schema (SQLite).
-- data/trends.db is the source of truth; README.md and reports/* are rendered from it.
-- Domain-agnostic: "ai-models" is one domain; "clothing", "furniture", ... would be others.

PRAGMA foreign_keys = ON;

-- One row per tracked topic area.
CREATE TABLE IF NOT EXISTS domains (
    id            INTEGER PRIMARY KEY,
    slug          TEXT NOT NULL UNIQUE,          -- used for reports/<slug>.md|pdf
    title         TEXT NOT NULL,                 -- report heading
    description   TEXT NOT NULL DEFAULT '',      -- one-line subtitle
    ranking_basis TEXT NOT NULL DEFAULT '',      -- how the rank is decided (shown at top)
    item_label    TEXT NOT NULL DEFAULT 'Name',  -- table header for items, e.g. 'Model', 'Product'
    vendor_label  TEXT NOT NULL DEFAULT 'Vendor / brand', -- e.g. 'Vendor', 'Brand', 'Retailer'
    table_note    TEXT NOT NULL DEFAULT '',      -- small print under the ranked table
    footer        TEXT NOT NULL DEFAULT '',      -- refresh cadence note at the bottom
    last_updated  TEXT NOT NULL DEFAULT ''       -- ISO date (Europe/Prague) of last data change
);

-- The things being ranked: models, garments, sofas, ...
CREATE TABLE IF NOT EXISTS items (
    id              INTEGER PRIMARY KEY,
    domain_id       INTEGER NOT NULL REFERENCES domains(id) ON DELETE CASCADE,
    name            TEXT NOT NULL,
    vendor_or_brand TEXT NOT NULL DEFAULT '',
    released        TEXT NOT NULL DEFAULT '',    -- display text, e.g. "9 Nov 2026" or "Oct 2026 (weights)"
    best_for        TEXT NOT NULL DEFAULT '',
    why_care        TEXT NOT NULL DEFAULT '',    -- inline Markdown allowed (**bold**, `code`, [links](...))
    rank            INTEGER,                     -- 1 = most relevant; NULL when retired
    status          TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'retired')),
    first_seen      TEXT NOT NULL,               -- ISO date the item entered the DB
    last_updated    TEXT NOT NULL,               -- ISO date of last edit
    UNIQUE (domain_id, name)
);

-- Evidence: every item should have at least one primary source.
CREATE TABLE IF NOT EXISTS sources (
    id         INTEGER PRIMARY KEY,
    item_id    INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    url        TEXT NOT NULL,
    label      TEXT NOT NULL DEFAULT '',         -- link text in the table, e.g. "anthropic.com"
    fetched_at TEXT NOT NULL DEFAULT '',         -- ISO date the page was last checked
    UNIQUE (item_id, url)
);

-- Per-domain categories rendered as extra sections (e.g. "Open weights worth running").
CREATE TABLE IF NOT EXISTS tag_definitions (
    domain_id INTEGER NOT NULL REFERENCES domains(id) ON DELETE CASCADE,
    tag       TEXT NOT NULL,                     -- e.g. "open-weights"
    title     TEXT NOT NULL,                     -- section heading
    intro     TEXT NOT NULL DEFAULT '',          -- optional sentence above the list
    position  INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (domain_id, tag)
);

CREATE TABLE IF NOT EXISTS item_tags (
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    tag     TEXT NOT NULL,
    note    TEXT NOT NULL DEFAULT '',            -- e.g. "MIT", "pending: Apache 2.0 promised"
    PRIMARY KEY (item_id, tag)
);

-- Dated notes for the "What changed lately" section (newest first, latest N shown).
CREATE TABLE IF NOT EXISTS changes (
    id        INTEGER PRIMARY KEY,
    domain_id INTEGER NOT NULL REFERENCES domains(id) ON DELETE CASCADE,
    date      TEXT NOT NULL,                     -- ISO date, used for ordering
    headline  TEXT NOT NULL,                     -- rendered in bold
    text      TEXT NOT NULL                      -- inline Markdown allowed
);

CREATE INDEX IF NOT EXISTS idx_items_domain_rank ON items(domain_id, status, rank);
CREATE INDEX IF NOT EXISTS idx_changes_domain_date ON changes(domain_id, date);

-- Which db/migrations/*.sql files have been applied (managed by `scripts/upsert.py migrate`).
CREATE TABLE IF NOT EXISTS schema_migrations (
    filename   TEXT PRIMARY KEY,
    applied_at TEXT NOT NULL
);
