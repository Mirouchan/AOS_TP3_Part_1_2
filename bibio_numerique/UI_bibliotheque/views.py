from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def accueil(request):
    nb_visites = request.session.get('visites', 0) + 1
    request.session['visites'] = nb_visites
    return render(request, 'accueil.html', {'visites': nb_visites})

def auteurs(request):
    return render(request, 'auteurs.html')

def livres(request):
    return render(request, 'livres.html')

def emprunts(request):
    return render(request, 'emprunts.html')

# ← SUPPRIMER ajouter_livre et supprimer_livre
# Votre API /api/livres/ gère déjà tout !