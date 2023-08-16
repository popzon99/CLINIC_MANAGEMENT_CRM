from django.db import models

class Appointment(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    therapist = models.ForeignKey('physiotherapist.Physiotherapist', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    # Add other fields as needed
    # ...



