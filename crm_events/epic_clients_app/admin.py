from django.contrib import admin
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'company_name', 'created_at', 'updated_at', 'sales_contact')


admin.site.register(Client, ClientAdmin)
