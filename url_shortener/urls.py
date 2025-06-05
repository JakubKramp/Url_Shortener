from rest_framework.routers import SimpleRouter
from url_shortener.views import UrlViewSet

shortener_router = SimpleRouter()

shortener_router.register("", UrlViewSet)
