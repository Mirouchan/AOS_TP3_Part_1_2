from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Auteur, Livre, Emprunt
from django.views import View
from django.utils.decorators import method_decorator

# ============================================
# AUTEURS - VUES FONCTIONS
# ============================================

@csrf_exempt
@require_http_methods(["GET", "POST"])
def liste_auteurs(request):
    if request.method == "GET":
        auteurs = Auteur.objects.all()
        data = [{"id": a.id, "nom": a.nom, "prenom": a.prenom, "nationalite": a.nationalite, "date_naissance": str(a.date_naissance), "biographie": a.biographie} for a in auteurs]
        return JsonResponse(data, safe=False)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            auteur = Auteur.objects.create(
                nom=data.get("nom"),
                prenom=data.get("prenom"),
                nationalite=data.get("nationalite", ""),
                date_naissance=data.get("date_naissance"),
                biographie=data.get("biographie", "")
            )
            return JsonResponse({"id": auteur.id, "message": "Créé"}, status=201)
        except Exception as e:
            return JsonResponse({"erreur": str(e)}, status=400)

@csrf_exempt
def detail_auteur(request, id):
    auteur = get_object_or_404(Auteur, id=id)
    data = {"id": auteur.id, "nom": auteur.nom, "prenom": auteur.prenom, "nationalite": auteur.nationalite, "date_naissance": str(auteur.date_naissance), "biographie": auteur.biographie}
    return JsonResponse(data)

@csrf_exempt
@require_http_methods(["PUT"])
def modifier_auteur(request, id):
    auteur = get_object_or_404(Auteur, id=id)
    try:
        data = json.loads(request.body)
        auteur.nom = data.get("nom", auteur.nom)
        auteur.prenom = data.get("prenom", auteur.prenom)
        auteur.nationalite = data.get("nationalite", auteur.nationalite)
        auteur.date_naissance = data.get("date_naissance", auteur.date_naissance)
        auteur.biographie = data.get("biographie", auteur.biographie)
        auteur.save()
        return JsonResponse({"message": "Modifié"})
    except Exception as e:
        return JsonResponse({"erreur": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def supprimer_auteur(request, id):
    auteur = get_object_or_404(Auteur, id=id)
    auteur.delete()
    return JsonResponse({"message": "Supprimé"}, status=204)

# ============================================
# LIVRES - VUES CLASSES
# ============================================

@method_decorator(csrf_exempt, name='dispatch')
class ListeLivresView(View):
    def get(self, request):
        livres = Livre.objects.select_related('auteur').all()
        data = [{"id": l.id, "titre": l.titre, "isbn": l.isbn, "date_publication": str(l.date_publication), "nombre_pages": l.nombre_pages, "auteur_id": l.auteur_id, "auteur": f"{l.auteur.prenom} {l.auteur.nom}", "disponible": l.disponible, "resume": l.resume} for l in livres]
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            livre = Livre.objects.create(
                titre=data.get("titre"),
                isbn=data.get("isbn", ""),
                date_publication=data.get("date_publication"),
                nombre_pages=data.get("nombre_pages"),
                auteur_id=data.get("auteur_id"),
                resume=data.get("resume", "")
            )
            return JsonResponse({"id": livre.id, "message": "Livre créé"}, status=201)
        except Exception as e:
            return JsonResponse({"erreur": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class DetailLivreView(View):
    def get(self, request, id):
        livre = get_object_or_404(Livre, id=id)
        data = {"id": livre.id, "titre": livre.titre, "isbn": livre.isbn, "date_publication": str(livre.date_publication), "nombre_pages": livre.nombre_pages, "auteur_id": livre.auteur_id, "auteur": f"{livre.auteur.prenom} {livre.auteur.nom}", "disponible": livre.disponible, "resume": livre.resume}
        return JsonResponse(data)

    def put(self, request, id):
        livre = get_object_or_404(Livre, id=id)
        try:
            data = json.loads(request.body)
            livre.titre = data.get("titre", livre.titre)
            livre.isbn = data.get("isbn", livre.isbn)
            livre.date_publication = data.get("date_publication", livre.date_publication)
            livre.nombre_pages = data.get("nombre_pages", livre.nombre_pages)
            livre.auteur_id = data.get("auteur_id", livre.auteur_id)
            livre.resume = data.get("resume", livre.resume)
            livre.save()
            return JsonResponse({"message": "Livre modifié"})
        except Exception as e:
            return JsonResponse({"erreur": str(e)}, status=400)

    def delete(self, request, id):
        livre = get_object_or_404(Livre, id=id)
        livre.delete()
        return JsonResponse({"message": "Livre supprimé"}, status=204)

# ============================================
# EMPRUNTS - VUES CLASSES
# ============================================

@method_decorator(csrf_exempt, name='dispatch')
class ListeEmpruntsView(View):
    def get(self, request):
        emprunts = Emprunt.objects.select_related('livre__auteur').all()
        data = [{"id": e.id, "nom_lecteur": e.nom_lecteur, "livre_id": e.livre_id, "livre": e.livre.titre, "auteur": f"{e.livre.auteur.prenom} {e.livre.auteur.nom}", "date_emprunt": str(e.date_emprunt), "date_retour": str(e.date_retour) if e.date_retour else None} for e in emprunts]
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            emprunt = Emprunt.objects.create(
                nom_lecteur=data.get("nom_lecteur"),
                livre_id=data.get("livre")
            )
            return JsonResponse({"id": emprunt.id, "message": "Emprunt créé"}, status=201)
        except Exception as e:
            return JsonResponse({"erreur": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class DetailEmpruntView(View):
    def get(self, request, id):
        emprunt = get_object_or_404(Emprunt, id=id)
        data = {"id": emprunt.id, "nom_lecteur": emprunt.nom_lecteur, "livre": emprunt.livre.titre, "date_emprunt": str(emprunt.date_emprunt), "date_retour": str(emprunt.date_retour) if emprunt.date_retour else None}
        return JsonResponse(data)

    def put(self, request, id):
        emprunt = get_object_or_404(Emprunt, id=id)
        try:
            data = json.loads(request.body)
            if data.get("date_retour"):
                emprunt.date_retour = data.get("date_retour")
                emprunt.save()
            return JsonResponse({"message": "Emprunt mis à jour"})
        except Exception as e:
            return JsonResponse({"erreur": str(e)}, status=400)

    def delete(self, request, id):
        emprunt = get_object_or_404(Emprunt, id=id)
        emprunt.delete()
        return JsonResponse({"message": "Emprunt supprimé"}, status=204)