from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class RoleModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    permissions = models.ManyToManyField('auth.Permission', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class UserModel(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    role = models.ForeignKey(RoleModel, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    _is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_permission(self, perm_codename):
        """
        Custom permission check against the RoleModel's permissions.
        perm_codename: The codename of the permission (e.g., 'add_tablemodel').
        """
        # Check if the user's role has the specified permission
        if self.role:
            return self.role.permissions.filter(codename=perm_codename).exists()
        return False

    def has_module_perms(self, app_label):
        # Check if the user has any permissions within the specified app
        if self.role:
            return self.role.permissions.filter(content_type__app_label=app_label).exists()
        return False

    @property
    def is_staff(self):
        # Allow access to the admin interface if the user is a superuser or has staff access
        return self.is_superuser or self._is_staff

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value