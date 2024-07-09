from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from user.views import CreateUserView, ManageUserView, LoginUserView

router = routers.DefaultRouter()
router.register("staff", ManageUserView, basename="staff")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
]

app_name = "user"
