from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "HybridCryptography"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('upload/', views.uploadview.as_view(), name='upload'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
