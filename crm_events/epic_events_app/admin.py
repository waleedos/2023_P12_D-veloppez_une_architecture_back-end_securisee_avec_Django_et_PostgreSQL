from django.contrib import admin
from .models import Evenement


class EvenementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_debut', 'date_fin', 'lieu', 'type_evenement', 'statut', 'contrat')


admin.site.register(Evenement, EvenementAdmin)
