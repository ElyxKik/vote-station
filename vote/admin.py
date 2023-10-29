from django.contrib import admin

from vote.models import Candidat



class CandidatAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'post_nom', 'photo', 'numero')



admin.site.register(Candidat, CandidatAdmin)