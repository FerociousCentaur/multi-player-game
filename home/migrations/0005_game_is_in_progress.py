# Generated by Django 4.2.1 on 2023-05-19 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_profile_remove_game_game_opponent_alter_game_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="is_in_progress",
            field=models.BooleanField(default=False),
        ),
    ]
