from blogapi.blog.models import Comment


def new_comment(user_id: int, data: dict) -> Comment:
    comment = Comment.objects.create(
        author_id=user_id,
        **data,
    )
    return comment
