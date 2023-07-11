from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Entry(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=2000)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self) -> str:
        return self.title