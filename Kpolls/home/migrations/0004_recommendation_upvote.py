# Generated by Django 3.0.6 on 2020-07-12 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20200707_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='upvote',
            field=models.IntegerField(default=0),
        ),
    ]
