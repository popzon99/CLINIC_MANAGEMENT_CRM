from django.contrib import admin
from .models import Speciality, WorkingDay, TimeSlot, Therapist, TherapistLogin

class TimeSlotInline(admin.TabularInline):
    model = TimeSlot

class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ('day_name',)

class TherapistAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'phone', 'gender', 'is_active')
    list_filter = ('branch', 'gender', 'is_active')
    search_fields = ('name', 'phone')
    inlines = [TimeSlotInline]

class TherapistLoginAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'user')
    search_fields = ('therapist__name', 'user__username')

class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(WorkingDay, WorkingDayAdmin)
admin.site.register(Therapist, TherapistAdmin)
admin.site.register(TherapistLogin, TherapistLoginAdmin)
