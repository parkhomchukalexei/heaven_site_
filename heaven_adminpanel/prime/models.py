from django.db import models

# Create your models here.


class PrimeTable(models.Model):
    date = models.DateField(default='01-01-2023', null=False, auto_now=False)
    client = models.ForeignKey('users.Client', on_delete=models.DO_NOTHING)
    operator = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)
    account_id = models.CharField(null=False, max_length=50)


class TableData(models.Model):
    date = models.DateField()
    data = models.FloatField(null=True)
    table = models.ForeignKey('PrimeTable', on_delete=models.CASCADE)