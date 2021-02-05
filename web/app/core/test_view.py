from django.test import TestCase
from core.models import Link
from http.cookies import SimpleCookie
from django.core.cache import cache


class ViewTest(TestCase):

    user_id = 'qwertyid'

    @classmethod
    def setUpTestData(cls):
        Link.objects.create(url='test1.ru', key='testkey1', user_id=ViewTest.user_id)
        Link.objects.create(url='test2.ru', key='testkey2', user_id=ViewTest.user_id)

    def test_link_list_without_cookie(self):

        response = self.client.get('/api/links/')
        self.assertEqual(response.status_code, 400)

    def test_link_list_get_request_with_cookie(self):
        self.client.cookies = SimpleCookie({'user_id': self.user_id})
        response = self.client.get('/api/links/')
        self.assertEqual(response.status_code, 200)

    def test_link_list_post_request(self):
        test_url = 'test3.ru'
        test_key = 'testkey3'

        self.client.cookies = SimpleCookie({'user_id': self.user_id})

        data = {'url': test_url,
                'key': test_key,
                'user_id': self.user_id}

        response = self.client.post('/api/links/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 201, msg='Wrong status code.')
        self.assertEqual(Link.objects.filter(key=test_key).exists(), True, msg='New record not saved in DB.')
        self.assertEqual(cache.get(test_key), test_url, msg='Wrong cache data in cache')

    def test_link_list_post_request_bad_keys(self):
        bad_keys = ['api', 'admin']
        self.client.cookies = SimpleCookie({'user_id': self.user_id})
        for key in bad_keys:
            data = {'url': 'test4.ru',
                    'key': key,
                    'user_id': self.user_id}
            response = self.client.post('/api/links/', data=data, content_type='application/json')
            self.assertEqual(response.status_code, 400, msg=f'Wrong status code with bad key "{key}"')

    def test_link_list_delete_request(self):

        test_url = 'test7.ru'
        test_key = 'testkey7'

        data = {'url': test_url,
                'key': test_key,
                'user_id': self.user_id}

        self.client.cookies = SimpleCookie({'user_id': self.user_id})
        self.client.post('/api/links/', data=data, content_type='application/json')

        data['id'] = Link.objects.filter(key=test_key).first().id

        response = self.client.delete('/api/links/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200, msg='Wrong status code.')
        self.assertFalse(Link.objects.filter(id=data['id']).exists(), msg='Data not delete from DB.')
        self.assertIsNone(cache.get(test_key), msg='Data not delete from cache.')


