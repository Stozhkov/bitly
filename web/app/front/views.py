from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from uuid import uuid4

from django.core.cache import cache

from core.models import Link


def main(request):
    response = render(request, 'main.html')

    if 'user_id' in request.COOKIES:
        uuid = request.COOKIES['user_id']
    else:
        uuid = uuid4()

    response.set_cookie('user_id', uuid, max_age=2592000)

    return response


def redirect_to_url(request, key):

    url = cache.get(key)

    if url is None:
        url = str(get_object_or_404(Link, key=key).url)

    if not url.startswith('https') and not url.startswith('http'):
        url = 'http://' + url

    cache.set(key, url, timeout=3600)

    return redirect(url)
