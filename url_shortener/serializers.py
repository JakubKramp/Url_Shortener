from rest_framework import serializers

from url_shortener.models import Url


class ShortUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ["id", "original_url", "short_url"]
        read_only_fields = ["id", "short_url"]
