# account/models.py
from django.db import models
from django.db.models.signals import pre_save
from random import randint
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not password:
            raise ValueError('Superusers must have a password')
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_('Email'))
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # Quyidagi qatorlarni qo'shing yoki mavjud bo'lsa o'zgartiring
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # O'ziga xos related_name
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # O'ziga xos related_name
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.full_name or self.email

    def __str__(self):
        return self.email

class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.PositiveIntegerField()
    is_used = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

def user_token_pre_save(sender, instance, *args, **kwargs):
    if not instance.token:
        instance.token = randint(10000, 99999)

pre_save.connect(user_token_pre_save, sender=UserToken)