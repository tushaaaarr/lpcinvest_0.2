# Generated by Django 3.1.7 on 2023-02-22 15:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20230221_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2023, 2, 22, 20, 45, 14, 538145)),
        ),
        migrations.AlterField(
            model_name='constructionupdates',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2023, 2, 22, 20, 45, 14, 531149)),
        ),
        migrations.AlterField(
            model_name='properties',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2023, 2, 22, 20, 45, 14, 352746)),
        ),
    ]
