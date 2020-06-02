from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, first_name, last_name, email, password, gender, address, phone, is_pgVendor, is_foodVendor, is_student, area_id, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email,
                          gender=gender, address=address, phone=phone, is_pgVendor=is_pgVendor,
                          is_foodVendor=is_foodVendor, is_student=is_student, area_id=area_id)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password, gender="Male", address="", phone="", **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault('is_pgVendor', False)
        extra_fields.setdefault('is_foodVendor', False)
        extra_fields.setdefault('is_student', False)
        extra_fields.setdefault('area_id', None)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(first_name, last_name, email, password, gender, address, phone, **extra_fields)
