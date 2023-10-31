from django import forms

from vote.models import Election, Candidat, ScrutinList


class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ('titre', 'groupe', 'systeme_de_vote','type', 'debut_election', 'fin_election' )


class CandidatForm(forms.ModelForm):
    class Meta:
        model = Candidat
        fields = ('prenom', 'nom', 'post_nom', 'photo', 'telephone', 'email')


class ScrutinListForm(forms.ModelForm):
    class Meta:
        model = ScrutinList
        fields = ('titre_du_scrutin',)