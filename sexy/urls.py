from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name = 'home'),

    #Login and register url
    path('login', views.login_view, name = 'login'),
    path('register1', views.register1, name = 'register1'),
    path('register2', views.register2, name = 'register2'),
    path('register3', views.register3, name = 'register3'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)