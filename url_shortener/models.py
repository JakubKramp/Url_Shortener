from django.db import models

from shortener.models import TimeStampedModel
from shortener.utils import get_short_url


class Url(TimeStampedModel):
    """
    In the future consider removing urls created by anonymous users after certain amount of time
    """

    original_url = models.URLField(blank=False, null=False, unique=True)
    short_url = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = get_short_url(self.original_url)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.original_url} shortened to {self.short_url}"
