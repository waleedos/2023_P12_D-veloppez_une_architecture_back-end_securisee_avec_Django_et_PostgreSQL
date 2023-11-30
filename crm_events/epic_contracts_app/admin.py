from django.contrib import admin
from .models import Contrat


class ContratAdmin(admin.ModelAdmin):
    list_display = ('client', 'montant_total', 'montant_restant', 'date_creation', 'statut')


admin.site.register(Contrat, ContratAdmin)
