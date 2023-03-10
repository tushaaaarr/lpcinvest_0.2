# Generated by Django 3.1.7 on 2023-03-01 07:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20230223_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipedrive_jsondata',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 3, 1, 13, 14, 25, 937067)),
        ),
        migrations.AddField(
            model_name='pipedrive_jsondata',
            name='email',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='pipedrive_jsondata',
            name='investment_type',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='pipedrive_jsondata',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='pipedrive_jsondata',
            name='phone',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='pipedrive_jsondata',
            name='property_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='pipedrive_jsondata',
            name='source',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2023, 3, 1, 13, 14, 25, 936063)),
        ),
        migrations.AlterField(
            model_name='constructionupdates',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2023, 3, 1, 13, 14, 25, 930067)),
        ),
        migrations.AlterField(
            model_name='properties',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2023, 3, 1, 13, 14, 25, 869104)),
        ),
    ]
