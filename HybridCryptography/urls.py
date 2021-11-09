from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "HybridCryptography"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('upload/', views.uploadView.as_view(), name='upload'),
    path('download/',views.downloadView.as_view(),name="download"),
    path('success/', views.successView.as_view(), name="success"),
    path('download_file/',views.download_file,name="download_file"),
    path('email_send/',views.email_send,name="email_send"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
