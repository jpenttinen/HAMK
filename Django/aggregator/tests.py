from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import NewsSource


class SourceManagementTests(TestCase):
    def test_can_create_news_source(self):
        response = self.client.post(
            reverse('aggregator:source_list'),
            data={
                'name': 'BBC',
                'feed_url': 'https://feeds.bbci.co.uk/news/rss.xml',
                'max_items': 7,
                'is_active': True,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        source = NewsSource.objects.get(name='BBC')
        self.assertEqual(source.max_items, 7)


class DashboardTests(TestCase):
    @patch('aggregator.services.feedparser.parse')
    def test_dashboard_limits_items_per_source(self, mock_parse):
        NewsSource.objects.create(
            name='Example',
            feed_url='https://example.com/feed',
            max_items=1,
            is_active=True,
        )

        mock_parse.return_value = SimpleNamespace(
            feed={'title': 'Example Feed'},
            entries=[
                {
                    'title': 'First item',
                    'link': 'https://example.com/1',
                    'summary': 'Summary one',
                    'published': 'Today',
                },
                {
                    'title': 'Second item',
                    'link': 'https://example.com/2',
                    'summary': 'Summary two',
                    'published': 'Today',
                },
            ],
            bozo=0,
            bozo_exception=None,
        )

        response = self.client.get(reverse('aggregator:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First item')
        self.assertNotContains(response, 'Second item')
