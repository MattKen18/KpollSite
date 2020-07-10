# Generated by Django 3.0.6 on 2020-07-02 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Idolranking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank_votes', models.CharField(default=0, max_length=200)),
                ('idol', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song', models.CharField(max_length=200)),
                ('artist', models.CharField(max_length=200)),
            ],
        ),
    ]
