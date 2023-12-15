# Generated by Django 4.2.8 on 2023-12-09 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_feature"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vote",
            name="story",
        ),
        migrations.AddField(
            model_name="feature",
            name="story_points",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="feature",
            name="voted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="vote",
            name="feature",
            field=models.ForeignKey(
                default=None, on_delete=django.db.models.deletion.CASCADE, related_name="votes", to="core.feature"
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="Story",
        ),
    ]