from datetime import timedelta

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models


class Statuses(models.TextChoices):
    ACTIVE = "+", "Active"
    BLOCKED = "-", "Blocked"
    IN_MODERATION = "/", "In moderation"


class Post(models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=300)
    content = models.TextField(
        validators=[
            MinLengthValidator(300, "The post must be at least 300 characters.")
        ]
    )

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    status = models.CharField(  # pyright: ignore
        max_length=1,
        choices=Statuses,  # pyright: ignore
        default=Statuses.IN_MODERATION,
    )

    # For the AI auto-answer features
    automatically_answer_comments = models.BooleanField(default=True)
    automatic_answer_delay = models.DurationField(default=timedelta(minutes=30))

    def __str__(self):
        return f"{self.title} by {self.author}"


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    parent_comment = models.ForeignKey(
        "Comment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    content = models.TextField(
        max_length=600,
        validators=[MinLengthValidator(15, "Enter at least 15 characters.")],
    )

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    status = models.CharField(  # pyright: ignore
        max_length=1,
        choices=Statuses,  # pyright: ignore
        default=Statuses.IN_MODERATION,
    )

    ai_generated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} commented {self.post}"
