from datetime import timedelta

from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=300)
    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    # For the AI auto-answer features
    automaticly_answer_comments = models.BooleanField(default=True)
    authomatic_answer_delay = models.DurationField(default=timedelta(minutes=30))


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "Comment", on_delete=models.SET_NULL, null=True, blank=True
    )

    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    is_blocked = models.BooleanField(default=False)
    is_AI_generated = models.BooleanField(default=False)
