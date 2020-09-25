# Generated by Django 3.2 on 2020-09-24 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='title')),
                ('critics_consensus', models.TextField(blank=True, null=True, verbose_name='Consenso')),
                ('genre', models.TextField(blank=True, null=True, verbose_name='duration')),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='rating')),
                ('images', models.ImageField(blank=True, null=True, upload_to='movie/images/', verbose_name='images')),
                ('amount_reviews', models.PositiveIntegerField(blank=True, null=True, verbose_name='Amount_reviews')),
                ('approval_percentage', models.PositiveIntegerField(blank=True, null=True, verbose_name='Porcentae')),
            ],
        ),
    ]