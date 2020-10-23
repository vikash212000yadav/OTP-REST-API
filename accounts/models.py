from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(phone=phone)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self.db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class AttendeeManager(BaseUserManager):
    def create_attendee(self, first_name, last_name, phone, password=None):
        if not phone:
            raise ValueError('Attendee must have a phone number')
        if not password:
            raise ValueError('Attendee must have a password')

        attendee_obj = self.model(first_name=first_name, last_name=last_name, phone=phone)
        attendee_obj.set_password(password)
        attendee_obj.save(using=self.db)
        return attendee_obj


class CoordinatorManager(BaseUserManager):
    def create_coordinator(self, first_name, last_name, phone, password=None):
        if not phone:
            raise ValueError('Coordinator must have a phone number')
        if not password:
            raise ValueError('Coordinator must have a password')

        coordinator_obj = self.model(first_name=first_name, last_name=last_name, phone=phone)
        coordinator_obj.set_password(password)
        coordinator_obj.save(using=self.db)
        return coordinator_obj


class ManagerManager(BaseUserManager):
    def create_manager(self, first_name, last_name, phone, password=None):
        if not phone:
            raise ValueError('Manager must have a phone number')
        if not password:
            raise ValueError('Manager must have a password')

        manager_obj = self.model(first_name=first_name, last_name=last_name, phone=phone)
        manager_obj.set_password(password)
        manager_obj.save(using=self.db)
        return manager_obj


class HelpdeskManager(BaseUserManager):
    def create_helpdesk(self, first_name, last_name, phone, password=None):
        if not phone:
            raise ValueError('Helpdesk must have a phone number')
        if not password:
            raise ValueError('Helpdesk must have a password')

        helpdesk_obj = self.model(first_name=first_name, last_name=last_name, phone=phone)
        helpdesk_obj.set_password(password)
        helpdesk_obj.save(using=self.db)
        return helpdesk_obj


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$',
        message="Phone number must be entered in the format: '+918708733948'. Up to 14 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    first_login = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.name:
            return self.name
        else:
            return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Area(object):
    Urban = 'Urban'
    Rural = 'Rural'
    AREA_CHOICES = [
        (Urban, 'Urban'),
        (Rural, 'Rural'),
    ]


class Gender(object):
    Male = 'Male'
    Female = 'Female'
    Trans = 'Trans'
    GENDER_CHOICES = [
        (Male, 'Male'),
        (Female, 'Female'),
        (Trans, 'Trans'),
    ]


class Attendee(User, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    guardian_name = models.CharField(max_length=50)
    area = models.CharField(choices=Area.AREA_CHOICES, max_length=5)
    address1 = models.CharField("House Number", max_length=1024)
    address2 = models.CharField("Street Name", max_length=1024)
    landmark = models.CharField("Landmark", max_length=1024)
    zip_code = models.CharField("ZIP / Postal Code", max_length=12)
    city = models.CharField("City", max_length=1024)
    state = models.CharField("State", max_length=1024)
    country = models.CharField("Country", max_length=1024)
    """phone_regex = RegexValidator(
        regex=r'^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$',
        message="Phone number must be entered in the format: '+918708733948'. Up to 14 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)"""
    gender = models.CharField(choices=Gender.GENDER_CHOICES, max_length=6)
    dob = models.DateField()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'zip_code']

    objects = AttendeeManager()

    def __str__(self):
        return self.first_name


class Coordinator(User, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    guardian_name = models.CharField(max_length=50)
    area = models.CharField(choices=Area.AREA_CHOICES, max_length=5)
    address1 = models.CharField("House Number", max_length=1024)
    address2 = models.CharField("Street Name", max_length=1024)
    landmark = models.CharField("Landmark", max_length=1024)
    zip_code = models.CharField("ZIP / Postal Code", max_length=12)
    city = models.CharField("City", max_length=1024)
    state = models.CharField("State", max_length=1024)
    country = models.CharField("Country", max_length=1024)
    """phone_regex = RegexValidator(
        regex=r'^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$',
        message="Phone number must be entered in the format: '+918708733948'. Up to 14 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)"""
    gender = models.CharField(choices=Gender.GENDER_CHOICES, max_length=6)
    dob = models.DateField()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'zip_code']

    objects = CoordinatorManager()

    def __str__(self):
        return self.first_name


class Manager(User, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    guardian_name = models.CharField(max_length=50)
    area = models.CharField(choices=Area.AREA_CHOICES, max_length=5)
    address1 = models.CharField("House Number", max_length=1024)
    address2 = models.CharField("Street Name", max_length=1024)
    landmark = models.CharField("Landmark", max_length=1024)
    zip_code = models.CharField("ZIP / Postal Code", max_length=12)
    city = models.CharField("City", max_length=1024)
    state = models.CharField("State", max_length=1024)
    country = models.CharField("Country", max_length=1024)
    """phone_regex = RegexValidator(
        regex=r'^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$',
        message="Phone number must be entered in the format: '+918708733948'. Up to 14 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)"""
    gender = models.CharField(choices=Gender.GENDER_CHOICES, max_length=6)
    dob = models.DateField()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'zip_code']

    objects = ManagerManager()

    def __str__(self):
        return self.first_name


class Helpdesk(User, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    guardian_name = models.CharField(max_length=50)
    area = models.CharField(choices=Area.AREA_CHOICES, max_length=5)
    address1 = models.CharField("House Number", max_length=1024)
    address2 = models.CharField("Street Name", max_length=1024)
    landmark = models.CharField("Landmark", max_length=1024)
    zip_code = models.CharField("ZIP / Postal Code", max_length=12)
    city = models.CharField("City", max_length=1024)
    state = models.CharField("State", max_length=1024)
    country = models.CharField("Country", max_length=1024)
    """phone_regex = RegexValidator(
        regex=r'^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$',
        message="Phone number must be entered in the format: '+918708733948'. Up to 14 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)"""
    gender = models.CharField(choices=Gender.GENDER_CHOICES, max_length=6)
    dob = models.DateField()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'zip_code']

    objects = HelpdeskManager()

    def __str__(self):
        return self.first_name


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(
        regex=r'^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$',
        message="Phone number must be entered in the format: '+918708733948'. Up to 14 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of OTP sent')
    validated = models.BooleanField(
        default=False,
        help_text='If it is True, that means user have validate oyp correctly in second API'
    )

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)
