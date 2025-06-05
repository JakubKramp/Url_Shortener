import string
from secrets import choice
from typing import Callable
import hashlib

from django.conf import settings


def database_contains(url: str) -> bool:
    from url_shortener.models import Url

    """
    Checks if short url is already in database, to avoid collision
    :param url: Generated short URL
    :return: True if the short URL already exists, False otherwise
    """
    return Url.objects.filter(short_url=url).exists()


def get_short_url(original_url: str) -> Callable:
    """
    Based on settings returns appropriate url shortening function
    :param original_url: Url to be shortened
    :return: Url shortening function
    """
    return (
        get_deterministic_short_url(original_url)
        if settings.DETERMINISTIC
        else get_random_short_url(original_url)
    )


def get_random_short_url(url: str) -> str:
    """
    Simple function for generating short, random strings we use for url shortening.
    we use secrets.choice() because its less predictable than random.choice()
    :param url: Url to be shortened
    :return: Shortened url
    """
    allowed_chars = string.ascii_letters + string.digits

    for _ in range(5):
        short_url = "".join([choice(allowed_chars) for _ in range(settings.URL_LENGTH)])
        if not database_contains(short_url):
            return short_url

    raise Exception("Failed to generate a unique short URL after multiple attempts.")


def get_deterministic_short_url(url: str) -> str:
    """
    Simple function for generating short, deterministic strings we use for url shortening.
    we use md5 algorithm, and take first chunk of length = settings.URL_LENGTH. In case of collision take next chunk.
    :param url: Url to be shortened
    :return: shortened url
    """
    md5_hash = hashlib.md5(url.encode()).hexdigest()
    for i in range(32 // settings.URL_LENGTH):
        short_url = md5_hash[i * settings.URL_LENGTH : (i + 1) * settings.URL_LENGTH]
        if not database_contains(short_url):
            return short_url
