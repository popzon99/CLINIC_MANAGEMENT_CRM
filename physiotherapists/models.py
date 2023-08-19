from django.db import models
from django.contrib.auth.models import User
from branches.models import Branch

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class WorkingDay(models.Model):
    day_name = models.CharField(max_length=20)

    def __str__(self):
        return self.day_name

class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

class Therapist(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    specialities = models.ManyToManyField(Speciality)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    slots_per_minute = models.PositiveIntegerField()
    working_days = models.ManyToManyField(WorkingDay)
    time_slots = models.ManyToManyField(TimeSlot)
    is_active = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='therapists/', blank=True, null=True)

    def __str__(self):
        return self.name

class TherapistLogin(models.Model):
    therapist = models.OneToOneField(Therapist, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='therapists/logins/', blank=True, null=True)

    def __str__(self):
        return f"Login for {self.therapist.name}"

