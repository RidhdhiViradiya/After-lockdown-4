from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name="login_register"),
    url(r'^register$', views.register, name="register"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^reset_password/$', PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password_reset"),
    url(r'^reset_password_sent/$', PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    url(r'^reset_password_complete/$', PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
    path('area', views.area_handle, name="area"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
