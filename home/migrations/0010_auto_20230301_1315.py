# Generated by Django 3.1.7 on 2023-03-01 07:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20230301_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2023, 3, 1, 13, 15, 48, 524338)),
        ),
        migrations.AlterField(
            model_name='constructionupdates',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2023, 3, 1, 13, 15, 48, 517341)),
        ),
        migrations.AlterField(
            model_name='pipedrive_jsondata',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 3, 1, 13, 15, 48, 525336)),
        ),
        migrations.AlterField(
            model_name='properties',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2023, 3, 1, 13, 15, 48, 452895)),
        ),
    ]
