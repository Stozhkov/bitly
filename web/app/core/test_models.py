from django.test import TestCase
from core.models import Link
from django.db.models import CharField, DateTimeField
from datetime import datetime, timedelta


class LinkModelTest(TestCase):

    test_url = 'http://mail.ru'
    test_key_1 = 'Kwivn4E0'
    test_key_2 = 'Kwivn4E2'
    test_user_id = '12f065bd-612f-4cdc-9978-ba0b582b39f1'

    @classmethod
    def setUpTestData(cls):
        Link.objects.create(url=LinkModelTest.test_url,
                            key=LinkModelTest.test_key_1,
                            user_id=LinkModelTest.test_user_id)

        Link.objects.create(url=LinkModelTest.test_url,
                            key=LinkModelTest.test_key_2,
                            user_id=LinkModelTest.test_user_id)

        Link.objects.filter(id=2).update(created=datetime.now() - timedelta(minutes=10))

    def test_url_field_type(self):
        link = Link.objects.get(id=1)
        field = link._meta.get_field('url')
        self.assertTrue(isinstance(field, CharField))

    def test_url_label(self):
        link = Link.objects.get(id=1)
        field_label = link._meta.get_field('url').verbose_name
        self.assertEqual(field_label, 'url')

    def test_url_max_length(self):
        link = Link.objects.get(id=1)
        field_length = link._meta.get_field('url').max_length
        self.assertEqual(field_length, 1000)

    def test_key_field_type(self):
        link = Link.objects.get(id=1)
        field = link._meta.get_field('key')
        self.assertTrue(isinstance(field, CharField))

    def test_key_label(self):
        link = Link.objects.get(id=1)
        field_label = link._meta.get_field('key').verbose_name
        self.assertEqual(field_label, 'key')

    def test_key_max_length(self):
        link = Link.objects.get(id=1)
        field_length = link._meta.get_field('key').max_length
        self.assertEqual(field_length, 8)

    def test_key_unique(self):
        link = Link.objects.get(id=1)
        field_unique = link._meta.get_field('key').unique
        self.assertEqual(field_unique, True)

    def test_user_id_field_type(self):
        link = Link.objects.get(id=1)
        field = link._meta.get_field('user_id')
        self.assertTrue(isinstance(field, CharField))

    def test_user_id_label(self):
        link = Link.objects.get(id=1)
        field_label = link._meta.get_field('user_id').verbose_name
        self.assertEqual(field_label, 'user id')

    def test_user_id_default(self):
        link = Link.objects.get(id=1)
        field_default_value = link._meta.get_field('user_id').default
        self.assertEqual(field_default_value, '')

    def test_created_field_type(self):
        link = Link.objects.get(id=1)
        field = link._meta.get_field('created')
        self.assertTrue(isinstance(field, DateTimeField))

    def test_created_label(self):
        link = Link.objects.get(id=1)
        field_label = link._meta.get_field('created').verbose_name
        self.assertEqual(field_label, 'created')

    def test_created_auto_now_add(self):
        link = Link.objects.get(id=1)
        field_label = link._meta.get_field('created').auto_now_add
        self.assertEqual(field_label, True)

    def test_delete_old_records(self):

        Link.delete_old_records(minutes=5)

        self.assertEqual(Link.objects.filter(id=1).exists(), True, msg='Deleted not old record.')
        self.assertEqual(Link.objects.filter(id=2).exists(), False, msg='Old record not deleted.')


