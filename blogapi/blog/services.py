import json

from django.utils.timezone import now
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from blogapi.blog.models import Comment


def new_comment(user_id: int, data: dict) -> Comment:
    comment = Comment.objects.create(
        author_id=user_id,
        **data,
    )

    clocked, _ = ClockedSchedule.objects.get_or_create(
        clocked_time=now() + comment.post.automatic_answer_delay
    )

    if comment.post.automatically_answer_comments:
        PeriodicTask.objects.create(
            clocked=clocked,
            name=f"Answer comment {comment.pk}",
            task="blogapi.blog.tasks.answer_comment",
            args=json.dumps([comment.pk]),
            one_off=True,
        )

    return comment
