from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from blogapi.blog.api import comments_router, posts_router
from blogapi.users.api import router as users_router

api = NinjaExtraAPI()

api.add_router("posts", posts_router, tags=["Posts"])
api.add_router("comments", comments_router, tags=["Comments"])
api.add_router("users", users_router, tags=["Users"])

api.register_controllers(NinjaJWTDefaultController)
