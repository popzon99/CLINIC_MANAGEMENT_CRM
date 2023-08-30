from django.db import models
from django.contrib.auth.models import User
from branches.models import Branch
from patients.models import Patient  # New import for Prescription
from appointments.models import Appointment  # New import for Prescription

# Speciality Model
class Speciality(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class WorkingDay(models.Model):
    day_name = models.CharField(max_length=20)
    weekday_number = models.IntegerField()  # <-- Add this line

    def __str__(self):
        return self.day_name

# Time Slot Model
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

# Therapist Model
class Therapist(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    qualification = models.CharField(max_length=200)  # Added Qualification
    specialities = models.ManyToManyField(Speciality)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    appointment_interval = models.PositiveIntegerField()  # Changed name to appointment_interval
    working_days = models.ManyToManyField(WorkingDay, through='TherapistWorkingDay')  # Through an intermediary model
    is_active = models.BooleanField(default=True)
    profile_photo = models.ImageField(upload_to='therapists/', blank=True, null=True)

    def __str__(self):
        return self.name

# Therapist Working Day Through Model
class TherapistWorkingDay(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    working_day = models.ForeignKey(WorkingDay, on_delete=models.CASCADE)
    time_slots = models.ManyToManyField(TimeSlot)

# Therapist Login Model
class TherapistLogin(models.Model):
    therapist = models.OneToOneField(Therapist, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='therapists/logins/', blank=True, null=True)

    def __str__(self):
        return f"Login for {self.therapist.name}"
    


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.TextField()
    dosage = models.TextField()
    frequency = models.CharField(max_length=100)
    additional_notes = models.TextField(blank=True, null=True)
    date_issued = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.user.first_name} from {self.therapist.name}"
