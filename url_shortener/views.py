from django.http import HttpResponseRedirect
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from url_shortener.models import Url
from url_shortener.serializers import ShortUrlSerializer


class UrlViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Url.objects
    lookup_field = "short_url"
    serializer_class = ShortUrlSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return HttpResponseRedirect(instance.original_url)

    def create(self, request, *args, **kwargs):
        original_url = request.data.get("original_url")

        if not original_url:
            return Response({"error": "original_url is required"}, status=400)

        try:
            instance = Url.objects.get(original_url=original_url)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Url.DoesNotExist:
            return super().create(request, *args, **kwargs)
