from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


# Create your models here.

class Users(models.Model):
    userdata = models.TextField(max_length=500, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.added_by.profile.userdata, filename)


class Post(models.Model):
    body = models.TextField(max_length=500)
    date = models.DateField(default=datetime.date.today)
    post_image = models.FileField(blank=True, upload_to=user_directory_path)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Comments(models.Model):
    comment = models.TextField(max_length=500)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)


class Likes(models.Model):
    user_liked = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Users.objects.create(user=instance)
    instance.profile.save()
