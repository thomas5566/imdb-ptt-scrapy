# Generated by Django 3.1 on 2020-09-26 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_star', '0006_pttmovie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='amount_reviews',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='amount_reviews'),
        ),
        migrations.AlterField(
            model_name='pttmovie',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title'),
        ),
    ]
