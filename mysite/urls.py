from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("solver.urls")),
    path("admin/", admin.site.urls),
]