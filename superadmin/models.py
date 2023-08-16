from django.db import models



class Admin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    branch = models.ForeignKey('branches.Branch', on_delete=models.SET_NULL, null=True)
    # Add other fields as needed
    # ...

class Settings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)
    # Add other fields as needed
    # ...
