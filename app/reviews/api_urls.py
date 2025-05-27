from rest_framework.routers import DefaultRouter
from reviews.views import (
    CountryViewSet,
    ManufacturerViewSet,
    CarViewSet,
    CommentViewSet,
)
from reviews.views import ObtainAuthTokenCustom, CustomAPIRootView
from django.urls import path

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'cars', CarViewSet, basename='car')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', CustomAPIRootView.as_view(), name='api-root'),  # ← корень
    path('token/', ObtainAuthTokenCustom.as_view(), name='api-token'),  # ← токен
]

urlpatterns += router.urls