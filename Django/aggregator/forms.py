from django import forms

from .models import NewsSource


class NewsSourceForm(forms.ModelForm):
    class Meta:
        model = NewsSource
        fields = ('name', 'feed_url', 'max_items', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Source name'}),
            'feed_url': forms.URLInput(attrs={'placeholder': 'https://example.com/feed'}),
            'max_items': forms.NumberInput(attrs={'min': 1, 'max': 50}),
        }
