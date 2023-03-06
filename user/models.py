from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.utils import timezone

from referral.models import Referral

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **other_fields):
        if not email:
            raise ValueError("User must have an email")
        if not name:
            raise ValueError("User must have a name")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **other_fields):
        other_fields.setdefault("is_staff", True) 
        user = self.create_user(
            email,
            name,
            password=password,
            **other_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, **other_fields):
        other_fields.setdefault("is_active", True) 
        other_fields.setdefault("is_staff", True) 
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_verified', True)

        user = self.create_user(
            email,
            name,
            password=password,
            **other_fields
        )
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=150)
    
    created_at = models.DateField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # Admin user; Non super-user
    is_superuser = models.BooleanField(default=False) # Superuser
    referred_by = models.ForeignKey(Referral, on_delete=models.SET_NULL, null=True, related_name='referred_by')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['name'] # Email & Password are required by default.

    def get_name(self):
        # The user is identified by their name
        return self.name

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    