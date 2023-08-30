from django.db import models
from django.contrib.auth.models import User
from physiotherapists.models import Speciality
from branches.models import Branch

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

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
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
    
    # Profile photo with a default image (adjust the path accordingly)
    profile_photo = models.ImageField(upload_to='patients/', default='path/to/default/image.jpg')
    
    # Timestamp of when the patient is added
    date_added = models.DateTimeField(auto_now_add=True)  

    # Suggestion: Adding a human-readable unique patient ID 
    patient_id = models.CharField(max_length=10, unique=True)

    # Tags for the patient
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    


