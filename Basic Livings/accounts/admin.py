from django.conf.urls import url
from django.shortcuts import render
from django.utils.html import format_html
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group
from admin_object_actions.admin import ModelAdminObjectActionsMixin
from rangefilter.filter import DateRangeFilter
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Area, City, Packages, PublicQueries
from .forms import CustomUserChangeForm, CustomUserCreationForm
# Register your models here.


admin.site.site_header = "'Basic Livings' Administration"
admin.site.site_title = " Administration Controls"
admin.site.index_title = "Database Tables"


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    
    return Wrapper


class CustomUserAdmin(ModelAdminObjectActionsMixin, UserAdmin):
    #
    # def get_urls(self):
    #     urls = super(CustomUserAdmin, self).get_urls()
    #     my_urls = [url(r'^users/report/$', self.my_view, name="print_view")]
    #     return my_urls + urls
    #
    # def my_view(self, request):
    #     # custom view which should return an HttpResponse
    #     obj = self.get_queryset(request)
    #     return render(request, 'admin/print.html')
    #
    change_list_template = 'admin/change_list.html'

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     # extra_context['osm_data'] = self.get_osm_info()
    #     return super().change_view(
    #         request, object_id, form_url, extra_context=extra_context,
    #     )
    
    def print_view(self, request, queryset):
        obj = queryset
        name = "user"
        return render(request, 'admin/print.html', {'obj': obj, 'name': name})
    print_view.short_description = format_html('<span>Print</span>')
    
    list_display = ('email', 'first_name', 'last_name', 'phone', 'address', 'is_active',)
    list_filter = (('area_id', RelatedDropdownFilter),
                            ('last_login', DateRangeFilter),
                            ('date_joined', DateRangeFilter),
                            ('is_active', custom_titled_filter('Active Status')),
                            ('is_pgVendor', custom_titled_filter('Paying Guest Vendor Status')),
                            ('is_foodVendor', custom_titled_filter('Mess Vendor Status')),
                            ('is_student', custom_titled_filter('Student Status')))
    list_per_page = 10
    fieldsets = (
        # (None, {'fields': ('password')} ),
        ('Personal info', {'fields': ('first_name', 'last_name', 'password', 'email', 'gender', 'address', 'phone','area_id')}),
        ('Permissions', {'fields': ('is_pgVendor', 'is_foodVendor', 'is_student', 'is_superuser', 'is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')
    filter_horizontal = ()

    def set_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        if count == 1:
            self.message_user(request, "Marked {} User Inactive".format(count))
        else:
            self.message_user(request, "Marked {} Users Inactive".format(count))
    set_inactive.short_description = "Mark Selected as Inactive !!"

    def set_active(self, request, queryset):
        count = queryset.update(is_active=True)
        if count == 1:
            self.message_user(request, "Marked {} User Active".format(count))
        else:
            self.message_user(request, "Marked {} Users Active".format(count))
    set_active.short_description = "Mark Selected as Active !!"

    actions = {'set_inactive', 'set_active', 'print_view'}


class PackagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'is_active']
    ordering = ['title', 'price']
    list_filter = [('is_active', custom_titled_filter('Active Status')), ('price', DropdownFilter), ('duration', custom_titled_filter('Months'))]
    list_per_page = 10
    
    def set_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        if count == 1:
            self.message_user(request, "Marked {} Package Inactive".format(count))
        else:
            self.message_user(request, "Marked {} Packages Inactive".format(count))
    set_inactive.short_description = "Mark Selected as Inactive !!"

    def set_active(self, request, queryset):
        count = queryset.update(is_active=True)
        if count == 1:
            self.message_user(request, "Marked {} Package Active".format(count))
        else:
            self.message_user(request, "Marked {} Packages Active".format(count))
    set_active.short_description = "Mark Selected as Active !!"

    actions = {'set_inactive', 'set_active', 'print_view'}


class CityAdmin(admin.ModelAdmin):
    list_display = ['city_name']
    ordering = ['city_name']
    search_fields = ['city_name']
    list_per_page = 10


class AreaAdmin(admin.ModelAdmin):

    list_display = ['area_name', 'city']
    list_filter = (('city_id', RelatedDropdownFilter), )
    ordering = ['area_name']
    search_fields = ('area_name', )
    list_per_page = 10


class PublicQueriesAdmin(admin.ModelAdmin):
    list_display = ['sender', 'subject', 'date_posted']
    ordering = ('sender', 'date_posted')
    list_filter = (('date_posted', DateRangeFilter), )
    list_per_page = 10

    def print_view(self, request, queryset):
        obj = queryset
        name = "queries"
        return render(request, 'admin/print.html', {'obj': obj, 'name': name})

    print_view.short_description = format_html('<span>Print</span>')
    
    actions = ['print_view']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Packages, PackagesAdmin)
admin.site.register(PublicQueries, PublicQueriesAdmin)
admin.site.unregister(Group)
