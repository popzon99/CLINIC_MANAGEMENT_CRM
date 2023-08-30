from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from branches.models import Branch

class AdminUserManager(BaseUserManager):
    def create_user(self, email, name, phone, branch, role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone, branch=branch, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, branch, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, phone, branch, role, password, **extra_fields)

class AdminUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AdminUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'branch', 'role']

    def __str__(self):
        return self.name

    def get_role_display(self):
        return self.get_role().replace('_', ' ').title()

    def get_role(self):
        return self.role

class FranchiseAdmin(AdminUser):
    class Meta:
        verbose_name_plural = 'Franchise Admins'

    def get_role(self):
        return "Franchise Admin"

class Receptionist(AdminUser):
    class Meta:
        verbose_name_plural = 'Receptionists'

    def get_role(self):
        return "Receptionist"





