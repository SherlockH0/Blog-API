from http import HTTPStatus
from typing import List

from django.shortcuts import get_object_or_404
from ninja import ModelSchema, PatchDict, Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from blogapi.blog.api.author import Author
from blogapi.blog.models import Post

router = Router()


class PostIn(ModelSchema):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "automatic_answer_delay",
            "automaticly_answer_comments",
        ]


class PostOut(ModelSchema):
    author: Author

    class Meta:
        model = Post
        fields = "__all__"


# Create


@router.post("", auth=JWTAuth())
def create_post(request, payload: PostIn):
    post = Post.objects.create(author_id=request.auth.id, **payload.dict())
    return {"id": post.pk}


# Read


@router.get("/{post_id}", response=PostOut)
def get_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    return post


@router.get("", response=List[PostOut])
def get_posts(request):
    queryset = Post.objects.all()
    return queryset


# Update


@router.put("/{post_id}", auth=JWTAuth())
def update_post(request, post_id: int, payload: PostIn):
    post = get_object_or_404(Post, id=post_id)

    if post.author.id != request.auth.id:
        return HTTPStatus.FORBIDDEN

    for attr, value in payload.dict().items():
        setattr(post, attr, value)

    post.save()
    return {"success": True}


@router.patch("/{post_id}", auth=JWTAuth())
def update_post_partial(
    request,
    post_id: int,
    payload: PatchDict[PostIn],  # pyright: ignore[reportInvalidTypeArguments]
):
    post = get_object_or_404(Post, id=post_id)

    if post.author.id != request.auth.id:
        raise HttpError(HTTPStatus.FORBIDDEN, "Only post's author can change it")

    for attr, value in payload.items():
        setattr(post, attr, value)

    post.save()
    return {"success": True}


# Delete


@router.delete("/{post_id}")
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return {"success": True}
