from datetime import date, datetime
from typing import Optional

from ninja import FilterSchema, ModelSchema, Schema

from blogapi.blog.models import Comment, Post


class Author(Schema):
    id: int
    username: str


class CommentIn(Schema):
    post_id: int
    content: str
    parent_comment_id: Optional[int] = None


class CommentOut(ModelSchema):
    author: Author

    class Meta:
        model = Comment
        fields = "__all__"


class CommentFilterSchema(FilterSchema):
    created: Optional[datetime] = None
    author: Optional[int] = None
    post: Optional[int] = None


class DailyAnalyticsSchema(Schema):
    date: date
    blocked: int
    active: int


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


class PostFilterSchema(FilterSchema):
    created: Optional[datetime] = None
    author: Optional[int] = None
