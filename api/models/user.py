import uuid
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models

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
