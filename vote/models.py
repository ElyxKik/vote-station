from django.db import models
from django.db.models.deletion import CASCADE

from compte.models import User



class Election(models.Model):

    class SystemeVote(models.TextChoices):
        VOTE_A_BULLETIN_SECRET = 'Vote à bulletin sécret'
        VOTE_NON_ANONYME = 'Vote non anonyme'

    user = models.ForeignKey(User, on_delete=CASCADE)
    titre = models.CharField(max_length=100)
    groupe = models.CharField(max_length=100)
    systeme_de_vote = models.CharField(choices=SystemeVote.choices, default='Vote à bulletin sécret',max_length=100)
    debut_election = models.DateTimeField()
    fin_election = models.DateTimeField()
    published = models.BooleanField(default=False)
    resultat = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)


class ScrutinList(models.Model):
    titre_du_scrutin = models.CharField(max_length=100)
    election = models.ForeignKey(Election, on_delete=CASCADE)
    description = models.TextField(blank=True)
    gagnant = models.CharField(max_length=200, blank=True)


class VoteSimple(models.Model):
    titre = models.CharField(max_length=100)
    election = models.ForeignKey(Election, on_delete=CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)


class Candidat(models.Model):
    list_candidat = models.ForeignKey(ScrutinList, on_delete=CASCADE)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    post_nom = models.CharField(max_length=50, blank=True)
    numero = models.PositiveIntegerField(default=0)
    photo = models.ImageField(
        verbose_name='photo de profil', upload_to='photo_candidat', blank=True)
    key = models.CharField(max_length=50)
    telephone = models.PositiveIntegerField()
    email = models.EmailField()
    date = models.DateTimeField(auto_now=True)


class Electeur(models.Model):
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    post_nom = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)


class VoixVoteScrutin(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=CASCADE, null=True, blank=True)
    electeur = models.ForeignKey(Electeur, on_delete=CASCADE)
    key = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)


class VoixVoteSimple(models.Model):
    vote_simple = models.ForeignKey(VoteSimple, on_delete=CASCADE)
    electeur = models.ForeignKey(Electeur, on_delete=CASCADE)
    vote = models.BooleanField(null=True)
    key = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)



