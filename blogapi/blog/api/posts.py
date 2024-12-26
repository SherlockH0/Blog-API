from typing import List

from django.shortcuts import get_object_or_404
from ninja import PatchDict, Query, Router
from ninja.pagination import paginate
from ninja_jwt.authentication import JWTAuth

from blogapi.blog.models import Post
from blogapi.blog.schemas import PostFilterSchema, PostIn, PostOut
from blogapi.blog.services import new_post, update_resource

router = Router()

# Create


@router.post("", auth=JWTAuth(), response={201: PostOut})
def create_post(request, payload: PostIn):
    post = new_post(request.auth.id, payload.dict())
    return 201, post


# Read


@router.get("/{post_id}", response=PostOut)
def get_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    return post


@router.get("", response=List[PostOut])
@paginate
def list_posts(request, filters: Query[PostFilterSchema]):
    posts = Post.objects.all()
    posts = filters.filter(posts)
    return posts


# Update


@router.put("/{post_id}", auth=JWTAuth(), response=PostOut)
def update_post(request, post_id: int, payload: PostIn):
    post = get_object_or_404(Post, id=post_id, author__id=request.auth.id)

    return update_resource(post, payload.dict())


@router.patch("/{post_id}", auth=JWTAuth(), response=PostOut)
def update_post_partial(
    request,
    post_id: int,
    payload: PatchDict[PostIn],  # pyright: ignore[reportInvalidTypeArguments]
):
    post = get_object_or_404(Post, id=post_id, author__id=request.auth.id)

    return update_resource(post, payload)


# Delete


@router.delete("/{post_id}", auth=JWTAuth(), response={204: None})
def delete_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id, author__id=request.auth.id)
    post.delete()
    return 204
