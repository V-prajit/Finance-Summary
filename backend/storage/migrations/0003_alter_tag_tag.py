# Generated by Django 5.0.7 on 2024-08-19 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_alter_adminrules_tag_alter_customrules_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
