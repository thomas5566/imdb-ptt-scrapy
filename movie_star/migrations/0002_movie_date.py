# Generated by Django 3.2 on 2020-09-24 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_star', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='date',
            field=models.TextField(blank=True, null=True, verbose_name='date'),
        ),
    ]