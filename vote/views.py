from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .decorators import admin_required

from vote.models import Election, Candidat, Electeur, ScrutinList, VoteSimple, VoixVoteScrutin, VoixVoteSimple
from vote.forms import ElectionForm, CandidatForm, ScrutinListForm



@admin_required
def home(request):
    elections = Election.objects.all()
    nombre_elections = elections.count()
    candidats = Candidat.objects.all()
    nombre_candidats = candidats.count()
    electeur = Electeur.objects.all()
    nombre_electeur = electeur.count()
    return render(request, 'accueil.html', {'elections':elections, 'nombre_elections':nombre_elections, 'nombre_candidats': nombre_candidats, 'nombre_electeur':nombre_electeur})


@admin_required
def election(request):
    form = ElectionForm()
    elections = Election.objects.filter(resultat=False)
    elections_passe = Election.objects.filter(resultat=True)
    nombre_election = elections.count()
    return render(request, 'elections.html', {'elections':elections, 'nombre_election':nombre_election, 'form':form, 'elections_passe':elections_passe})



@admin_required
def candidats(request):
    candidats = Candidat.objects.all()
    return render(request, 'candidats.html', {'candidats':candidats})


@admin_required
def election_detail(request, id):
    election = Election.objects.get(id=id)
    scrutin = ScrutinList.objects.filter(election=election)
    vote_simple = VoteSimple.objects.filter(election=election)
    scrutin_exist = scrutin.exists()
    vote_simple_exist = vote_simple.exists()
    return render(request, 'election-detail.html', {'election':election, 
                                                    'scrutin':scrutin, 
                                                    'vote_simple':vote_simple,
                                                    'scrutin_exist':scrutin_exist,
                                                    'vote_simple_exist':vote_simple_exist})

@admin_required
def electeurs(request):
    electeurs = Electeur.objects.all()
    return render(request, 'electeurs.html', {'electeurs': electeurs})



@admin_required
def new_election(request):
    user = request.user
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.user = user
            form2.save()
            return redirect('election')
        


@admin_required
def pub_election(request, id):
    election = Election.objects.get(id=id)
    election.published = True
    election.save(update_fields=['published'])
    return redirect('election_detail', election.id)



@admin_required
def del_election(request, id):
    election = Election.objects.get(id=id)
    election.delete()
    return redirect('election')

@admin_required
def scrutin_liste_detail(request, id):
    scrutin = ScrutinList.objects.get(id=id)
    candidats = Candidat.objects.filter(list_candidat=scrutin)
    return render(request, 'scrutin-detail.html', {'scrutin':scrutin, 'candidats':candidats})


@admin_required
def new_scrutin_liste(request, id):
    election = Election.objects.get(id=id)
    if request.method == 'POST':
        titre_scrutin = request.POST.get('scrutin')
        description = request.POST.get('description')
        scrutin = ScrutinList.objects.create(titre_du_scrutin=titre_scrutin, election=election, description=description)
        scrutin.save()
        return redirect('scrutin_liste_detail', scrutin.id)


@admin_required
def new_vote_simple(request, id):
    election = Election.objects.get(id=id)
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        vote_simple = VoteSimple.objects.create(titre=titre, election=election, description=description)
        vote_simple.save()
        return redirect('vote_simple_detail', vote_simple.id)

   
@admin_required
def vote_simple_detail(request, id):
    vote_simple = get_object_or_404(VoteSimple, id=id)
    try:
        nombre_oui = VoixVoteSimple.objects.filter(vote_simple=vote_simple, vote=True).count()
        nombre_non = VoixVoteSimple.objects.filter(vote_simple=vote_simple, vote=False ).count()
        nombre_null = VoixVoteSimple.objects.filter(vote_simple=vote_simple, vote=None ).count()
    except VoixVoteSimple.DoesNotExist:
        nombre_oui = 0
        nombre_non = 0
        nombre_null = 0
    return render(request, 'vote_simple_detail.html', {'vote_simple':vote_simple,
                                                        'nombre_oui':nombre_oui,
                                                        'nombre_non':nombre_non,
                                                        'nombre_null':nombre_null})


@admin_required
def candidats(request):
    candidats = Candidat.objects.all()
    return render(request,'candidats.html', {'candidats':candidats})


@admin_required
def candidat_detail(request, id):
    candidat = Candidat.objects.get(id=id)
    return render(request, 'candidat.html', {'candidat': candidat})


@admin_required
def new_candidat(request, id):
    liste = ScrutinList.objects.get(id=id)
    nombre_candidat = Candidat.objects.filter(list_candidat=liste).count()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        post_nom = request.POST.get('post_nom')
        prenom = request.POST.get('prenom')
        photo = request.FILES.get('photo')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        key = "Kddù*896"
        numero = nombre_candidat + 1
        candidat = Candidat.objects.create(list_candidat=liste, nom=nom, post_nom=post_nom, prenom=prenom, photo=photo, telephone=telephone, numero=numero, email=email, key=key)
        candidat.save()
        return redirect('scrutin_liste_detail', liste.id)
    

def voted(request):
    return render(request, 'voted.html')



def page_vote(request, id):
    election = get_object_or_404(Election, id=id)
    liste = ScrutinList.objects.filter(election=election)
    liste_non_vide = [l for l in liste if l.candidat_set.exists()]

    try:
        user = Electeur.objects.get(user=request.user)
    except Electeur.DoesNotExist:
        return redirect('non_authoriser')

    if user in election.electeur.all():
        return redirect('voted')

    if request.method == 'POST':
        candidat_select = [key for key in request.POST.keys() if key.startswith('candidat_')]
        
        for candidat_key in candidat_select:
            liste_id = candidat_key.split('_')[-1]
            candidat_id = request.POST[candidat_key]
            
            try:
                voix = VoixVoteScrutin.objects.get(liste_id=liste_id, candidat=candidat_id, electeur=user)
            except VoixVoteScrutin.DoesNotExist:
                voix = None
            
            if voix is None:
                # Créez un nouveau vote pour chaque candidat sélectionné
                vote = VoixVoteScrutin(liste_id=liste_id, candidat=candidat_id, electeur=user, key="fjr*55")
                vote.save()
                # Assurez-vous de gérer les erreurs ou les contraintes appropriées ici.
        
        return redirect('confirmation_vote')
    
    return render(request, 'page_vote.html', {'liste_non_vide':liste_non_vide, 'election':election})



def page_vote_simple(request, id):
    election = Election.objects.get(id=id)
    electeur =  Electeur.objects.get(user=request.user)
    vote_simple = VoteSimple.objects.get(election=election)
    voix = VoixVoteSimple.objects.filter(vote_simple=vote_simple, electeur=electeur).exists()
    
    if voix:
        return redirect('voted')
    
    return render(request, 'page_vote_simple.html', {'election':election, 'vote_simple':vote_simple, 'voix':voix})


def vote_simple_oui(request, id):
    vote_simple = VoteSimple.objects.get(id=id)
    try:
        user = Electeur.objects.get(user=request.user)
    except Electeur.DoesNotExist:
        return redirect('non_authoriser')
    vote = VoixVoteSimple.objects.create(vote_simple=vote_simple, electeur=user, vote=True, key="fjr*55")
    vote.save()
    return redirect('confirmation_vote')

def vote_simple_non(request, id):
    vote_simple = VoteSimple.objects.get(id=id)
    try:
        user = Electeur.objects.get(user=request.user)
    except Electeur.DoesNotExist:
        return redirect('non_authoriser')
    vote = VoixVoteSimple.objects.create(vote_simple=vote_simple, electeur=user, vote=False, key="fjr*55")
    vote.save()
    return redirect('confirmation_vote')


def vote_simple_null(request, id):
    vote_simple = VoteSimple.objects.get(id=id)
    try:
        user = Electeur.objects.get(user=request.user)
    except Electeur.DoesNotExist:
        return redirect('non_authoriser')
    vote = VoixVoteSimple.objects.create(vote_simple=vote_simple, electeur=user, key="fjr*55")
    vote.save()
    return redirect('confirmation_vote')


def page_electeur(request):
    elections = Election.objects.filter(published=True, resultat=False )
    elections_passe = Election.objects.filter(published=True, resultat=True )
    return render(request, 'page_electeur.html', {'elections':elections, 'elections_passe':elections_passe})



def non_authoriser(request):
    return render(request, 'non_authoriser.html')


def confirmation_vote(request):
    return render(request, 'confiramtion_vote.html')