from datetime import date
from typing import List

from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404
from ninja import PatchDict, Query, Router, Schema
from ninja.pagination import paginate
from ninja_jwt.authentication import JWTAuth

from blogapi.blog.models import Comment, Post
from blogapi.blog.schemas import (
    CommentFilterSchema,
    CommentIn,
    CommentOut,
    DailyAnalyticsSchema,
)
from blogapi.blog.services import new_comment

router = Router()


# Create


@router.post("", auth=JWTAuth(), response={201: CommentOut})
def create_comment(request, payload: CommentIn):
    comment = new_comment(request.auth.id, payload.dict())
    return 201, comment


# Read


@router.get("/{comment_id}", response=CommentOut)
def get_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    return comment


@router.get("", response=List[CommentOut])
@paginate
def list_comments(request, filters: Query[CommentFilterSchema]):
    comments = Comment.objects.all()
    comments = filters.filter(comments)
    return comments


# Update


@router.put("/{comment_id}", auth=JWTAuth(), response=CommentOut)
def update_comment(request, comment_id: int, payload: CommentIn):
    comment = get_object_or_404(Comment, id=comment_id, author__id=request.auth.id)
    for attr, value in payload.dict().items():
        setattr(comment, attr, value)
    comment.save()

    return comment


@router.patch("/{comment_id}", auth=JWTAuth(), response=CommentOut)
def update_comment_partial(
    request,
    comment_id: int,
    payload: PatchDict[CommentIn],  # pyright: ignore[reportInvalidTypeArguments]
):
    comment = get_object_or_404(Comment, id=comment_id, author__id=request.auth.id)

    for attr, value in payload.items():
        setattr(comment, attr, value)

    comment.save()
    return comment


# Delete


@router.delete("/{comment_id}", auth=JWTAuth(), response={204: None})
def delete_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id, author__id=request.auth.id)
    comment.delete()
    return 204


# Comment analytics


@router.get(
    "/daily_breakdown/{post_id}",
    response=list[DailyAnalyticsSchema],
)
def daily_breakdown(request, post_id: int, date_from: date, date_to: date):
    post = get_object_or_404(Post, id=post_id)

    comments = post.comment_set

    query = (
        comments.filter(created__date__gte=date_from, created__date__lte=date_to)
        .values(date=F("created__date"))
        .annotate(
            active=Count("id", filter=Q(status=Post.Statuses.ACTIVE)),
            blocked=Count("id", filter=Q(status=Post.Statuses.BLOCKED)),
        )
    )

    return list(query)
