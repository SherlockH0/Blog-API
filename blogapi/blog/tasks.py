import json
from typing import TypedDict

import google.generativeai as genai
from django.conf import settings
from django.utils.timezone import now

from blogapi.blog.models import BaseResource, Comment

genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def answer_comment(comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    response = model.generate_content(
        settings.AI_COMMENT_QUERY_TEMPLATE.format(
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


class ModerationResult(TypedDict):
    passes_test: bool
    reason: str


def moderate_resource(obj: BaseResource):
    """
    Checks the `obj`'s content field for obscene expressions or words.
    If present, sets the `obj` status field to `Blocked` and adds a reason to the `block_reason` field.
    If the `obj` is clean, sets the `status` field to `Active` and sets the `block_reason` field to an empty string.

    Moderation query for an AI model can be changed using `AI_MODERATION_QUERY_TEMPLATE`
    setting in settings.py
    """
    response = model.generate_content(
        settings.AI_MODERATION_QUERY_TEMPLATE.format(resource=obj.content),
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=ModerationResult
        ),
    )

    results: ModerationResult = json.loads(response.text)

    if results["passes_test"]:
        obj.status = BaseResource.Statuses.ACTIVE
        obj.block_reason = None
    else:
        obj.status = BaseResource.Statuses.BLOCKED
        obj.block_reason = results["reason"]

    obj.last_moderated = now()
    obj.save()
