from __future__ import annotations

import html
from typing import Any, Iterable

import feedparser
from django.utils.html import strip_tags

from .models import NewsSource


def _normalize_entry(entry: Any) -> dict[str, str]:
    title = html.unescape(entry.get('title', 'Untitled')).strip()
    link = entry.get('link', '#')
    summary = entry.get('summary') or entry.get('description') or ''
    clean_summary = html.unescape(strip_tags(summary)).strip()
    if len(clean_summary) > 280:
        clean_summary = clean_summary[:277].rstrip() + '...'
    published = entry.get('published') or entry.get('updated') or 'No publication date'

    return {
        'title': title or 'Untitled',
        'link': link,
        'summary': clean_summary,
        'published': published,
    }


def fetch_news_for_sources(sources: Iterable[NewsSource]) -> list[dict[str, Any]]:
    results = []

    for source in sources:
        try:
            parsed = feedparser.parse(
                source.feed_url,
                request_headers={
                    'User-Agent': 'DjangoNewsAggregator/1.0 (+https://localhost)',
                    'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml',
                },
            )

            entries = list(getattr(parsed, 'entries', []))[: source.max_items]
            items = [_normalize_entry(entry) for entry in entries]
            bozo_exception = getattr(parsed, 'bozo_exception', None)

            error = None
            if getattr(parsed, 'bozo', 0) and not items:
                if bozo_exception:
                    error = f'Could not parse feed: {bozo_exception}'
                else:
                    error = 'Could not parse feed.'

            results.append(
                {
                    'source': source,
                    'feed_title': parsed.feed.get('title', source.name),
                    'items': items,
                    'error': error,
                }
            )
        except Exception as exc:  # pragma: no cover - network/remote failures are dynamic
            results.append(
                {
                    'source': source,
                    'feed_title': source.name,
                    'items': [],
                    'error': f'Failed to fetch feed: {exc}',
                }
            )

    return results
