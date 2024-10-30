# Generated by Django 5.1.2 on 2024-10-30 10:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_automaticly_answer_comments_post_automatically_answer_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='blocked',
        ),
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('+', 'Active'), ('-', 'Blocked'), ('/', 'In moderation')], default='/', max_length=1),
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('+', 'Active'), ('-', 'Blocked'), ('/', 'In moderation')], default='/', max_length=1),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=600, validators=[django.core.validators.MinLengthValidator(15, 'Enter at least 15 characters.')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(300, 'The post must be at least 300 characters.')]),
        ),
    ]