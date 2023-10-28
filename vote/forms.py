from django import forms

from vote.models import Election


class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ('titre', 'groupe', 'systeme_de_vote', 'debut_election', 'fin_election' )