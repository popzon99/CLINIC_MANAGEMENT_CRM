from django.contrib import admin
from .models import Appointment, TimeSlot, AppointmentLog, AppointmentNote

class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 0

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date', 'doctor')
    search_fields = ('patient__name', 'doctor__name', 'patient__phone_number')
    inlines = [TimeSlotInline]

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time')
    list_filter = ('doctor',)
    search_fields = ('doctor__name',)

@admin.register(AppointmentLog)
class AppointmentLogAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'action', 'timestamp', 'user')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('appointment__patient__name', 'appointment__doctor__name', 'user__username')
    readonly_fields = ('timestamp',)

@admin.register(AppointmentNote)
class AppointmentNoteAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'timestamp', 'user')
    list_filter = ('timestamp', 'user')
    search_fields = ('appointment__patient__name', 'appointment__doctor__name', 'user__username')
    readonly_fields = ('timestamp',)

# Register other models (Therapist, Patient, Package) here if needed
