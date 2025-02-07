from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Blog(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
