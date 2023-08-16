from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    # Add other fields as needed
    # ...
