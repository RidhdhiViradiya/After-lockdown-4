from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import CheckConstraint, Q, F
# Create your models here.
from django.utils.html import format_html


def upload_path_handler(instance, filename):
    return "payingGuest/images/user{id3}/room-{id2}/{file}".format(id3=instance.room_id.user_id, id2=instance.room_id.getRoomId(), file=filename)


def upload_path_handler2(instance, filename):
    return "payingGuest/images/user{id3}/{file}".format(id3=instance.getUserId(), file=filename)


class Amenities(models.Model):
    amenities_id = models.AutoField(primary_key=True)
    amenities_name = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        db_table = 'amenities'
        verbose_name = "Amenities"
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.amenities_name


class Room(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Both', 'Both')
    )
    room_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="user_id")
    address = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=200, null=False, default="Room for You")
    no_of_beds = models.PositiveIntegerField(default=0, null=False, blank=False)
    vacant_beds = models.PositiveIntegerField(default=0, null=False, blank=False)
    rent_per_bed = models.PositiveIntegerField(default=0, null=False, blank=False)
    deposit = models.PositiveIntegerField(default=0, null=True, blank=True)
    available_from = models.DateTimeField(blank=False, null=False)
    image_path = models.ImageField(upload_to=upload_path_handler2, default="")
    amenities = models.CharField(max_length=500, default="", null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, blank=False, null=False)
    area_id = models.ForeignKey('accounts.Area', on_delete=models.CASCADE, db_column="area_id", db_index=True)
    special_instruction = models.CharField(max_length=400, blank=True, null=True)
    date_posted = models.DateTimeField(default=datetime.today())
    exp_date = models.DateTimeField(default=datetime.today())
    is_active = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'rooms'
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    # def __str__(self):
    #     return 'User: ' + self.user_id.get_full_name() + "\n  Address: " + self.address

    def __str__(self):
        return str(self.room_id)

    def getUserId(self):
        return self.user_id.getuser_id()

    def getRoomId(self):
        return self.room_id

    def getAddress(self):
        return self.address
    
    def get_exp_date(self):
        return self.exp_date

    def get_is_active(self):
        return self.is_active
    
    def set_is_active(self, status):
        self.is_active = status
    
    def image_tag(self):
        return format_html('<img src="{}" width="250px" height="150px" />'.format(self.image_path.url))

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    
    @property
    def days_since_posted(self):
        return (datetime.today().date() - self.date_posted.date()).days


class RoomImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, db_column="room_id")
    image_path = models.ImageField(upload_to=upload_path_handler, default="")

    class Meta:
        db_table = 'room_images'
        verbose_name = "Room Image"
        verbose_name_plural = "Room Images"

    def __str__(self):
        # return "User: " + str(self.room_id.getUserId()) + " Room: " + str(self.room_id.getRoomId())
        return str(self.room_id)
    
    def image_tag(self):
        if self.image_path:
            return format_html('<img src="{}" width="250px" height="150px" />'.format(self.image_path.url))
        
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class RoomsVendorPayment(models.Model):
    pay_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="user_id")
    room_id = models.ForeignKey(Room,  on_delete=models.CASCADE, db_column="room_id")
    amount = models.FloatField(null=False, blank=False)
    date_of_payment = models.DateTimeField(default=datetime.today())
    order_id = models.CharField(null=False, default="", max_length=30)

    class Meta:
        db_table = 'rooms_vendor_payment'
        verbose_name = "Room Payment"
        verbose_name_plural = "Rooms Payments"

    def __str__(self):
        return "User: " + self.user_id.get_full_name() + "Payment Number: " + str(self.pay_id)


class RoomsBookingDetail(models.Model):
    booking_id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, db_column="room_id")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="user_id")
    booking_date = models.DateTimeField(default=datetime.today())
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'rooms_booking_details'
        verbose_name = "Room Booking"
        verbose_name_plural = "Room Bookings"

    def __str__(self):
        return "User: " + self.user_id.get_full_name() + " Booking Number: " + str(self.booking_id)


class RoomAppointments(models.Model):
    appoint_id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=1024, null=False, blank=False)
    comment = models.CharField(max_length=600, null=False, blank=False)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, db_column="room_id")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="user_id")
    date_posted = models.DateTimeField(default=datetime.today())
    
    def __str__(self):
        return "Sender: " + self.sender
    
    class Meta:
        db_table = 'room_appointments'
        verbose_name = "Room Appointment"
        verbose_name_plural = "Room Appointments"
