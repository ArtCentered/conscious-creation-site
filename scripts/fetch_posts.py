#!/usr/bin/env python3
"""Pull the latest posts from Substack into data/posts.json.

Run by .github/workflows/sync-posts.yml on a schedule. Safe to run locally.
Tries the RSS feed first, then Substack's JSON API. Exits non-zero, with a
GitHub Actions error annotation explaining why, if neither works, so a broken
fetch never overwrites a good file with an empty one.
"""
import json
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

SITE = "https://travisknudsen.substack.com"
FEED = f"{SITE}/feed"
API = f"{SITE}/api/v1/posts?limit=6&offset=0"
OUT = Path(__file__).resolve().parent.parent / "data" / "posts.json"
LIMIT = 6
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, application/json, text/html;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch(url: str, attempts: int = 3) -> bytes:
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            body = e.read()[:200].decode("utf-8", "replace").replace("\n", " ")
            last = f"HTTP {e.code} from {url}: {body}"
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__} from {url}: {e}"
        time.sleep(2 * (i + 1))
    raise RuntimeError(last or f"no response from {url}")


def from_feed(raw: bytes) -> list[dict]:
    root = ET.fromstring(raw)
    posts = []
    for item in root.findall("./channel/item")[:LIMIT]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue
        pub = item.findtext("pubDate")
        enc = item.find("enclosure")
        posts.append({
            "title": title,
            "subtitle": (item.findtext("description") or "").strip(),
            "url": link,
            "date": parsedate_to_datetime(pub).date().isoformat() if pub else None,
            "image": enc.get("url") if enc is not None else None,
        })
    return posts


def from_api(raw: bytes) -> list[dict]:
    posts = []
    for p in json.loads(raw)[:LIMIT]:
        title = (p.get("title") or "").strip()
        link = p.get("canonical_url") or ""
        if not title or not link:
            continue
        posts.append({
            "title": title,
            "subtitle": (p.get("subtitle") or "").strip(),
            "url": link,
            "date": (p.get("post_date") or "")[:10] or None,
            "image": p.get("cover_image"),
        })
    return posts


def main() -> int:
    errors = []
    posts: list[dict] = []
    for name, url, parse in (("feed", FEED, from_feed), ("api", API, from_api)):
        try:
            posts = parse(fetch(url))
            if posts:
                print(f"Fetched {len(posts)} posts via {name}")
                break
            errors.append(f"{name} returned no posts")
        except Exception as e:  # noqa: BLE001
            errors.append(str(e))

    if not posts:
        msg = " | ".join(errors)
        print(f"::error::Substack fetch failed. {msg}")
        print("Leaving data/posts.json untouched", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"source": SITE, "posts": posts}, indent=2) + "\n")
    print(f"Wrote {len(posts)} posts to {OUT.relative_to(OUT.parent.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
