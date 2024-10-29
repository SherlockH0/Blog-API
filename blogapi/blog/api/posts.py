from typing import List

from django.db import Error
from django.shortcuts import get_object_or_404
from ninja import ModelSchema, PatchDict, Router
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
            "automatically_answer_comments",
        ]
        fields_optional = [
            "automatic_answer_delay",
            "automatically_answer_comments",
        ]


class PostOut(ModelSchema):
    author: Author

    class Meta:
        model = Post
        fields = "__all__"


# Create


@router.post("", auth=JWTAuth(), response={201: PostOut})
def create_post(request, payload: PostIn):
    post = Post.objects.create(author_id=request.auth.id, **payload.dict())
    return 201, post


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


@router.put("/{post_id}", auth=JWTAuth(), response=PostOut)
def update_post(request, post_id: int, payload: PostIn):
    post = get_object_or_404(Post, id=post_id, author__id=request.auth.id)

    for attr, value in payload.dict().items():
        setattr(post, attr, value)

    post.save()
    return post


@router.patch("/{post_id}", auth=JWTAuth(), response=PostOut)
def update_post_partial(
    request,
    post_id: int,
    payload: PatchDict[PostIn],  # pyright: ignore[reportInvalidTypeArguments]
):
    post = get_object_or_404(Post, id=post_id, author__id=request.auth.id)

    for attr, value in payload.items():
        setattr(post, attr, value)

    post.save()
    return post


# Delete


@router.delete("/{post_id}", auth=JWTAuth(), response={204: None})
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id, author__id=request.auth.id)
    post.delete()
    return 204
