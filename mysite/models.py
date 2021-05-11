from django.db import models
from django.contrib.auth.models import User

class Mood(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.status

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, default='不願意透漏身份的人')
    message = models.TextField(null=False)
    del_pass = models.CharField(max_length=10)
    pub_time = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.message





class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.PositiveIntegerField(default=160)
    male = models.BooleanField(default=False)
    website = models.URLField(null=True)

    def __str__(self):
        return self.user.username