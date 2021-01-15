from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("new_account", views.UserCreate.as_view(), name="account-new_account-api"),
]
