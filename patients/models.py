from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    specialities = models.ManyToManyField('treatments.Speciality')
    location = models.CharField(max_length=100)
    # Add other fields as needed
    # ...

class PatientLogin(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    # Add other fields as needed
    # ...

