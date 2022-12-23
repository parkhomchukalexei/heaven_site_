from django.db import models


# from users.models import Client,AbstractUser

# Create your models here.


class OnlyFansTable(models.Model):
    date = models.DateField(default='01-01-2022', null=False, auto_now=False)
    table_type = models.BooleanField(default=False)
    client = models.ForeignKey('users.Client', on_delete=models.DO_NOTHING)
    operator = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)


class TableData(models.Model):
    date = models.DateField()
    data = models.FloatField(null=True)
    data_type = models.TextField(null=False)
    table = models.ForeignKey('OnlyFansTable', on_delete=models.CASCADE)
