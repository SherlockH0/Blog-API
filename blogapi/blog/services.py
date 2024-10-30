import django_rq

from blogapi.blog.models import Comment

from .tasks import answer_comment


def new_comment(user_id: int, data: dict) -> Comment:
    comment = Comment.objects.create(
        author_id=user_id,
        **data,
    )

    if comment.post.automatically_answer_comments:
        scheduler = django_rq.get_scheduler("default")
        scheduler.enqueue_in(
            comment.post.automatic_answer_delay, answer_comment, comment.pk
        )

    return comment
