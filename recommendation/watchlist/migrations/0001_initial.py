# Generated by Django 5.0.3 on 2024-03-24 00:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watched', models.BooleanField(default=False)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='users.profile')),
            ],
            options={
                'unique_together': {('profile', 'movie')},
            },
        ),
    ]
