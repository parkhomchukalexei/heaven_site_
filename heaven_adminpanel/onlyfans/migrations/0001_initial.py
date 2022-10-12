# Generated by Django 4.0.6 on 2022-07-28 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_remove_client_email_remove_client_login_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlyFansTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('fp', models.BooleanField(default=False)),
                ('fp_data', models.FloatField(null=True)),
                ('op', models.BooleanField(default=False)),
                ('op_data', models.FloatField(null=True)),
                ('pp', models.BooleanField(default=False)),
                ('pp_data', models.FloatField(null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.client')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]