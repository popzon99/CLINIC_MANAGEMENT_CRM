from django.db import models
from django.contrib.auth.models import User

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

class Patient(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    specialities = models.ManyToManyField('physiotherapists.Speciality')
    location = models.ForeignKey('branches.Branch', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    # Medical Information
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    # Login Information
    email = models.EmailField(unique=True)  # Ensure unique email for login
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # User for authentication
    
    profile_photo = models.ImageField(upload_to='patients/', blank=True, null=True)

    def __str__(self):
        return self.name

class PatientLogin(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # User for authentication
    # Additional login fields can be added here
    
    profile_photo = models.ImageField(upload_to='patients/logins/', blank=True, null=True)

    def __str__(self):
        return f"Login for {self.patient.name}"
