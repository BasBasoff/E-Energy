# Generated by Django 3.1.4 on 2021-02-09 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210209_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='id_adapters',
        ),
        migrations.AddField(
            model_name='device',
            name='id_adapters',
            field=models.ManyToManyField(to='app.Adapters'),
        ),
        migrations.RemoveField(
            model_name='device',
            name='id_devices',
        ),
        migrations.AddField(
            model_name='device',
            name='id_devices',
            field=models.ManyToManyField(to='app.Devices'),
        ),
    ]
