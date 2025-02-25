import uuid
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models

class CustomBaseUserManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        if not email: 
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        superuser = self.model(email=email, role=User.Role.ADMIN, is_staff=True, is_superuser=True, **other_fields)
        superuser.set_password(password)
        superuser.save()
        return superuser

class User(AbstractBaseUser, PermissionsMixin): 
    """
    custom User model extending AbstractUser.
    stores shared fields for all users and handles user authentication.
    """
    class Role(models.TextChoices): 
        ADMIN = "ADMIN", "Server Administrator"
        STANDARD = "STANDARD", 'Standard User'
        MERCHANT = 'MERCHANT', 'Merchant Administrator'
        LOGISTICS = 'LOGISTICS', 'Logistics Administrator'
        DRIVER = 'DRIVER', 'Logistics Driver'

    base_role = Role.ADMIN 
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=True, null=True)
    firebase_uid = models.CharField(max_length=255, blank=True, null=True, unique=True)
    is_staff = models.BooleanField(default=False);
    is_superuser = models.BooleanField(default=False);
    creation_date = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=50, choices=Role.choices, null=False, blank=False, editable=False)

    objects = CustomBaseUserManager()

    USERNAME_FIELD = 'email'

    def is_standard(self): 
        return self.role == self.Role.STANDARD
    def is_merchant(self): 
        return self.role == self.Role.MERCHANT
    def is_logistics(self): 
        return self.role == self.Role.LOGISTICS
    def is_driver(self): 
        return self.role == self.Role.DRIVER


    def save(self, *args, **kwargs):
        """
        Assigns the base role on first save.
        """
        if not self.pk:
            self.role = getattr(self.__class__, "base_role", self.Role.STANDARD)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.role})"

    class Meta: 
        verbose_name = "User"
        verbose_name_plural = "All Users"


class StandardUserManager(models.Manager): 
    def get_queryset(self, *args, **kwargs): 
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STANDARD)

class StandardUser(User): 
    base_role = User.Role.STANDARD

    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    users = StandardUserManager()

    class Meta: 
        verbose_name = "Standard User"

class MerchantAdministratorManager(models.Manager): 
    def get_queryset(self, *args, **kwargs): 
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.MERCHANT)

class MerchantAdministrator(User): 
    base_role = User.Role.MERCHANT

    business_name = models.CharField(max_length=50, blank=False)

    merchants = MerchantAdministratorManager()

    class Meta: 
        verbose_name = "Merchant Administrator"

class LogisticsAdministratorManager(models.Manager): 
    def get_queryset(self, *args, **kwargs): 
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.LOGISTICS)

class LogisticsAdministrator(User): 
    base_role = User.Role.LOGISTICS

    logistics_name = models.CharField(max_length=50, blank=False)

    logistics = LogisticsAdministratorManager()

    class Meta: 
        verbose_name = "Logistics Administrator"


class DriverManager(models.Manager): 
    def get_queryset(self, *args, **kwargs): 
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.DRIVER)

class Driver(User): 
    base_role = User.Role.DRIVER

    driver_first_name = models.CharField(max_length=50, blank=False)
    driver_last_name = models.CharField(max_length=50, blank=False)
    logistics_name = models.ForeignKey(LogisticsAdministrator, on_delete=models.CASCADE, related_name="drivers")

    drivers = DriverManager()

    class Meta: 
        verbose_name = "Logistics Driver"
