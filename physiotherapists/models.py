from django.db import models

class Physiotherapist(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    specialities = models.ManyToManyField('treatments.Speciality')
    status = models.BooleanField(default=True)
    # Add other fields as needed
    # ...

class TherapistRequest(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    specialities = models.ManyToManyField('treatments.Speciality')
    status = models.BooleanField(default=False)  # Default to not approved
    # Add other fields as needed
    # ...

