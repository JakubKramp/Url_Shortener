from django.test import TestCase
from django.urls import reverse

from url_shortener.models import Url


class UrlShortenerTestCase(TestCase):
    def test_shorten_url(self):
        url = "https://pl.wikipedia.org/wiki/Real_Madryt"
        self.client.post("", data={"original_url": url})

        self.assertEqual(1, Url.objects.count())
        url_obj = Url.objects.get(original_url=url)
        response = self.client.get(
            reverse("url-detail", kwargs={"short_url": url_obj.short_url})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], url)


    def test_create_existing_url(self):
        url = "https://pl.wikipedia.org/wiki/Real_Madryt"
        Url.objects.create(original_url=url)
        self.client.post("", data={"original_url": url})
        self.assertEqual(1, Url.objects.count())

    def test_create_invalid_url(self):
        url = "hts://pl.wikipedia.org/wiki/Real_Madryt"
        response = self.client.post("", data={"original_url": url})

        self.assertEqual(0, Url.objects.count())
        self.assertEqual(response.status_code, 400)

    def test_list_urls(self):
        url = "https://pl.wikipedia.org/wiki/Real_Madryt"
        Url.objects.create(original_url=url)
        response = self.client.get(
            reverse("url-list")
        )
        self.assertEqual(1, Url.objects.count())
        self.assertEqual(response.data[0]['original_url'], url)

