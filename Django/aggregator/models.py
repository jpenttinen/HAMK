from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class NewsSource(models.Model):
    name = models.CharField(max_length=120, unique=True)
    feed_url = models.URLField(unique=True)
    max_items = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text='Maximum number of news items to show for this source.',
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name
