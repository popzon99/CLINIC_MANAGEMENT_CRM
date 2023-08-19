
from django.contrib import admin
from .models import FranchiseAdmin

@admin.register(FranchiseAdmin)
class FranchiseAdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'branch', 'is_active')
    list_filter = ('branch', 'is_active')
    search_fields = ('name', 'email', 'phone')