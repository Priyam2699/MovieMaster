# Generated by Django 4.0.3 on 2022-04-07 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_alter_movie_trailer'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='price',
            field=models.IntegerField(default=100),
        ),
    ]
