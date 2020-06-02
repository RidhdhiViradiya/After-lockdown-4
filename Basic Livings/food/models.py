from django.db import models
from datetime import datetime
from django.utils.html import format_html
from accounts.models import User, Packages, Area, City
# Create your models here.
from django.conf import settings


class Tiffin_types(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True, null=False)
    # contains types like 2Dabbas, 3Dabbas, 4Dabbas, etc....

    class Meta:
        db_table = 'tiffin_types'
        verbose_name = "Tiffin Types"
        verbose_name_plural = "Tiffin Types"

    def __str__(self):
        return self.type_name

    def get_tiffin_id(self):
        return str(self.type_id)


def upload_path_handler(instance, filename):
    return "mess/images/user{id}/mess-{id2}/{file}".format(id=instance.user_id, id2=instance.mess_name, file=filename)


class Mess(models.Model):
    mess_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    mess_name = models.CharField(max_length=250, null=False)
    address = models.CharField(max_length=500, null=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, db_column='city')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, db_column='area')
    date_posted = models.DateTimeField(default=datetime.today())
    image_path = models.ImageField(upload_to=upload_path_handler, default="", blank=False, null=False)
    is_active = models.BooleanField(default=False, null=False)
    exp_date = models.DateTimeField(blank=False, default=datetime.today())

    class Meta:
        db_table = 'mess'
        verbose_name = "Mess"
        verbose_name_plural = "Mess"

    def image_tag(self):
        return format_html('<img src="{}" width="250px" height="150px" />'.format(self.image_path.url))

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    
    def get_exp_date(self):
        return self.exp_date

    def getmess_id(self):
        return self.mess_id

    def __str__(self):
        return "%s - %s" % (self.mess_id, self.mess_name)

    def get_mess_id(self):
        return "%s" % self.mess_id

    def get_mess_name(self):
        return self.mess_name


categories = [
    ('Veg', 'Veg'),
    ('Non-Veg', 'Non-Veg'),
    ('Semi Non-Veg', 'Semi Non-Veg'),
]


def upload_food_type(instance, filename):
    return "mess/images/user{id}/mess-{id2}/food_types/{file}".format(id=instance.mess_id.user_id,id2=instance.mess_id.mess_name, file=filename)


class Food_types(models.Model):
    food_id = models.AutoField(primary_key=True)
    mess_id = models.ForeignKey(Mess, on_delete=models.CASCADE, db_column='mess_id')
    title = models.CharField(max_length=100, null=False, blank=False, default="")
    tiffin_id = models.ForeignKey(Tiffin_types, on_delete=models.CASCADE, db_column='tiffin_id')
    description = models.CharField(max_length=2048, null=False)
    price = models.PositiveIntegerField(default=0, null=False, blank=False)
    category = models.CharField(max_length=20, choices=categories, default='Veg')
    image_path = models.ImageField(default="", upload_to=upload_food_type, null=False)
    is_active = models.BooleanField(null=False, default=True)
    # include the types of tiffin each mess provides

    class Meta:
        db_table = 'food_types'
        verbose_name = "Food Types"
        verbose_name_plural = "Food Types"

    def __str__(self):
        return "%s %s" % (self.food_id, self.mess_id.get_mess_name())
    
    def get_title(self):
        return self.title


class Mess_bookings(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,  on_delete=models.CASCADE, db_column='user_id')
    mess_id = models.ForeignKey(Mess,  on_delete=models.CASCADE, db_column='mess_id')
    food_id = models.ForeignKey(Food_types, on_delete=models.CASCADE, db_column='food_id', default="")
    booking_date = models.DateTimeField(blank=False, default=datetime.today())
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'mess_bookings'
        verbose_name = "Mess Bookings"
        verbose_name_plural = "Mess Bookings"
        
    def __str__(self):
        return "User: " + self.user_id.get_full_name() + " Booking Number: " + str(self.booking_id)


class MessVendorPayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    mess_id = models.ForeignKey(Mess,  on_delete=models.CASCADE, db_column='mess_id')
    package_id = models.ForeignKey(Packages,  on_delete=models.CASCADE, db_column='package_id')
    date_of_payment = models.DateTimeField(blank=False, default=datetime.today())
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="user_id", default=None)
    order_id = models.CharField(null=False, default="", max_length=30)

    class Meta:
        db_table = 'mess_vendor_payment'
        verbose_name = "Mess Payments"
        verbose_name_plural = "Mess Payments"

    def __str__(self):
        return "Order Id: {}".format(self.order_id)