"""Fetch the latest TLDR Tech and TLDR AI issues and the top Hacker News stories.

Saves text files to news/raw/<today>/ for the news-scout skill to read.
Uses only the Python standard library.

Usage: python scripts/fetch_news.py
"""
import json
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TLDR_EDITIONS = {"tech": "TLDR Tech", "ai": "TLDR AI"}
HN_STORY_COUNT = 30
HEADERS = {"User-Agent": "writer-agent-news-scout/1.0 (personal use)"}


def fetch(url):
    request = Request(url, headers=HEADERS)
    with urlopen(request, timeout=30) as response:
        return response.geturl(), response.read().decode("utf-8", errors="replace")


class TextWithLinks(HTMLParser):
    """Converts HTML to plain text, keeping link URLs in brackets."""

    SKIP = {"script", "style", "noscript", "svg"}
    BLOCK = {"p", "div", "h1", "h2", "h3", "h4", "li", "br", "section", "article"}

    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip_depth = 0
        self.href = None

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
        elif tag == "a":
            self.href = dict(attrs).get("href")
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth:
            self.skip_depth -= 1
        elif tag == "a":
            if self.href and self.href.startswith("http"):
                self.parts.append(f" ({self.href})")
            self.href = None
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip_depth:
            self.parts.append(data)

    def text(self):
        lines = [" ".join(line.split()) for line in "".join(self.parts).splitlines()]
        cleaned = []
        for line in lines:
            if line or (cleaned and cleaned[-1]):
                cleaned.append(line)
        return "\n".join(cleaned).strip()


def save_tldr(out_dir):
    successes = 0
    for slug, name in TLDR_EDITIONS.items():
        try:
            final_url, page = fetch(f"https://tldr.tech/api/latest/{slug}")
            parser = TextWithLinks()
            parser.feed(page)
            content = f"# {name}\nSource: {final_url}\n\n{parser.text()}\n"
            (out_dir / f"tldr-{slug}.md").write_text(content, encoding="utf-8")
            print(f"OK   {name}: {final_url}")
            successes += 1
        except Exception as error:
            print(f"FAIL {name}: {error}")
    return successes


def save_hacker_news(out_dir):
    try:
        _, body = fetch("https://hacker-news.firebaseio.com/v0/topstories.json")
        story_ids = json.loads(body)[:HN_STORY_COUNT]
        lines = ["# Hacker News top stories", "Source: https://news.ycombinator.com", ""]
        for story_id in story_ids:
            _, item_body = fetch(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
            item = json.loads(item_body)
            if not item or item.get("type") != "story":
                continue
            discussion = f"https://news.ycombinator.com/item?id={story_id}"
            lines.append(f"- {item.get('title', '(no title)')}")
            lines.append(f"  Link: {item.get('url', discussion)}")
            lines.append(
                f"  Points: {item.get('score', 0)} | Comments: {item.get('descendants', 0)}"
                f" | Discussion: {discussion}"
            )
        (out_dir / "hacker-news.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"OK   Hacker News: {len(story_ids)} stories checked")
        return 1
    except Exception as error:
        print(f"FAIL Hacker News: {error}")
        return 0


def main():
    out_dir = PROJECT_ROOT / "news" / "raw" / date.today().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    successes = save_tldr(out_dir) + save_hacker_news(out_dir)
    print(f"Saved to {out_dir}")
    if successes == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()