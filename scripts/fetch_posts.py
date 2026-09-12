#!/usr/bin/env python3
"""Pull the latest posts from the Substack RSS feed into data/posts.json.

Run by .github/workflows/sync-posts.yml on a schedule. Safe to run locally.
Exits non-zero if the feed returns no items so a broken fetch never
overwrites a good file with an empty one.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED = "https://travisknudsen.substack.com/feed"
OUT = Path(__file__).resolve().parent.parent / "data" / "posts.json"
LIMIT = 6


def main() -> int:
    req = urllib.request.Request(FEED, headers={"User-Agent": "consciouscreationtheory.com post sync"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        root = ET.fromstring(resp.read())

    posts = []
    for item in root.findall("./channel/item")[:LIMIT]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue
        pub = item.findtext("pubDate")
        date = parsedate_to_datetime(pub).date().isoformat() if pub else None
        enc = item.find("enclosure")
        posts.append({
            "title": title,
            "subtitle": (item.findtext("description") or "").strip(),
            "url": link,
            "date": date,
            "image": enc.get("url") if enc is not None else None,
        })

    if not posts:
        print("Feed returned no posts; leaving data/posts.json untouched", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"source": FEED, "posts": posts}, indent=2) + "\n")
    print(f"Wrote {len(posts)} posts to {OUT.relative_to(OUT.parent.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
