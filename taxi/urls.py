from django.urls import path, include
from rest_framework.routers import DefaultRouter
from taxi import views

router = DefaultRouter()
router.register(r'users', views.TaxiUserViewSet)
router.register(r'drivers', views.DriverViewSet)
router.register(r'passengers', views.PassengerViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
