from django.contrib import admin
from .models import Patient, Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'location', 'date_added', 'patient_id')
    list_filter = ('gender', 'location', 'date_added')
    search_fields = ('user__first_name', 'user__last_name', 'patient_id')

    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'address', 'phone', 'date_of_birth', 'gender', 'profile_photo', 'tags')
        }),
        ('Medical Information', {
            'fields': ('height', 'weight', 'blood_group', 'notes')
        }),
        ('Additional Information', {
            'fields': ('location', 'specialities', 'date_added', 'patient_id')
        }),
    )

# Register your models here.
admin.site.register(Tag, TagAdmin)
admin.site.register(Patient, PatientAdmin)

