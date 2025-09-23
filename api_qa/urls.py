from django.urls import path

from api_qa.views import index

app_name = "api_qa"

urlpatterns: list[path] = [
    path("", index, name="index"),
]
