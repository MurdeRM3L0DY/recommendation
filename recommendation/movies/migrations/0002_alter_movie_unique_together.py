# Generated by Django 5.0.3 on 2024-03-24 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='movie',
            unique_together={('title', 'release_date')},
        ),
    ]