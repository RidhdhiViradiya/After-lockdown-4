from django.conf.urls import url
from django.conf.urls.static import static

from . import views, settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    url(r'^$', views.index, name="main_home"),
    path('logout/', views.logout, name="LoggedOut"),
    url(r'^update_user/$', views.update_user, name="update_user"),
    path('admin/', admin.site.urls),
    path('food/', include('food.urls')),
    path('payingGuest/', include('payingGuest.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
