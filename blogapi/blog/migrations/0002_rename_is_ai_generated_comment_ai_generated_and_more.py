# Generated by Django 5.1.2 on 2024-10-28 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='is_AI_generated',
            new_name='ai_generated',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='is_blocked',
            new_name='blocked',
        ),
    ]