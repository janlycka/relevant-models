#!/usr/bin/env python3
"""Render README.md, reports/<slug>.md and reports/<slug>.pdf from data/trends.db.

Markdown rendering is stdlib-only. PDF rendering uses WeasyPrint (HTML -> PDF) and is
skipped with a warning if WeasyPrint is not installed, unless --require-pdf is given.

    python scripts/render.py                # MD + PDF (if weasyprint importable)
    python scripts/render.py --no-pdf       # Markdown only
    python scripts/render.py --check        # exit 1 if committed Markdown is stale
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import trendsdb  # noqa: E402

ROOT = trendsdb.ROOT
REPORTS = ROOT / "reports"
README = ROOT / "README.md"
FEATURED = "ai-models"      # domain shown on the README landing page
CHANGES_SHOWN = 5           # "What changed lately" bullets per domain
GEN_NOTE = "generated from data/trends.db by scripts/render.py, do not edit by hand"
REPO_URL = "https://github.com/janlycka/relevant-models"


# ---------------------------------------------------------------- data access
def load_domain(conn, slug: str) -> dict:
    d = conn.execute("SELECT * FROM domains WHERE slug = ?", (slug,)).fetchone()
    if d is None:
        raise SystemExit(f"unknown domain {slug!r}")
    items = conn.execute(
        "SELECT * FROM items WHERE domain_id = ? AND status = 'active' "
        "ORDER BY rank IS NULL, rank, name",
        (d["id"],),
    ).fetchall()
    sources = {}
    for s in conn.execute(
        "SELECT s.* FROM sources s JOIN items i ON i.id = s.item_id "
        "WHERE i.domain_id = ? ORDER BY s.id",
        (d["id"],),
    ):
        sources.setdefault(s["item_id"], []).append(s)
    changes = conn.execute(
        "SELECT * FROM changes WHERE domain_id = ? ORDER BY date DESC, id LIMIT ?",
        (d["id"], CHANGES_SHOWN),
    ).fetchall()
    sections = []
    for t in conn.execute(
        "SELECT * FROM tag_definitions WHERE domain_id = ? ORDER BY position, tag", (d["id"],)
    ):
        members = conn.execute(
            "SELECT i.name, it.note FROM item_tags it JOIN items i ON i.id = it.item_id "
            "WHERE i.domain_id = ? AND it.tag = ? AND i.status = 'active' "
            "ORDER BY i.rank IS NULL, i.rank, i.name",
            (d["id"], t["tag"]),
        ).fetchall()
        if members:
            sections.append({"title": t["title"], "intro": t["intro"], "members": members})
    return {"d": d, "items": items, "sources": sources, "changes": changes, "sections": sections}


def human_date(iso: str) -> str:
    if not iso:
        return "n/a"
    dt = date.fromisoformat(iso)
    return f"{dt.day} {dt.strftime('%b %Y')}"


def cell(text: str) -> str:
    """Make text safe for a Markdown table cell."""
    return text.replace("|", "\\|").replace("\n", " ")


# ------------------------------------------------------------------- Markdown
def domain_markdown(data: dict, level: int = 1) -> str:
    d, h = data["d"], "#" * level
    sub = "#" * (level + 1)
    out = [f"{h} {d['title']}", ""]
    if d["description"]:
        out += [d["description"], ""]
    out.append(f"**Last updated:** {human_date(d['last_updated'])} (Prague)  ")
    if d["ranking_basis"]:
        out.append(f"**How the ranking works:** {d['ranking_basis']}")
    out.append("")
    if data["changes"]:
        out += [f"{sub} What changed lately", ""]
        out += [f"- **{c['headline']}:** {c['text']}" for c in data["changes"]]
        out.append("")
    out += [f"{sub} Ranked", ""]
    out.append(f"| # | {d['item_label']} | {d['vendor_label']} | Released | Best for | Why you should care | Source |")
    out.append("|---|---|---|---|---|---|---|")
    for it in data["items"]:
        links = ", ".join(
            f"[{s['label'] or s['url']}]({s['url']})" for s in data["sources"].get(it["id"], [])
        )
        out.append(
            "| " + " | ".join(cell(str(x)) for x in (
                it["rank"] if it["rank"] is not None else "–", it["name"], it["vendor_or_brand"],
                it["released"], it["best_for"], it["why_care"])) + f" | {links} |"
        )
    out.append("")
    if d["table_note"]:
        out += [d["table_note"], ""]
    for s in data["sections"]:
        out += [f"{sub} {s['title']}", ""]
        if s["intro"]:
            out += [s["intro"], ""]
        out += [f"- **{m['name']}**" + (f": {m['note']}" if m["note"] else "") for m in s["members"]]
        out.append("")
    if d["footer"]:
        out += ["---", "", d["footer"], ""]
    return "\n".join(out)


def readme_markdown(featured: dict, domains: list) -> str:
    rows = "\n".join(
        f"| {d['title']} (`{d['slug']}`) | {human_date(d['last_updated'])} | "
        f"[Markdown](reports/{d['slug']}.md) · [PDF](reports/{d['slug']}.pdf) |"
        for d in domains
    )
    intro = (
        "> This page is rendered from a SQLite database (`data/trends.db`) by GitHub Actions. "
        "See [How this repo works](#how-this-repo-works)."
    )
    body = domain_markdown(featured, level=1).split("\n")
    # insert the intro line right after the title
    body = body[:2] + [intro, ""] + body[2:]
    about = f"""## How this repo works

A small, domain-agnostic trend-tracking pipeline. AI models are the first domain.

```
research (today: a scheduled assistant; planned: LangChain agents on a private VPS)
   │  scripts/upsert.py  (add / update / retire items, sources, change notes)
   ▼
data/trends.db  (SQLite, committed: the single source of truth)
   │  push to main → .github/workflows/render.yml → scripts/render.py
   ▼
README.md · reports/<domain>.md · reports/<domain>.pdf  (generated, never hand-edited)
```

| Domain | Last updated | Reports |
|---|---|---|
{rows}

Schema: [`db/schema.sql`](db/schema.sql) · Architecture and how to add a domain: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
"""
    return f"<!-- {GEN_NOTE} -->\n" + "\n".join(body).rstrip() + "\n\n" + about


# ----------------------------------------------------------------------- HTML
_INLINE = re.compile(r"`([^`]+)`|\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)\s]+)\)")


def inline_html(text: str) -> str:
    out, pos = [], 0
    for m in _INLINE.finditer(text):
        out.append(html.escape(text[pos:m.start()]))
        if m.group(1) is not None:
            out.append(f"<code>{html.escape(m.group(1))}</code>")
        elif m.group(2) is not None:
            out.append(f"<strong>{inline_html(m.group(2))}</strong>")
        else:
            out.append(f'<a href="{html.escape(m.group(4))}">{inline_html(m.group(3))}</a>')
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return "".join(out)


CSS = """
@page { size: A4 landscape; margin: 12mm 10mm 14mm 10mm;
        @bottom-right { content: counter(page) " / " counter(pages); font-family: "DejaVu Sans", sans-serif; font-size: 7pt; color: #777; }
        @bottom-left { content: "generated from data/trends.db"; font-family: "DejaVu Sans", sans-serif; font-size: 7pt; color: #777; } }
body { font-family: "DejaVu Sans", "Liberation Sans", Arial, sans-serif; font-size: 8.5pt; color: #111; line-height: 1.35; }
h1 { font-size: 17pt; margin: 0 0 2mm 0; }
h2 { font-size: 11.5pt; margin: 5mm 0 2mm 0; border-bottom: 1px solid #ccc; }
p { margin: 1.2mm 0; }
ul { margin: 1mm 0 1mm 5mm; padding: 0; }
table { width: 100%; border-collapse: collapse; font-size: 7.4pt; }
thead { display: table-header-group; }
th { background: #222; color: #fff; text-align: left; padding: 1.4mm; }
td { border-bottom: 0.4pt solid #ccc; padding: 1.2mm 1.4mm; vertical-align: top; }
tr { page-break-inside: avoid; }
tr:nth-child(even) td { background: #f5f5f5; }
td.rank { width: 4mm; font-weight: bold; text-align: right; }
td.name { width: 30mm; font-weight: bold; } td.vendor { width: 24mm; } td.rel { width: 20mm; }
td.best { width: 38mm; } td.src { width: 30mm; word-break: break-all; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 92%; background: #eee; padding: 0 0.6mm; }
a { color: #0645ad; text-decoration: none; }
.meta { color: #333; } .small { color: #555; font-size: 7.5pt; }
"""


def domain_html(data: dict) -> str:
    d = data["d"]
    e = inline_html
    parts = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'>",
        f"<title>{html.escape(d['title'])}</title>",
        f"<meta name='author' content='{REPO_URL}'>",
        f"<meta name='dcterms.created' content='{d['last_updated']}'>",
        f"<meta name='dcterms.modified' content='{d['last_updated']}'>",
        f"<style>{CSS}</style></head><body>",
        f"<!-- {GEN_NOTE} -->",
        f"<h1>{e(d['title'])}</h1>",
    ]
    if d["description"]:
        parts.append(f"<p>{e(d['description'])}</p>")
    parts.append(f"<p class='meta'><strong>Last updated:</strong> {human_date(d['last_updated'])} (Prague)"
                 + (f" · <strong>How the ranking works:</strong> {e(d['ranking_basis'])}" if d["ranking_basis"] else "")
                 + "</p>")
    if data["changes"]:
        parts.append("<h2>What changed lately</h2><ul>")
        parts += [f"<li><strong>{e(c['headline'])}:</strong> {e(c['text'])}</li>" for c in data["changes"]]
        parts.append("</ul>")
    parts.append(f"<h2>Ranked</h2><table><thead><tr><th>#</th><th>{e(d['item_label'])}</th><th>{e(d['vendor_label'])}</th>"
                 "<th>Released</th><th>Best for</th><th>Why you should care</th><th>Source</th></tr></thead><tbody>")
    for it in data["items"]:
        links = "<br>".join(f"<a href='{html.escape(s['url'])}'>{html.escape(s['label'] or s['url'])}</a>"
                            for s in data["sources"].get(it["id"], []))
        parts.append(
            f"<tr><td class='rank'>{it['rank'] if it['rank'] is not None else '–'}</td>"
            f"<td class='name'>{e(it['name'])}</td><td class='vendor'>{e(it['vendor_or_brand'])}</td>"
            f"<td class='rel'>{e(it['released'])}</td><td class='best'>{e(it['best_for'])}</td>"
            f"<td>{e(it['why_care'])}</td><td class='src'>{links}</td></tr>")
    parts.append("</tbody></table>")
    if d["table_note"]:
        parts.append(f"<p class='small'>{e(d['table_note'])}</p>")
    for s in data["sections"]:
        parts.append(f"<h2>{e(s['title'])}</h2>")
        if s["intro"]:
            parts.append(f"<p>{e(s['intro'])}</p>")
        parts.append("<ul>" + "".join(
            f"<li><strong>{e(m['name'])}</strong>" + (f": {e(m['note'])}" if m["note"] else "") + "</li>"
            for m in s["members"]) + "</ul>")
    if d["footer"]:
        parts.append(f"<p class='small'>{e(d['footer'])}</p>")
    parts.append(f"<p class='small'>Source repository: <a href='{REPO_URL}'>{REPO_URL}</a></p>")
    parts.append("</body></html>")
    return "\n".join(parts)


def write_pdf(html_doc: str, target: Path) -> None:
    from weasyprint import HTML  # imported lazily so Markdown rendering stays stdlib-only
    # fixed identifier keeps output byte-stable when the data has not changed
    HTML(string=html_doc, base_url=str(ROOT)).write_pdf(target, pdf_identifier=target.stem.encode())


# ----------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=str(trendsdb.DB_PATH))
    ap.add_argument("--no-pdf", action="store_true", help="skip PDF output")
    ap.add_argument("--require-pdf", action="store_true", help="fail if WeasyPrint is missing")
    ap.add_argument("--force-pdf", action="store_true", help="rebuild PDFs even if inputs are unchanged")
    ap.add_argument("--check", action="store_true", help="only verify committed Markdown is up to date")
    args = ap.parse_args()

    conn = trendsdb.connect(args.db)
    slugs = [r["slug"] for r in conn.execute("SELECT slug FROM domains ORDER BY id")]
    if not slugs:
        raise SystemExit("no domains in the database")
    datas = {s: load_domain(conn, s) for s in slugs}
    featured = datas.get(FEATURED) or datas[slugs[0]]

    outputs = {README: readme_markdown(featured, [datas[s]["d"] for s in slugs])}
    for s in slugs:
        outputs[REPORTS / f"{s}.md"] = f"<!-- {GEN_NOTE} -->\n" + domain_markdown(datas[s]).rstrip() + "\n"

    if args.check:
        stale = [str(p.relative_to(ROOT)) for p, txt in outputs.items()
                 if not p.exists() or p.read_text() != txt]
        if stale:
            print("stale generated files:", ", ".join(stale))
            return 1
        print("generated Markdown is up to date")
        return 0

    REPORTS.mkdir(exist_ok=True)
    for p, txt in outputs.items():
        p.write_text(txt)
        print("wrote", p.relative_to(ROOT))

    if not args.no_pdf:
        try:
            import weasyprint  # noqa: F401
        except ImportError:
            if args.require_pdf:
                raise SystemExit("WeasyPrint is required for PDF output (pip install weasyprint)")
            print("warning: WeasyPrint not installed, skipping PDFs", file=sys.stderr)
            return 0
        import hashlib
        import weasyprint
        for s in slugs:
            target = REPORTS / f"{s}.pdf"
            doc = domain_html(datas[s])
            # PDFs embed randomly named font subsets, so they are not byte-stable. A stamp of
            # the HTML input lets us skip regeneration (and a noisy commit) when nothing changed.
            stamp = REPORTS / f".{s}.pdf.sha256"
            digest = hashlib.sha256((doc + weasyprint.__version__).encode()).hexdigest()
            if target.exists() and stamp.exists() and stamp.read_text().strip() == digest and not args.force_pdf:
                print("unchanged", target.relative_to(ROOT))
                continue
            write_pdf(doc, target)
            stamp.write_text(digest + "\n")
            print("wrote", target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
