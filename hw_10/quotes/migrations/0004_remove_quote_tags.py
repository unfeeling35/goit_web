# Generated by Django 5.0.6 on 2024-09-09 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_alter_tag_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='tags',
        ),
    ]