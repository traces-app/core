import uuid
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models

'''
class Role(models.Model): 
    ROLES = [
        ('STANDARD', 'Standard'),
        ('MERCHANT', 'Merchant'),
        ('LOGISTICS', 'Logistics'),
    ]
    name = models.CharField(max_length=20, choices=ROLES, unique=True)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        return self.create_user(email=email, password=password, first_name=first_name, last_name=last_name, is_staff=True, is_superuser=True, **other_fields)

    def create_user(self, email, first_name, last_name, password, **other_fields):
        if not email: 
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    custom User model extending AbstractUser.
    stores shared fields for all users and handles user authentication.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    creation_date = models.DateTimeField(default=timezone.now)
    firebase_uid = models.CharField(max_length=255, blank=True, null=True, unique=True)
    roles = models.ManyToManyField(Role, related_name='users')
    is_staff = models.BooleanField(default=False);
    is_superuser = models.BooleanField(default=False);

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self): 
        return self.email 

'''

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

    base_role = Role.ADMIN 
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    firebase_uid = models.CharField(max_length=255, blank=True, null=True, unique=True)
    is_staff = models.BooleanField(default=False);
    is_superuser = models.BooleanField(default=False);
    creation_date = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=50, choices=Role.choices, null=False, blank=False, editable=False)

    objects = CustomBaseUserManager()

    USERNAME_FIELD = 'email'

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
