from django.shortcuts import render
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.contrib import admin
from accounts.admin import CustomUserAdmin
from accounts.models import User
from datetime import datetime
from rangefilter.filter import DateRangeFilter

from .models import *
# Register your models here.


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    
    return Wrapper


class MessModel(admin.ModelAdmin):
    
    def print_view(self, request, queryset):
        obj = queryset
        name = "mess"
        return render(request, 'admin/print.html', {'obj': obj, 'name': name})

    print_view.short_description = format_html('<span>Print</span>')
    
    def set_inactive(self, request, queryset):
        count = 0
        add = 0
        for row in queryset:
            date_str = row.get_exp_date()
            if date_str.date() > datetime.today().date():
                Mess.objects.filter(mess_id=row.getmess_id()).update(is_active=True)
                add += 1
            else:
                Mess.objects.filter(mess_id=row.getmess_id()).update(is_active=False)
                count += 1
        if count == 1 or count == 0:
            self.message_user(request, "Marked {} Mess Inactive".format(count))
        else:
            self.message_user(request, "Marked {} Mess Inactive".format(count))
        if add == 1 or add == 0:
            self.message_user(request, "Marked {} Mess Active".format(add))
        else:
            self.message_user(request, "Marked {} Mess Active".format(add))
    
    set_inactive.short_description = "Check Expired Mess !!"
    
    actions = {'set_inactive', 'print_view'}
    
    list_display = ('mess_id', 'mess_name', 'address', 'is_active', )
    readonly_fields = ('image_tag',)
    list_filter = (('user_id', RelatedDropdownFilter),
                   ('area', RelatedDropdownFilter),
                   ('date_posted', DateRangeFilter),
                   ('exp_date', DateRangeFilter),
                   ('is_active', custom_titled_filter('Active Status')),
                   )
    
    ordering = ['mess_id', 'mess_name', 'address']
    list_per_page = 15


class FoodTypesModel(admin.ModelAdmin):
    def image_tags(self, obj):
        return format_html('<img src="{}" width="150px" height="250px" />'.format(obj.image_path.url))

    image_tags.short_description = 'Image'
    readonly_fields = ('image_tags', )
    list_display = ('food_id', 'mess_id', 'description', 'price', 'is_active')
    ordering = ('mess_id', 'price')
    search_fields = ('description', )
    list_filter = (('mess_id', RelatedDropdownFilter), ('category', ChoiceDropdownFilter), 'is_active')
    
    def set_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        if count == 1:
            self.message_user(request, "Marked {} Food Type Inactive".format(count))
        else:
            self.message_user(request, "Marked {} Food Types Inactive".format(count))
    set_inactive.short_description = "Mark Selected as Inactive !!"

    def set_active(self, request, queryset):
        count = queryset.update(is_active=True)
        if count == 1:
            self.message_user(request, "Marked {} Food Type Active".format(count))
        else:
            self.message_user(request, "Marked {} Food Types Active".format(count))
    set_active.short_description = "Mark Selected as Active !!"

    actions = {'set_inactive', 'set_active'}
    list_per_page = 15


class TiffinTypes(admin.ModelAdmin):
    list_display = ('type_name', 'is_active')
    list_filter = (('is_active', custom_titled_filter('Active Status')),)
    list_per_page = 15


class MessBookingAdmin(admin.ModelAdmin):
    
    def print_view(self, request, queryset):
        obj = queryset
        name = "mbookings"
        return render(request, 'admin/print.html', {'obj': obj, 'name': name})

    print_view.short_description = format_html('<span>Print</span>')
    
    actions = ['print_view']
    list_display = ('booking_id', 'user_id', 'booking_date')
    list_filter = ('is_active', ('booking_date', DateRangeFilter))
    ordering = ('booking_id', )
    list_per_page = 15

    
class MessVendorPaymentAdmin(admin.ModelAdmin):
    
    def print_view(self, request, queryset):
        obj = queryset
        name = "mpayments"
        return render(request, 'admin/print.html', {'obj': obj, 'name': name})

    print_view.short_description = format_html('<span>Print</span>')
    
    actions = ['print_view']
    
    list_display = ('order_id', 'user_id', 'mess_id')
    list_filter = (('user_id', RelatedDropdownFilter), ('date_of_payment', DateRangeFilter))
    search_fields = ('order_id',)
    list_per_page = 15


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Mess, MessModel)
admin.site.register(Tiffin_types, TiffinTypes)
admin.site.register(Food_types, FoodTypesModel)
admin.site.register(Mess_bookings, MessBookingAdmin)
admin.site.register(MessVendorPayment, MessVendorPaymentAdmin)

