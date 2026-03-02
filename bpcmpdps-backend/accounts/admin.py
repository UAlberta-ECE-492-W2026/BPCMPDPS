from django.contrib import admin
from .models import OperatorProfile

@admin.register(OperatorProfile)
class OperatorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "alerts_enabled")
    search_fields = ("user__username", "user__email", "phone_number")