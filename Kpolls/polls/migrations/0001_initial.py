# Generated by Django 3.0.6 on 2020-07-02 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('rem_date', models.DateTimeField(null=True, verbose_name='date removed')),
                ('slug', models.SlugField(unique=True)),
                ('ended', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('prompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Prompt')),
            ],
        ),
    ]
