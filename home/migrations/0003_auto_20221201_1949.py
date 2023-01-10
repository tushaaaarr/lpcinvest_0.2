# Generated by Django 3.1.7 on 2022-12-01 14:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20221201_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyCities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='properties',
            name='city',
        ),
        migrations.AlterField(
            model_name='properties',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2022, 12, 1, 19, 49, 50, 304985)),
        ),
    ]
