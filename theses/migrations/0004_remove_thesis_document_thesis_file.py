# Generated by Django 5.1.5 on 2025-08-01 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("theses", "0003_alter_thesis_document"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="thesis",
            name="document",
        ),
        migrations.AddField(
            model_name="thesis",
            name="file",
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
