from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name="food_index"),
    url(r'^details/(?P<id>\d+)/$', views.details, name="DetailPage"),
    url(r'^vendor/$', views.vendor_index, name="food_vendor_index"),
    url(r'^vendor/addmess/$', views.addmess, name="add_mess"),
    path('area', views.area_handle, name="area"),
    path('filter', views.filterdata, name="filter"),
    path('vendor/addmess/area', views.area_handle, name="area_vendor"),
    url(r'^vendor/addmess/submitMess/$', views.submitMess, name="submit_mess"),
    url(r'^vendor/viewmess/$', views.viewmess, name="view_mess"),
    url(r'^vendor/viewfoodtype/$', views.viewfoodtype, name="view_food_types"),
    url(r'^vendor/managestudent/$', views.managestudent, name="food_manage_student"),
    path('vendor/managestudent/delete', views.delete, name="delete_student"),
    url(r'^vendor/payment/$', views.payment, name="payment_food"),
    url(r'^vendor/payment/handlerequest/$', views.handlerequest, name="handle_request_food"),
    url(r'^vendor/managepayment/(?P<rid>\d+)/$', views.managepayment, name="managepayment_food"),
    url(r'^vendor/manageEmail/$', views.manageEmail, name="food_manage_email"),
    path('vendor/manageEmail/send-mail', views.sendEmail, name="food_send_email"),
    url(r'^vendor/addfoodtype/$', views.addfoodtype, name="add_food_type"),
    url(r'^vendor/addfoodtype/submit/$', views.submitType, name="submit_food_type"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
