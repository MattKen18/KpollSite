# Generated by Django 3.0.6 on 2020-07-18 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_delete_recommendation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_recommendation', models.CharField(max_length=500)),
            ],
        ),
    ]
