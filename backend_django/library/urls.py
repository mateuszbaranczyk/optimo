from django.urls import include, path
from library.views import BookViewSet, ReservationViewSet, ReserveView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("reserve/", ReserveView.as_view()),
]
