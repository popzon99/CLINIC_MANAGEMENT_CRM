from django.db import models

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields as needed
    # ...

class Treatment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    specialities = models.ManyToManyField(Speciality)
    # Add other fields as needed
    # ...

