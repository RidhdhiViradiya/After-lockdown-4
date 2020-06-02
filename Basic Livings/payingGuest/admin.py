from django.shortcuts import render
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.contrib import admin
from payingGuest.models import Room
from django.contrib.admin import DateFieldListFilter
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


class RoomAdmin(admin.ModelAdmin):

    def print_view(self, request, queryset):
        obj = queryset
        name = "rooms"
        return render(request, 'admin/print.html', {'obj': obj, 'name': name})

    print_view.short_description = format_html('<span>Print</span>')

    def set_expired(self, request, queryset):
        count = 0
        add = 0
        for row in queryset:
            date_str = row.get_exp_date()
            if date_str.date() > datetime.today().date():
                Room.objects.filter(room_id=row.getRoomId()).update(is_active=True)
                add += 1
            else:
                Room.objects.filter(room_id=row.getRoomId()).update(is_active=False)
                count += 1
        if count == 1 or count == 0:
            self.message_user(request, "Marked {} Room Inactive".format(count))
        else:
            self.message_user(request, "Marked {} Rooms Inactive".format(count))
        if add == 1 or add == 0:
            self.message_user(request, "Marked {} Room Active".format(add))
        else:
            self.message_user(request, "Marked {} Rooms Active".format(add))
    set_expired.short_description = "Check Expired Rooms !!"
    
    def set_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        if count == 1:
            self.message_user(request, "Marked {} Room Inactive".format(count))
        else:
            self.message_user(request, "Marked {} Rooms Inactive".format(count))
    set_inactive.short_description = "Mark Selected as Inactive !!"

    def set_active(self, request, queryset):
        count = queryset.update(is_active=True)
        if count == 1:
            self.message_user(request, "Marked {} Room Active".format(count))
        else:
            self.message_user(request, "Marked {} Rooms Active".format(count))
    set_active.short_description = "Mark Selected as Active !!"

    actions = {'set_inactive', 'set_active', 'set_expired', 'print_view'}

    def image_tags(self, obj):
        return format_html('<img src="{}" width="250px" height="150px" />'.format(obj.image_path.url))

    image_tags.short_description = 'Image'
    
    list_display = ('room_id', 'user_id', 'address', 'days_since_posted', 'is_active')
    ordering = ['room_id', 'user_id', 'address', ]
    readonly_fields = ('image_tags',)
    list_filter = [
                   ('date_posted', DateRangeFilter),
                   ('exp_date', DateRangeFilter),
                   ('area_id', RelatedDropdownFilter),
                   ('is_active', custom_titled_filter('Active Status')),
                   ]
    list_per_page = 10


class Appointment(admin.ModelAdmin):
    list_display = ('sender', 'email', 'date_posted')
    ordering = ('appoint_id', 'date_posted', )
    list_filter = (('date_posted', DateRangeFilter),
                   ('user_id', RelatedDropdownFilter),
                   ('room_id', RelatedDropdownFilter))
    search_fields = ('sender', 'email')
    list_per_page = 10


class RoomImagesAdminModal(admin.ModelAdmin):
    def image_tags(self, obj):
        return format_html('<img src="{}" width="50px" height="50px" />'.format(obj.image_path.url))
    
    image_tags.short_description = 'Image'
    
    list_filter = (('room_id', RelatedDropdownFilter), )
    list_display = ('image_id', 'room_id', 'image_tags', )
    readonly_fields = ('image_tag', )
    ordering = ('image_id', )
    list_per_page = 10


class RoomVendorPaymentModal(admin.ModelAdmin):
    
    def print_view(self, request, queryset):
        obj = queryset
        name = "rpayments"
        return render(request, 'admin/print.html', {'obj': obj, 'name': name})

    print_view.short_description = format_html('<span>Print</span>')
    
    actions = ['print_view']
    
    list_display = ('order_id', 'user_id')
    list_filter = (('user_id', RelatedDropdownFilter), ('date_of_payment', DateRangeFilter))
    search_fields = ('order_id', )
    list_per_page = 10
    
    
class RoomBookingsModal(admin.ModelAdmin):
    
    def print_view(self, request, queryset):
        obj = queryset
        name = "rbookings"
        return render(request, 'admin/print.html', {'obj': obj, 'name': name})

    print_view.short_description = format_html('<span>Print</span>')
    
    actions = ['print_view']
    
    list_display = ('booking_id','room_id', 'user_id', 'booking_date')
    list_per_page = 10
    ordering = ('booking_id', )
    list_filter = (('user_id', RelatedDropdownFilter), ('room_id', RelatedDropdownFilter), ('booking_date', DateRangeFilter), )
    
    
admin.site.register(Amenities)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomImage, RoomImagesAdminModal)
admin.site.register(RoomsVendorPayment, RoomVendorPaymentModal)
admin.site.register(RoomsBookingDetail, RoomBookingsModal)
admin.site.register(RoomAppointments, Appointment)