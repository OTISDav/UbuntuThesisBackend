# Generated by Django 5.1.5 on 2025-08-01 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("theses", "0005_thesis_document"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="thesis",
            name="file",
        ),
        migrations.AlterField(
            model_name="thesis",
            name="document",
            field=models.FileField(upload_to="documents"),
        ),
    ]
