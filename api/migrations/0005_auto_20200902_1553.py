# Generated by Django 3.0.7 on 2020-09-02 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200902_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scraper',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]