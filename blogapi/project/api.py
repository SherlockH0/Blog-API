from ninja import NinjaAPI

from blogapi.blog.api import comments_router, posts_router

api = NinjaAPI()

api.add_router("/posts", posts_router)
api.add_router("/comments", comments_router)
