from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import LoginUserView, RegisterUserView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet),

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
]
