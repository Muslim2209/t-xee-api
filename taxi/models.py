from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from taxi.managers import TaxiUserManager


class TaxiUser(AbstractBaseUser, PermissionsMixin):
    DRIVER = 'driver'
    PASSENGER = 'passenger'
    USER_TYPES = [(DRIVER, 'Driver'), (PASSENGER, 'Passenger')]
    phone_number = PhoneNumberField(_('phone number'), unique=True)
    user_type = models.CharField(max_length=24, choices=USER_TYPES)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('status'),
        default=True,
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return str(self.phone_number)

    objects = TaxiUserManager()


class Passenger(models.Model):
    CASH = 'cash'
    CARD = 'card'
    CORPORATE_ACCOUNT = 'corporate_account'
    PAYMENT_TYPES = (
        (CASH, 'Cash'),
        (CARD, 'Card'),
        (CORPORATE_ACCOUNT, 'Corporate'),
    )
    user = models.OneToOneField(TaxiUser, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=120, choices=PAYMENT_TYPES)

    def __str__(self):
        return 'Passenger {}'.format(self.user.phone_number)


class Driver(models.Model):
    user = models.OneToOneField(TaxiUser, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=64)
    car_color = models.CharField(max_length=64)
    car_number = models.CharField(max_length=24)

    def __str__(self):
        return 'Driver {}'.format(self.user.phone_number)


class Order(models.Model):
    NEW = 'new'
    ACCEPTED = 'accepted'
    ARRIVED = 'arrived'
    IN_CAR = 'in_car'
    FINISHED = 'finished'
    ORDER_STATUSES = [
        (NEW, 'New'),
        (ACCEPTED, 'Order Accepted'),
        (ARRIVED, 'Driver arrived'),
        (IN_CAR, 'Passenger in the car'),
        (FINISHED, 'Trip finished'),
    ]
    passenger = models.ForeignKey(Passenger, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    start_point = models.CharField(max_length=224)
    destination_point = models.CharField(max_length=224)
    order_status = models.CharField(max_length=120, choices=ORDER_STATUSES)
