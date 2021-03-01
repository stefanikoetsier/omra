# Generated by Django 3.1.7 on 2021-03-01 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song_rater', '0006_rating_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, 'bad'), (2, 'not so good'), (3, 'mediocre'), (4, 'very good'), (5, 'perfect')]),
        ),
    ]