from typing import List

from django.shortcuts import get_object_or_404
from ninja import ModelSchema, PatchDict, Router
from ninja_jwt.authentication import JWTAuth

from blogapi.blog.api.author import Author
from blogapi.blog.models import Comment

router = Router()


class CommentIn(ModelSchema):
    class Meta:
        model = Comment
        fields = ["content", "parent_comment"]


class CommentOut(ModelSchema):
    author: Author

    class Meta:
        model = Comment
        fields = "__all__"


# Create


@router.post("")
def create_comment(request, payload: CommentIn):
    comment = Comment.objects.create(**payload.dict())
    return {"id": comment.pk}


# Read


@router.get("/{comment_id}", response=CommentOut)
def get_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    return comment


@router.get("", response=List[CommentOut])
def get_comments(request):
    queryset = Comment.objects.all()
    return queryset


# Update


@router.put("/{comment_id}")
def update_comment(request, comment_id: int, payload: CommentIn):
    comment = get_object_or_404(Comment, id=comment_id)
    for attr, value in payload.dict().items():
        setattr(comment, attr, value)
    comment.save()
    return {"success": True}


@router.patch("/{comment_id}")
def update_comment_partial(
    request,
    comment_id: int,
    payload: PatchDict[CommentIn],  # pyright: ignore[reportInvalidTypeArguments]
):
    comment = get_object_or_404(Comment, id=comment_id)

    for attr, value in payload.items():
        setattr(comment, attr, value)

    comment.save()
    return {"success": True}


# Delete


@router.delete("/{comment_id}")
def delete_comment(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return {"success": True}
