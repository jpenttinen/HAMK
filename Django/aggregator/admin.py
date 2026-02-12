from django.contrib import admin

from .models import NewsSource


@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'feed_url', 'max_items', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'feed_url')
