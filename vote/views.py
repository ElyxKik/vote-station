from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from vote.models import Election, Candidat, Electeur, ScrutinList, VoteSimple, VoixVoteScrutin, VoixVoteSimple
from vote.forms import ElectionForm, CandidatForm, ScrutinListForm



@login_required
def home(request):
    try:
        elections = Election.objects.all()
    except Election.DoesNotExist:
        elections = []
    return render(request, 'accueil.html', {'elections':elections})


def election(request):
    form = ElectionForm()
    try:
        elections = Election.objects.all()[:4]
    except Election.DoesNotExist:
        elections = []
    nombre_election = elections.count()
    return render(request, 'elections.html', {'elections':elections, 'nombre_election':nombre_election, 'form':form})


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


def new_election(request):
    user = request.user
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.user = user
            form2.save()
            return redirect('election')


def scrutin_liste_detail(request, id):
    scrutin = ScrutinList.objects.get(id=id)
    candidats = Candidat.objects.filter(list_candidat=scrutin)
    return render(request, 'scrutin-detail.html', {'scrutin':scrutin, 'candidats':candidats})


def new_scrutin_liste(request, id):
    election = Election.objects.get(id=id)
    if request.method == 'POST':
        titre_scrutin = request.POST.get('scrutin')
        description = request.POST.get('description')
        scrutin = ScrutinList.objects.create(titre_du_scrutin=titre_scrutin, election=election, description=description)
        scrutin.save()
        return redirect('scrutin_liste_detail', scrutin.id)



def new_vote_simple(request, id):
    election = Election.objects.get(id=id)
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        vote_simple = VoteSimple.objects.create(titre=titre, election=election, description=description)
        vote_simple.save()
        return redirect('vote_simple_detail', vote_simple.id)
    

def vote_simple_detail(request, id):
    vote_simple = VoteSimple.objects.get(id=id)
    return render(request, 'vote_simple_detail.html', {'vote_simple':vote_simple})



def candidats(request):
    candidats = Candidat.objects.all()
    return render(request,'candidats.html', {'candidats':candidats})


def candidat_detail(request, id):
    candidat = Candidat.objects.get(id=id)
    return render(request, 'candidat.html', {'candidat': candidat})


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
    


def page_vote(request, id):
    election = Election.objects.get(id=id)
    liste = ScrutinList.objects.filter(election=election)
    liste_non_vide = [l for l in liste if l.candidat_set.exists()]
    try:
        user = Electeur.objects.get(user=request.user)
    except Electeur.DoesNotExist:
        return redirect('non_authoriser')
    if request.method == 'POST':
        candidat_select = request.POST.getlist('candidat')
        for candidat_id in candidat_select:
            candidat = Candidat.objects.get(id=candidat_id)
            vote = VoixVoteScrutin.objects.create(candidat=candidat, electeur=user, key="fjr*55")
            vote.save()
        return redirect('confiramtion_vote')
    return render(request, 'page_vote.html', {'liste_non_vide':liste_non_vide, 'election':election})


def non_authoriser(request):
    return render(request, 'non_authoriser.html')


def confiramtion_vote(request):
    return render(request, 'confiramtion_vote.html')