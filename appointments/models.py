# Import Django modules
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# Import other modules in your project
from patients.models import Patient
from physiotherapists.models import Therapist, TimeSlot, TherapistWorkingDay
from accounts.models import Invoice  # Make sure to import your Invoice model
from twilio.rest import Client
from clinic_app.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.base.exceptions import TwilioRestException
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Constants
PENDING = 'Pending'
ACCEPTED = 'Accepted'
REJECTED = 'Rejected'
COMPLETED = 'Completed'
CANCELLED = 'Cancelled'

APPOINTMENT_STATUS = [
    (PENDING, 'Pending'),
    (ACCEPTED, 'Accepted'),
    (REJECTED, 'Rejected'),
    (COMPLETED, 'Completed'),
    (CANCELLED, 'Cancelled'),
]

# Function to send SMS via Twilio
def send_sms(message, to):
    try:
        client.messages.create(body=message, from_='+YourTwilioNumber', to=to)
    except TwilioRestException as e:
        logger.error(f"An error occurred while sending the SMS: {str(e)}")

# Define the Appointment model
class Appointment(models.Model):
    # Model fields
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='appointments')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, related_name='appointments')
    appointment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default=PENDING)
    invoice = models.OneToOneField(Invoice, null=True, blank=True, on_delete=models.SET_NULL, related_name='appointment')

    # Meta options
    class Meta:
        unique_together = ('therapist', 'time_slot', 'appointment_date')
        ordering = ['appointment_date', 'time_slot']

   




    # Check if the appointment is for today
    def is_today(self):
        return timezone.now().date() == self.appointment_date

    # Custom validations
    def clean(self):
        super().clean()
        working_days = self.therapist.working_days.all()
        if self.appointment_date.weekday() not in [d.weekday_number for d in working_days]:
            raise ValidationError(_('The selected date is not a working day for this therapist.'))

        overlapping_appointments = Appointment.objects.filter(
            therapist=self.therapist,
            appointment_date=self.appointment_date,
            time_slot=self.time_slot,
            status__in=[PENDING, ACCEPTED]
        ).exclude(id=self.id)
        if overlapping_appointments.exists():
            raise ValidationError(_('The selected time slot is already booked.'))

    # Save method
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # String representation of the model
    def __str__(self):
        return f"{self.patient.user.first_name} appointment with {self.therapist.name} on {self.appointment_date}"

    # Check if the appointment is upcoming
    @property
    def is_upcoming(self):
        return timezone.now().date() < self.appointment_date

    # Check if the appointment is past due
    @property
    def is_past_due(self):
        return timezone.now().date() > self.appointment_date

# Signal to send SMS when appointment is created or updated
@receiver(post_save, sender=Appointment)
def appointment_created_or_updated(sender, instance, created, **kwargs):
    if created:
        doctor_message = f"A new appointment {instance.id} is scheduled for {instance.appointment_date} at {instance.time_slot.start_time} with the patient {instance.patient.user.first_name}. Thank you. Meditrac Team"
        patient_message = f"Your appointment {instance.id} with {instance.therapist.name} is scheduled for {instance.appointment_date} at {instance.time_slot.start_time}. Thank you. Meditrac Team"
    else:
        doctor_message = f"Appointment {instance.id} with {instance.therapist.name} has been updated to {instance.appointment_date} at {instance.time_slot.start_time}."
        patient_message = f"Your appointment {instance.id} with {instance.therapist.name} has been updated to {instance.appointment_date} at {instance.time_slot.start_time}."

    try:
        send_sms(doctor_message, instance.therapist.phone_number)
        send_sms(patient_message, instance.patient.phone_number)
    except TwilioRestException as e:
        logger.error(f"An error occurred while sending the SMS: {str(e)}")

# Signal to send SMS when appointment is cancelled
@receiver(pre_delete, sender=Appointment)
def appointment_cancelled(sender, instance, **kwargs):
    message = f"Your appointment with {instance.therapist.name} on {instance.appointment_date} has been cancelled."
    send_sms(message, instance.patient.phone)
