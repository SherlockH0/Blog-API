import google.generativeai as genai
from celery import shared_task
from django.conf import settings

from blogapi.blog.models import Comment

genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


@shared_task
def answer_comment(comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    response = model.generate_content(
        settings.AI_QUERY_TEMPLATE.format(
            post_author=post.author,
            post_date=str(post.created),
            post=post.content,
            comment_author=comment.author,
            comment_date=comment.created,
            comment=comment.content,
        )
    )

    Comment.objects.create(
        author=post.author,
        post=post,
        parent_comment=comment,
        content=response.text,
        ai_generated=True,
    )
