from django.test import TestCase
from django.urls import reverse

from core.models import Link
from http.cookies import SimpleCookie
from django.core.cache import cache


class ViewTest(TestCase):

    user_id = 'qwertyid'

    @classmethod
    def setUpTestData(cls):
        Link.objects.create(url='http://0.0.0.0:8000', key='testkey9', user_id=ViewTest.user_id)

    def test_main_view(self):
        resp = self.client.get(reverse('main_page'))
        request = self.client.get('/')

        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(resp, 'main.html')

    def test_main_view_without_cookies(self):
        self.client.get('/')
        cookies_keys = self.client.cookies.keys()

        self.assertTrue('user_id' in cookies_keys, msg='Not set COOKIES "user_id". Then new user come in.')

    def test_main_view_with_cookies(self):
        test_user_id = '152dd7ab-fc61-4f8e-8d8d-cf1fe89a0908'

        self.client.cookies = SimpleCookie({'user_id': test_user_id})
        resp = self.client.get('/')

        self.assertEqual(resp.client.cookies['user_id'].value, test_user_id)

    def test_redirect_to_url_view(self):
        test_key = 'testkey9'
        test_url = 'http://0.0.0.0:8000'
        resp = self.client.get(f'/{test_key}/')

        self.assertRedirects(resp, test_url, status_code=302, target_status_code=302)
        self.assertEqual(cache.get(test_key), test_url, msg='Wrong cache data in cache')








