# Django News Aggregator

A Django-based news aggregator with:

- Configurable list of news sources
- Configurable max news items per source
- Source management UI (add/edit/delete/activate)
- Aggregated dashboard that displays latest items from active sources

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open:

- `http://127.0.0.1:8000/` for the news dashboard
- `http://127.0.0.1:8000/sources/` for source configuration
- `http://127.0.0.1:8000/admin/` for Django admin

## Example Feed URLs

- `https://feeds.bbci.co.uk/news/rss.xml`
- `https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml`
- `https://www.reddit.com/r/worldnews/.rss`
