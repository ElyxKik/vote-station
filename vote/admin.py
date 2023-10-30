from django.contrib import admin

from vote.models import Candidat, Election, Electeur



class CandidatAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'post_nom', 'photo', 'numero')

class ElecteurAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'post_nom')

admin.site.register(Candidat, CandidatAdmin)
admin.site.register(Election)
admin.site.register(Electeur, ElecteurAdmin)