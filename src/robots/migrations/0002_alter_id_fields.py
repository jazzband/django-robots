# Generated by Django 3.2 on 2021-09-23 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("robots", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rule",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="url",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
