"""Shared helpers for the trends SQLite database (stdlib only)."""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "trends.db"
SCHEMA = ROOT / "db" / "schema.sql"
MIGRATIONS = ROOT / "db" / "migrations"
TZ = ZoneInfo("Europe/Prague")


def today() -> str:
    """ISO date in Europe/Prague, the timezone all dates in the DB use."""
    return datetime.now(TZ).date().isoformat()


def connect(path: Path | str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate(conn: sqlite3.Connection) -> list[str]:
    """Apply db/schema.sql (idempotent) and any db/migrations/*.sql not yet applied."""
    conn.executescript(SCHEMA.read_text())
    done = {r[0] for r in conn.execute("SELECT filename FROM schema_migrations")}
    applied = []
    for f in sorted(MIGRATIONS.glob("*.sql")):
        if f.name in done:
            continue
        conn.executescript(f.read_text())
        conn.execute(
            "INSERT INTO schema_migrations (filename, applied_at) VALUES (?, ?)",
            (f.name, today()),
        )
        conn.commit()
        applied.append(f.name)
    return applied


def domain_id(conn: sqlite3.Connection, slug: str) -> int:
    row = conn.execute("SELECT id FROM domains WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        raise SystemExit(f"unknown domain: {slug!r} (create it with `upsert.py domain`)")
    return row["id"]


def item_row(conn: sqlite3.Connection, slug: str, name: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT i.* FROM items i JOIN domains d ON d.id = i.domain_id "
        "WHERE d.slug = ? AND i.name = ?",
        (slug, name),
    ).fetchone()
    if row is None:
        raise SystemExit(f"unknown item {name!r} in domain {slug!r}")
    return row
