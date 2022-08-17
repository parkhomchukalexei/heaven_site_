from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass


class Client(models.Model):
    name = models.CharField(max_length=255, null=True)
    surname = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    login_of = models.CharField(max_length=255, null=True)
    password_of = models.CharField(max_length=255, null=True)
    of_email = models.CharField(max_length=255, null=True)
    of_password_email = models.CharField(max_length=255, null=True)
    paid_account = models.BooleanField()
    login_of_paid_account = models.CharField(max_length=255, null=True)
    password_of_paid_account = models.CharField(max_length=255, null=True)
    email_of_paid_account = models.CharField(max_length=255, null=True)
    password_of_email_paid_account = models.CharField(max_length=255, null=True)
    photo = models.CharField(max_length=255, null=True)
    telegram_photos_link = models.CharField(max_length=255, null=True)



