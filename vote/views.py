from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from vote.models import Election, Candidat, Electeur, ScrutinList, VoteSimple
from vote.forms import ElectionForm, CandidatForm, ScrutinListForm



@login_required
def home(request):
    return render(request, 'accueil.html')


def election(request):
    elections = Election.objects.all()
    nombre_election = elections.count()
    return render(request, 'elections.html', {'elections':elections, 'nombre_election':nombre_election})


def election_detail(request, id):
    election = Election.objects.get(id=id)
    scrutin = ScrutinList.objects.filter(election=election)
    return render(request, 'election-detail.html', {'election':election, 'scrutin':scrutin})


def new_election(request):
    user = request.user
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.user = user
            form2.save()
            return redirect('election')
    else:
        form = ElectionForm()
    return render(request, 'new-election.html', {'form':form})


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
    


