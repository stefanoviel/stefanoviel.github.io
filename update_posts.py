#!/usr/bin/env python3
"""Refresh posts.json from Stefano's public Substack RSS feed."""

from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET


FEED_URL = "https://thinkingintext.substack.com/feed"
OUTPUT_PATH = Path(__file__).with_name("posts.json")
MAX_POSTS = 10
EXCERPT_LENGTH = 320
CONTENT_TAG = "{http://purl.org/rss/1.0/modules/content/}encoded"


class ParagraphParser(HTMLParser):
    """Collect readable paragraph text from a Substack post body."""

    def __init__(self) -> None:
        super().__init__()
        self.paragraphs: list[str] = []
        self.current: list[str] | None = None
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "p" and self.current is None:
            self.current = []
        if self.current is not None:
            classes = dict(attrs).get("class", "") or ""
            if self.ignored_depth:
                self.ignored_depth += 1
            elif "footnote-anchor" in classes:
                self.ignored_depth = 1

    def handle_data(self, data: str) -> None:
        if self.current is not None and not self.ignored_depth:
            self.current.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.ignored_depth:
            self.ignored_depth -= 1
            return
        if tag == "p" and self.current is not None:
            paragraph = " ".join("".join(self.current).split())
            if paragraph:
                self.paragraphs.append(paragraph)
            self.current = None


def text(element: ET.Element, name: str) -> str:
    child = element.find(name)
    return (child.text or "").strip() if child is not None else ""


def opening_excerpt(item: ET.Element) -> str:
    """Return the opening two paragraphs, shortened at a word boundary."""
    parser = ParagraphParser()
    parser.feed(text(item, CONTENT_TAG))
    paragraphs = [
        paragraph
        for paragraph in parser.paragraphs
        if not paragraph.startswith(("Thanks for reading", "Subscribe for"))
    ]
    excerpt = " ".join(paragraphs[:2]) or text(item, "description")
    if len(excerpt) <= EXCERPT_LENGTH:
        return excerpt
    shortened = excerpt[: EXCERPT_LENGTH + 1].rsplit(" ", 1)[0]
    return f"{shortened}…"


def fetch_posts() -> list[dict[str, str]]:
    request = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "stefanoviel.github.io RSS updater"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        root = ET.fromstring(response.read())

    posts = []
    for item in root.findall("./channel/item")[:MAX_POSTS]:
        enclosure = item.find("enclosure")
        published = datetime.strptime(
            text(item, "pubDate"), "%a, %d %b %Y %H:%M:%S %Z"
        ).replace(tzinfo=timezone.utc)
        posts.append(
            {
                "title": text(item, "title"),
                "description": opening_excerpt(item),
                "url": text(item, "link"),
                "date": published.isoformat().replace("+00:00", "Z"),
                "image": enclosure.get("url", "") if enclosure is not None else "",
            }
        )
    return posts


def main() -> None:
    posts = fetch_posts()
    OUTPUT_PATH.write_text(
        json.dumps(posts, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {OUTPUT_PATH.name} with {len(posts)} posts")


if __name__ == "__main__":
    main()
