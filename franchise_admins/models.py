# franchise_admins/models.py

from django.db import models
from branches.models import Branch

class FranchiseAdmin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)  # You might need to hash the password
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_role(self):
        # Implement logic to get the role based on permissions, etc.
        return "Franchise Admin"
    
    # Other advanced methods, properties, and fields