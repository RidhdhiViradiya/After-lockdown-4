from django.db import models
from django.core.mail import send_mail
from datetime import datetime
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.core.validators import RegexValidator
# Create your models here.


class PublicQueries(models.Model):
    query_id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=30, null=False)
    email = models.EmailField(max_length=300, null=False)
    subject = models.CharField(max_length=50)
    date_posted = models.DateTimeField(default=datetime.today())
    message = models.CharField(max_length=1024, null=False, blank=False)

    class Meta:
        db_table = "public_queries"
        verbose_name = "Public Query"
        verbose_name_plural = "Public Queries"

    def __str__(self):
        return self.sender


class Packages(models.Model):
    package_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=300, null=False)
    duration = models.PositiveIntegerField(null=False, blank=False)
    price = models.PositiveIntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "packages"
        verbose_name = "Packages"
        verbose_name_plural = "Packages"
        
    def __str__(self):
        return self.title


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'city'
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return str(self.city_name)

    def get_city_name(self):
        return str(self.city_name)


class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=40)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE, db_column='city_id')
    pincode = models.CharField(max_length=6, default="")

    class Meta:
        db_table = 'Area'
        verbose_name = "Area"
        verbose_name_plural = "Areas"

    def __str__(self):
        return self.area_name
    
    def get_area_name(self):
        return self.area_name
    
    @property
    def city(self):
        return self.city_id.city_name


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_LIST = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )
    RegexValid = RegexValidator(regex=r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$', message="Enter valid Phone Number", code="Invalid Phone Number")
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(_('first name'), max_length=30, unique=False, blank=False, null=False)
    last_name = models.CharField(_('last name'), max_length=30, unique=False, blank=True, null=True)
    email = models.EmailField(_('email'), unique=True, null=False, blank=False)
    gender = models.CharField(_('gender'), choices=GENDER_LIST, blank=False, max_length=10, null=False)
    address = models.CharField(_('address'), blank=False, null=False, max_length=200, default="")
    phone = models.CharField(_('phone'), validators=[RegexValid],max_length=10, blank=False, null=False, default="")
    is_pgVendor = models.BooleanField(_('pgVendor'), default=False, blank=False, null=False)
    is_foodVendor = models.BooleanField(_('foodVendor'), default=False, blank=False, null=False)
    is_student = models.BooleanField(_('student'), default=True, blank=False, null=False)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE, db_column='area_id', blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=datetime.today())
    email_verified_at = models.DateTimeField(_('email verified at'), blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    object = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address', 'password']

    def __str__(self):
        return '%s - %s %s' % (self.user_id, self.first_name, self.last_name)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_email(self):
        return self.email

    def short_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def getuser_id(self):
        return self.user_id

    def get_username(self):
        return self.first_name

    def get_phone(self):
        return str(self.phone)

    def get_gender(self):
        return self.gender

    def get_address(self):
        return self.address

    def email_user(self, subject, message, from_email=None, **kwargs):
        #
        # Sends an email to this User.
        #
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

