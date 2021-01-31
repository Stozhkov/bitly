from django.db import models
import datetime


class Link(models.Model):
    url = models.CharField(max_length=1000)
    key = models.CharField(max_length=8, unique=True)
    user_id = models.CharField(max_length=1000, default='')
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def delete_old_records(cls, minutes=60):
        cut_off = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        cls.objects.filter(created__lt=cut_off).delete()
