from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from reviews.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('reviews.api_urls')),  # Подключаем api_urls с роутером
    path('', IndexView.as_view(), name='index'),
]