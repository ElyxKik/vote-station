"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from compte.views import login_user, signup,logout_user
from vote.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('connection', login_user, name='login'),
    path('inscription', signup, name='signup'),
    path('deconnection', logout_user, name='logout'),
    path('', home, name='home'),
    path('election/all', election, name='election'),
    path('election/new', new_election, name='new_election'),
    path('election/<int:id>', election_detail, name='election_detail'),
    path('scrutin-de-liste/new/<int:id>', new_scrutin_liste, name='new_scrutin_liste'),
    path('scrutin-de-liste/<int:id>', scrutin_liste_detail, name='scrutin_liste_detail'),
    path('candidat/new/<int:id>', new_candidat, name='new_candidat'),
    path('vote-simple/<int:id>', vote_simple_detail, name='vote_simple_detail'),
    path('vote-simple/new/<int:id>', new_vote_simple, name='new_vote_simple')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
