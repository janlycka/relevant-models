#!/usr/bin/env python3
"""Write to data/trends.db: the only supported way to change tracked data.

Every write stamps the domain's last_updated (Europe/Prague date, or --date).
Examples (domain "ai-models"):

  upsert.py migrate
  upsert.py item ai-models "Claude Fable 5.2" --vendor Anthropic --released "9 Nov 2026" \\
      --best-for "Mathematicians" --why "One plain sentence." --rank 1 \\
      --source https://www.anthropic.com/claude-fable-and-mythos-5-2 --source-label anthropic.com
  upsert.py rank ai-models "Claude Fable 5.2" "Claude Opus 5.5" "GPT-6.1 Sol" ...
  upsert.py retire ai-models "GPT-6 Luna"
  upsert.py source ai-models "GPT-6 Luna" https://openai.com/... --label openai.com
  upsert.py change ai-models --headline "Muse Ember (9 Nov)" --text "..." --date 2026-11-09
  upsert.py tag ai-models "Inkling 2 Small" open-weights --note "open now, Apache 2.0"
  upsert.py touch ai-models          # mark checked today without other edits
  upsert.py list ai-models
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import trendsdb  # noqa: E402

ITEM_FIELDS = {  # CLI option -> column
    "vendor": "vendor_or_brand", "released": "released", "best_for": "best_for",
    "why": "why_care", "rank": "rank",
}


def stamp(conn, slug, day):
    conn.execute("UPDATE domains SET last_updated = ? WHERE slug = ?", (day, slug))


def renumber(conn, did, day):
    """Close gaps so active ranks run 1..N in their current order."""
    rows = conn.execute(
        "SELECT id, rank FROM items WHERE domain_id = ? AND status = 'active' "
        "ORDER BY rank IS NULL, rank, last_updated DESC, name", (did,)).fetchall()
    for n, r in enumerate(rows, 1):
        if r["rank"] != n:
            conn.execute("UPDATE items SET rank = ?, last_updated = ? WHERE id = ?", (n, day, r["id"]))


def cmd_migrate(conn, a):
    applied = trendsdb.migrate(conn)
    print("applied:", ", ".join(applied) if applied else "nothing (up to date)")


def cmd_domain(conn, a):
    fields = {k: v for k, v in {
        "title": a.title, "description": a.description, "ranking_basis": a.ranking_basis,
        "item_label": a.item_label, "vendor_label": a.vendor_label,
        "table_note": a.table_note, "footer": a.footer}.items() if v is not None}
    exists = conn.execute("SELECT 1 FROM domains WHERE slug = ?", (a.slug,)).fetchone()
    if exists:
        if fields:
            conn.execute(f"UPDATE domains SET {', '.join(f'{k} = ?' for k in fields)} WHERE slug = ?",
                         (*fields.values(), a.slug))
        print("updated domain", a.slug)
    else:
        if not a.title:
            raise SystemExit("--title is required for a new domain")
        fields["slug"] = a.slug
        conn.execute(f"INSERT INTO domains ({', '.join(fields)}) VALUES ({', '.join('?' * len(fields))})",
                     tuple(fields.values()))
        print("created domain", a.slug)
    stamp(conn, a.slug, a.date)


def cmd_item(conn, a):
    did = trendsdb.domain_id(conn, a.domain)
    vals = {col: getattr(a, opt) for opt, col in ITEM_FIELDS.items() if getattr(a, opt) is not None}
    row = conn.execute("SELECT id, rank FROM items WHERE domain_id = ? AND name = ?", (did, a.name)).fetchone()
    if a.rename:
        vals["name"] = a.rename
    if row is None:
        if a.rank is None:  # new items go to the bottom unless ranked explicitly
            vals["rank"] = (conn.execute("SELECT COALESCE(MAX(rank), 0) FROM items WHERE domain_id = ? "
                                         "AND status = 'active'", (did,)).fetchone()[0] + 1)
        vals.setdefault("name", a.name)
        vals.update(domain_id=did, status="active", first_seen=a.date, last_updated=a.date)
        if a.rank is not None:  # make room
            conn.execute("UPDATE items SET rank = rank + 1 WHERE domain_id = ? AND status = 'active' "
                         "AND rank >= ?", (did, a.rank))
        cur = conn.execute(f"INSERT INTO items ({', '.join(vals)}) VALUES ({', '.join('?' * len(vals))})",
                           tuple(vals.values()))
        item_id = cur.lastrowid
        print("added", a.name, "at rank", vals["rank"])
    else:
        item_id = row["id"]
        if a.rank is not None and a.rank != row["rank"]:
            old = row["rank"] if row["rank"] is not None else 10**9
            if a.rank < old:
                conn.execute("UPDATE items SET rank = rank + 1 WHERE domain_id = ? AND status = 'active' "
                             "AND rank >= ? AND rank < ? AND id != ?", (did, a.rank, old, item_id))
            else:
                conn.execute("UPDATE items SET rank = rank - 1 WHERE domain_id = ? AND status = 'active' "
                             "AND rank > ? AND rank <= ? AND id != ?", (did, old, a.rank, item_id))
        vals["status"] = "active"
        vals["last_updated"] = a.date
        conn.execute(f"UPDATE items SET {', '.join(f'{k} = ?' for k in vals)} WHERE id = ?",
                     (*vals.values(), item_id))
        print("updated", a.name)
    if a.source:
        add_source(conn, item_id, a.source, a.source_label or "", a.date, a.replace_sources)
    renumber(conn, did, a.date)
    stamp(conn, a.domain, a.date)


def add_source(conn, item_id, url, label, day, replace=False):
    if replace:
        conn.execute("DELETE FROM sources WHERE item_id = ?", (item_id,))
    conn.execute(
        "INSERT INTO sources (item_id, url, label, fetched_at) VALUES (?, ?, ?, ?) "
        "ON CONFLICT(item_id, url) DO UPDATE SET fetched_at = excluded.fetched_at, "
        "label = CASE WHEN excluded.label = '' THEN sources.label ELSE excluded.label END",
        (item_id, url, label, day))


def cmd_source(conn, a):
    it = trendsdb.item_row(conn, a.domain, a.name)
    add_source(conn, it["id"], a.url, a.label or "", a.date, a.replace)
    print("source recorded for", a.name)
    stamp(conn, a.domain, a.date)


def cmd_retire(conn, a):
    it = trendsdb.item_row(conn, a.domain, a.name)
    conn.execute("UPDATE items SET status = 'retired', rank = NULL, last_updated = ? WHERE id = ?",
                 (a.date, it["id"]))
    renumber(conn, it["domain_id"], a.date)
    stamp(conn, a.domain, a.date)
    print("retired", a.name)


def cmd_rank(conn, a):
    did = trendsdb.domain_id(conn, a.domain)
    for n, name in enumerate(a.names, 1):
        it = trendsdb.item_row(conn, a.domain, name)
        if it["status"] != "active":
            raise SystemExit(f"{name!r} is retired; re-activate it with `item` first")
        conn.execute("UPDATE items SET rank = ?, last_updated = ? WHERE id = ?", (-n, a.date, it["id"]))
    # unlisted active items keep their relative order after the listed ones
    rest = conn.execute("SELECT id FROM items WHERE domain_id = ? AND status = 'active' AND rank > 0 "
                        "ORDER BY rank", (did,)).fetchall()
    for k, r in enumerate(rest, len(a.names) + 1):
        conn.execute("UPDATE items SET rank = ? WHERE id = ?", (k, r["id"]))
    conn.execute("UPDATE items SET rank = -rank WHERE domain_id = ? AND rank < 0", (did,))
    stamp(conn, a.domain, a.date)
    print(f"ranked {len(a.names)} items; {len(rest)} unlisted kept below")


def cmd_change(conn, a):
    did = trendsdb.domain_id(conn, a.domain)
    conn.execute("INSERT INTO changes (domain_id, date, headline, text) VALUES (?, ?, ?, ?)",
                 (did, a.date, a.headline, a.text))
    stamp(conn, a.domain, a.date)
    print("change note added")


def cmd_tag(conn, a):
    it = trendsdb.item_row(conn, a.domain, a.name)
    if a.remove:
        conn.execute("DELETE FROM item_tags WHERE item_id = ? AND tag = ?", (it["id"], a.tag))
    else:
        if not conn.execute("SELECT 1 FROM tag_definitions WHERE domain_id = ? AND tag = ?",
                            (it["domain_id"], a.tag)).fetchone():
            if not a.section_title:
                raise SystemExit(f"tag {a.tag!r} is new for this domain; pass --section-title")
            conn.execute("INSERT INTO tag_definitions (domain_id, tag, title, position) VALUES "
                         "(?, ?, ?, (SELECT COALESCE(MAX(position), 0) + 1 FROM tag_definitions "
                         "WHERE domain_id = ?))", (it["domain_id"], a.tag, a.section_title, it["domain_id"]))
        conn.execute("INSERT INTO item_tags (item_id, tag, note) VALUES (?, ?, ?) "
                     "ON CONFLICT(item_id, tag) DO UPDATE SET note = excluded.note",
                     (it["id"], a.tag, a.note or ""))
    stamp(conn, a.domain, a.date)
    print(("removed" if a.remove else "set"), "tag", a.tag, "on", a.name)


def cmd_touch(conn, a):
    trendsdb.domain_id(conn, a.domain)
    stamp(conn, a.domain, a.date)
    print("last_updated =", a.date)


def cmd_list(conn, a):
    did = trendsdb.domain_id(conn, a.domain)
    q = "SELECT rank, name, vendor_or_brand, released, status FROM items WHERE domain_id = ?"
    if not a.all:
        q += " AND status = 'active'"
    for r in conn.execute(q + " ORDER BY status, rank IS NULL, rank, name", (did,)):
        print(f"{r['rank'] if r['rank'] is not None else '-':>3}  {r['name']}  |  {r['vendor_or_brand']}  |  "
              f"{r['released']}" + ("  [retired]" if r["status"] == "retired" else ""))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--db", default=str(trendsdb.DB_PATH))
    p.add_argument("--date", default=trendsdb.today(), help="ISO date to stamp (default: today, Prague)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("migrate", help="create/upgrade the DB from db/schema.sql + db/migrations")

    s = sub.add_parser("domain", help="create or update a domain")
    s.add_argument("slug")
    for f in ("title", "description", "ranking-basis", "item-label", "vendor-label", "table-note", "footer"):
        s.add_argument(f"--{f}")

    s = sub.add_parser("item", help="add an item or update the fields you pass")
    s.add_argument("domain"); s.add_argument("name")
    s.add_argument("--rename"); s.add_argument("--vendor"); s.add_argument("--released")
    s.add_argument("--best-for", dest="best_for"); s.add_argument("--why")
    s.add_argument("--rank", type=int, help="move to this rank, shifting others")
    s.add_argument("--source", help="primary source URL"); s.add_argument("--source-label")
    s.add_argument("--replace-sources", action="store_true", help="drop old sources first")

    s = sub.add_parser("source", help="add/refresh a source URL on an item")
    s.add_argument("domain"); s.add_argument("name"); s.add_argument("url")
    s.add_argument("--label"); s.add_argument("--replace", action="store_true")

    s = sub.add_parser("retire", help="drop an item from the ranking (kept in DB)")
    s.add_argument("domain"); s.add_argument("name")

    s = sub.add_parser("rank", help="set the full order: names listed become 1..N")
    s.add_argument("domain"); s.add_argument("names", nargs="+")

    s = sub.add_parser("change", help="add a 'What changed lately' note")
    s.add_argument("domain"); s.add_argument("--headline", required=True); s.add_argument("--text", required=True)

    s = sub.add_parser("tag", help="put an item in a section such as open-weights")
    s.add_argument("domain"); s.add_argument("name"); s.add_argument("tag")
    s.add_argument("--note"); s.add_argument("--remove", action="store_true")
    s.add_argument("--section-title", help="heading when the tag is new for the domain")

    s = sub.add_parser("touch", help="stamp last_updated without other changes")
    s.add_argument("domain")

    s = sub.add_parser("list", help="print the current ranking")
    s.add_argument("domain"); s.add_argument("--all", action="store_true", help="include retired")

    a = p.parse_args()
    conn = trendsdb.connect(a.db)
    if a.cmd != "migrate" and not conn.execute(
            "SELECT 1 FROM sqlite_master WHERE name = 'domains'").fetchone():
        raise SystemExit("database not initialised; run `upsert.py migrate` first")
    globals()[f"cmd_{a.cmd}"](conn, a)
    conn.commit()


if __name__ == "__main__":
    main()
