from django.contrib import admin
from django.urls import include, path

from .api import api

urlpatterns = [
    path("api/", api.urls),  # pyright: ignore[reportArgumentType, reportCallIssue]
    path("admin/", admin.site.urls),
    path("django-rq/", include("django_rq.urls")),
]
