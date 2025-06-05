from django.contrib import admin
from django.contrib.admin import ModelAdmin

from url_shortener.models import Url


# Register your models here.
@admin.register(Url)
class UrlAdmin(ModelAdmin):
    fields = [
        "original_url",
        "short_url",
    ]
    list_display = [
        "id",
        "original_url",
        "short_url",
    ]
    readonly_fields = ["short_url"]
