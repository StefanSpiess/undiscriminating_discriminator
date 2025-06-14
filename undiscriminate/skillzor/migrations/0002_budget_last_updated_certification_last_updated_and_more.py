# Generated by Django 5.2.1 on 2025-05-07 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("skillzor", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="budget",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="certification",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="developmentaction",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="employeecertification",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="project",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="skill",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="employeeskill",
            name="last_updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
