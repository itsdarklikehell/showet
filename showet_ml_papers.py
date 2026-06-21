#!/usr/bin/env python3
"""Showet ML Paper Reading List - AI/ML research paper tracking with GitHub integration.

Fetches papers from arXiv/HF, detects associated GitHub repositories, provides daily
summaries, and integrates with Showet for demo-tech crossover research.
"""

from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
import feedparser
import re


@dataclass
class MLPaper:
    """ML Paper representation."""
    title: str
    authors: list[str]
    summary: str
    published: str
    arxiv_id: str
    github_repo: Optional[str] = None
    categories: list[str] = None
    score: float = 0.0


class MLPaperTracker:
    """Track and curate ML research papers."""

    BASE_URL = "http://export.arxiv.org/api/query"
    HF_PAPERS_URL = "https://huggingface.co/papers"
    CACHE_DIR = Path.home() / ".showet" / "papers"
    PAPER_CATEGORIES = [
        "cs.LG",  # Machine Learning
        "cs.AI",  # Artificial Intelligence
        "cs.CV",  # Computer Vision
        "cs.CL",  # Computation and Language
        "cs.HC",  # Human-Computer Interaction
        "eess.IV", # Image and Video Processing
    ]

    # Keywords for demo-relevant papers
    DEMO_KEYWORDS = [
        "real-time", "interactive", "generative", "procedural", "creative",
        "animation", "rendering", "graphics", "neural", "video", "audio"
    ]

    def __init__(self):
        self.cache_dir = self.CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch_daily_papers(self, category: str = "cs.LG") -> list[MLPaper]:
        """Fetch recent papers from arXiv for a category."""
        feed = feedparser.parse(
            f"{self.BASE_URL}?search_query=cat:{category}&sortBy=submittedDate&sortOrder=descending&max_results=20"
        )

        papers = []
        for entry in feed.entries:
            # Extract GitHub repo if mentioned
            github = self._extract_github(entry.summary)

            # Check for demo-relevant keywords
            relevance_score = self._score_for_demos(entry.title + " " + entry.summary)

            paper = MLPaper(
                title=entry.title,
                authors=[a.name for a in entry.authors],
                summary=entry.summary[:500] + "...",
                published=entry.published,
                arxiv_id=entry.id.split("/")[-1],
                github_repo=github,
                categories=[c.term for c in entry.tags] if hasattr(entry, "tags") else [],
                score=relevance_score,
            )
            papers.append(paper)

        # Cache results
        cache_file = self.cache_dir / f"papers_{category}_{datetime.now().strftime('%Y-%m-%d')}.json"
        with open(cache_file, "w") as f:
            json.dump([{
                "title": p.title,
                "authors": p.authors,
                "summary": p.summary,
                "published": p.published,
                "arxiv_id": p.arxiv_id,
                "github_repo": p.github_repo,
                "categories": p.categories,
                "score": p.score,
            } for p in papers], f, indent=2)

        return papers

    def _extract_github(self, text: str) -> Optional[str]:
        """Extract GitHub repo URL from text."""
        patterns = [
            r"github\.com/([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)",
            r"github\.com/([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)/tree",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"https://github.com/{match.group(1)}"
        return None

    def _score_for_demos(self, text: str) -> float:
        """Score paper relevance for demoscene/creative applications."""
        text_lower = text.lower()
        matches = sum(1 for kw in self.DEMO_KEYWORDS if kw in text_lower)
        return min(matches / len(self.DEMO_KEYWORDS), 1.0)

    def get_github_implementations(self, arxiv_id: str) -> list[str]:
        """Find GitHub implementations for a paper."""
        # Search GitHub for papers with this arxiv ID
        search_url = f"https://api.github.com/search/repositories?q={arxiv_id}+in:readme"
        try:
            req = urllib.request.Request(search_url, headers={"Accept": "application/vnd.github.v3+json"})
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode())
            return [item["html_url"] for item in data.get("items", [])[:5]]
        except Exception:
            return []

    def daily_digest(self) -> str:
        """Generate a morning paper digest under 150 words."""
        papers = []
        for cat in ["cs.LG", "cs.AI"]:
            papers.extend(self.fetch_daily_papers(cat))

        # Sort by demo relevance
        papers.sort(key=lambda p: p.score, reverse=True)

        # Top 3 most relevant
        top = papers[:3]

        lines = ["📚 Daily AI Papers Digest\n"]
        for p in top:
            gh = f" | {p.github_repo}" if p.github_repo else ""
            lines.append(f"• {p.title[:60]}... ({p.arxiv_id[:10]}){gh}")
            if p.score > 0.3:
                lines.append(f"  Demo-relevant: {p.score:.0%}")

        return "\n".join(lines)

    def search_papers(self, query: str, max_results: int = 10) -> list[MLPaper]:
        """Search arXiv for specific topics."""
        feed = feedparser.parse(
            f"{self.BASE_URL}?search_query={query}&max_results={max_results}"
        )

        papers = []
        for entry in feed.entries:
            paper = MLPaper(
                title=entry.title,
                authors=[a.name for a in entry.authors],
                summary=entry.summary[:500] + "...",
                published=entry.published,
                arxiv_id=entry.id.split("/")[-1],
                categories=[c.term for c in entry.tags] if hasattr(entry, "tags") else [],
            )
            papers.append(paper)

        return papers


def main() -> int:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Showet ML Paper Reading List",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--digest", "-d", action="store_true", help="Show daily paper digest")
    parser.add_argument("--search", "-s", help="Search papers by topic")
    parser.add_argument("--category", "-c", default="cs.LG", help="arXiv category to fetch")
    parser.add_argument("--brief", "-b", action="store_true", help="Concise output under 150 words")
    args = parser.parse_args()

    tracker = MLPaperTracker()

    if args.digest:
        print(tracker.daily_digest())
    elif args.search:
        papers = tracker.search_papers(args.search)
        for p in papers[:10]:
            print(f"\n📰 {p.title}")
            print(f"   Authors: {', '.join(p.authors[:3])}{'...' if len(p.authors) > 3 else ''}")
            print(f"   {p.summary[:120]}...")
            if p.github_repo:
                print(f"   🔗 {p.github_repo}")
    else:
        # Default: show digest
        print(tracker.daily_digest())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())