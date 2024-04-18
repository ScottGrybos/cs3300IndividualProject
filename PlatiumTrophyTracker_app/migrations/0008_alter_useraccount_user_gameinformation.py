# Generated by Django 4.2 on 2024-04-18 22:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PlatiumTrophyTracker_app', '0007_alter_trophytracker_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_account', to='PlatiumTrophyTracker_app.user'),
        ),
        migrations.CreateModel(
            name='GameInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=200)),
                ('game_link', models.URLField()),
                ('img_url', models.URLField()),
                ('completion_time', models.CharField(blank=True, max_length=100, null=True)),
                ('rating', models.CharField(blank=True, max_length=100, null=True)),
                ('game_difficulty', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('description', models.TextField()),
                ('user_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlatiumTrophyTracker_app.useraccount')),
            ],
        ),
    ]
