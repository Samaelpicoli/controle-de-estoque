# Generated by Django 5.0.7 on 2024-07-10 21:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("estoque", "0003_auto_20240629_1239"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="estoque",
            name="funcionario",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="estoqueitens",
            name="saldo",
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
