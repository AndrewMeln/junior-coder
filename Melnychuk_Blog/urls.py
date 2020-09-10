from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.views.generic.base import TemplateView
from blog.views import Register


urlpatterns = [
    path('register/success/', TemplateView.as_view(
        template_name="registration/success.html"), name='register-success'),
    path('register/', Register.as_view(), name='register'),
    path('admin/', admin.site.urls, name='admin'),
    path('', include('django.contrib.auth.urls')),
    path('', include('blog.urls', namespace='blog')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)