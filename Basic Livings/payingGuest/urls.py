from django.conf import settings
from django.conf.urls import url
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="payingGuest_index"),
    url(r'^details/(?P<id>\d+)/$', views.details, name="DetailPage"),
    url(r'^details/(?P<id>\d+)/book$', views.book, name="book_room"),
    url(r'^vendor/$', views.vendor_index, name="pg_vendor_index"),
    url(r'change-password/$', views.change_password, name="change_password"),
    url(r'^vendor/addrooms/$', views.addrooms, name="addrooms"),
    path('area', views.area_handle, name="area"),
    path('vendor/addrooms/area', views.area_handle, name="area_vendor"),
    path('filter', views.filterdata, name="filter"),
    url(r'^vendor/addrooms/upload_pic/$', views.upload, name="uploadPhotos"),
    url(r'^vendor/payment/$', views.payment, name="payment"),
    url(r'^vendor/payment/handlerequest/$', views.handlerequest, name="handle_request"),
    path('vendor/viewrooms', views.viewrooms, name="viewrooms"),
    path('vendor/viewrooms/update', views.updaterooms, name="updaterooms"),
    path('vendor/managestudent', views.managestudent, name="managestudents"),
    path('vendor/manageappointments', views.manageappointments, name="manageappointments"),
    path('vendor/manageappointments/delete', views.deleteappointment, name="deleteappointment"),
    path('vendor/managestudent/delete', views.delete, name="deletestudent"),
    url(r'^vendor/manageEmail$', views.manageEmail, name="manage_email"),
    path('vendor/manageEmail/send-mail', views.sendEmail, name="sendEmail"),
    url(r'^vendor/managepayment/(?P<rid>\d+)/$', views.managepayment, name="managepayment"),
    path('vendor/area', views.area_handle, name="area"),
    url(r'^vendor/addrooms/submit/$', views.submitRoom, name="submit"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
