# Generated by Django 5.1.5 on 2025-02-01 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_user_connections"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="connection_requests",
            field=models.ManyToManyField(
                blank=True, related_name="requested_connections", to="users.user"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="connections",
            field=models.ManyToManyField(
                blank=True, related_name="connected_users", to="users.user"
            ),
        ),
    ]
