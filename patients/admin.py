from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Patient, PatientLogin

# Inline for PatientLogin
class PatientLoginInline(admin.StackedInline):
    model = PatientLogin
    can_delete = False
    verbose_name_plural = 'Login Information'

# Custom UserAdmin with PatientLoginInline
class CustomUserAdmin(UserAdmin):
    inlines = (PatientLoginInline,)

# Register User with CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'date_of_birth', 'email')
    list_filter = ('gender',)
    search_fields = ('name', 'email')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'address', 'specialities', 'location', 'phone', 'date_of_birth', 'gender')
        }),
        ('Medical Information', {
            'fields': ('height', 'weight', 'blood_group', 'notes')
        }),
        ('Login Information', {
            'fields': ('email', 'profile_photo')
        }),
    )
    inlines = (PatientLoginInline,)
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(user__is_active=True)
    make_active.short_description = "Activate selected patients"

    def make_inactive(self, request, queryset):
        queryset.update(user__is_active=False)
    make_inactive.short_description = "Deactivate selected patients"

@admin.register(PatientLogin)
class PatientLoginAdmin(admin.ModelAdmin):
    list_display = ('patient', 'user', 'profile_photo')
    search_fields = ('patient__name', 'user__username')

# Register Patient and PatientLogin models
admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientLogin, PatientLoginAdmin)

