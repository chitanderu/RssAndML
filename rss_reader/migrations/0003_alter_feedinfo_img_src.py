# Generated by Django 4.0.4 on 2023-03-08 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss_reader', '0002_feedinfo_category_feedinfo_expert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedinfo',
            name='img_src',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
