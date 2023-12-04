from django.contrib import admin
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'company_name', 'created_at', 'updated_at', 'commercial_assigne_display')

    def commercial_assigne_display(self, obj):
        return obj.commercial_assigne.get_full_name() if obj.commercial_assigne else 'Non Assigné'
    commercial_assigne_display.short_description = 'Commercial Assigné'


admin.site.register(Client, ClientAdmin)
