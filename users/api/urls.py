from django.urls import path
import users
from users.api.viewsets import login_user, logout_user, register_user

app_name = "users"

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]
