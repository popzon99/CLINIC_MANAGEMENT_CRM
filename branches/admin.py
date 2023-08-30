from django.contrib import admin
from .models import Branch
from .forms import BranchForm

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'phone_number', 'is_working')
    list_filter = ('is_working',)
    search_fields = ('name', 'address', 'email', 'phone_number')
    ordering = ('name',)
    actions = ['mark_as_working', 'mark_as_not_working']

    form = BranchForm

    def mark_as_working(self, request, queryset):
        queryset.update(is_working=True)
    mark_as_working.short_description = "Mark selected branches as working"

    def mark_as_not_working(self, request, queryset):
        queryset.update(is_working=False)
    mark_as_not_working.short_description = "Mark selected branches as not working"

admin.site.register(Branch, BranchAdmin)
