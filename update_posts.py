#!/usr/bin/env python3
"""Refresh posts.json from Stefano's public Substack RSS feed."""

from datetime import timezone
from email.utils import parsedate_to_datetime
import json
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET


FEED_URL = "https://thinkingintext.substack.com/feed"
OUTPUT_PATH = Path(__file__).with_name("posts.json")
MAX_POSTS = 10


def element_text(element: ET.Element, name: str) -> str:
    child = element.find(name)
    return (child.text or "").strip() if child is not None else ""


def fetch_posts() -> list[dict[str, str]]:
    request = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "stefanoviel.github.io RSS updater"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        root = ET.fromstring(response.read())

    posts = []
    for item in root.findall("./channel/item")[:MAX_POSTS]:
        title = element_text(item, "title")
        url = element_text(item, "link")
        published = parsedate_to_datetime(element_text(item, "pubDate"))
        if published.tzinfo is None:
            published = published.replace(tzinfo=timezone.utc)

        if title and url:
            posts.append(
                {
                    "title": title,
                    "url": url,
                    "date": published.astimezone(timezone.utc)
                    .isoformat()
                    .replace("+00:00", "Z"),
                }
            )

    if not posts:
        raise RuntimeError("The Substack feed did not contain any posts")

    return posts


def main() -> None:
    posts = fetch_posts()
    content = json.dumps(posts, ensure_ascii=False, indent=2) + "\n"
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Updated {OUTPUT_PATH.name} with {len(posts)} posts")


if __name__ == "__main__":
    main()
