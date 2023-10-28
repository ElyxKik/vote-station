from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from vote.models import Election
from vote.forms import ElectionForm


@login_required
def home(request):
    return render(request, 'accueil.html')


def election(request):
    elections = Election.objects.all()
    return render(request, 'elections.html', {'elections':elections})


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

