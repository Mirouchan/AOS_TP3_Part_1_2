from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Auteur , Livre
from django.views import View
from django.utils.decorators import method_decorator


# ============================================
# LISTE DES AUTEURS
# ============================================

def liste_auteurs(request):
    """GET : Retourne la liste de tous les auteurs"""

    auteurs = Auteur.objects.all()

    data = [
        {
            "id": auteur.id,
            "nom": auteur.nom,
            "prenom": auteur.prenom,
            "date_naissance": auteur.date_naissance,
            "biographie": auteur.biographie
        }
        for auteur in auteurs
    ]

    return JsonResponse(data, safe=False)


# ============================================
# DETAIL AUTEUR
# ============================================

def detail_auteur(request, id):
    """GET : Retourne les détails d'un auteur"""

    auteur = get_object_or_404(Auteur, id=id)

    data = {
        "id": auteur.id,
        "nom": auteur.nom,
        "prenom": auteur.prenom,
        "date_naissance": auteur.date_naissance,
        "biographie": auteur.biographie
    }

    return JsonResponse(data)


# ============================================
# CREER AUTEUR
# ============================================

@csrf_exempt
def creer_auteur(request):
    """POST : Crée un nouvel auteur"""

    if request.method != "POST":
        return JsonResponse({"erreur": "Méthode non autorisée"}, status=405)

    try:
        data = json.loads(request.body)

        auteur = Auteur.objects.create(
            nom=data.get("nom"),
            prenom=data.get("prenom"),
            date_naissance=data.get("date_naissance"),
            biographie=data.get("biographie", "")
        )

        return JsonResponse({
            "id": auteur.id,
            "message": "Auteur créé avec succès"
        }, status=201)

    except Exception as e:
        return JsonResponse({"erreur": str(e)}, status=400)


# ============================================
# MODIFIER AUTEUR
# ============================================

@csrf_exempt
def modifier_auteur(request, id):
    """PUT : Modifie un auteur"""

    if request.method != "PUT":
        return JsonResponse({"erreur": "Méthode non autorisée"}, status=405)

    auteur = get_object_or_404(Auteur, id=id)

    try:
        data = json.loads(request.body)

        auteur.nom = data.get("nom", auteur.nom)
        auteur.prenom = data.get("prenom", auteur.prenom)
        auteur.date_naissance = data.get("date_naissance", auteur.date_naissance)
        auteur.biographie = data.get("biographie", auteur.biographie)

        auteur.save()

        return JsonResponse({
            "message": "Auteur modifié avec succès"
        })

    except Exception as e:
        return JsonResponse({"erreur": str(e)}, status=400)


# ============================================
# SUPPRIMER AUTEUR
# ============================================

@csrf_exempt
def supprimer_auteur(request, id):
    """DELETE : Supprime un auteur"""

    if request.method != "DELETE":
        return JsonResponse({"erreur": "Méthode non autorisée"}, status=405)

    auteur = get_object_or_404(Auteur, id=id)

    auteur.delete()

    return JsonResponse({
        "message": "Auteur supprimé avec succès"
    }, status=204)
# ============================================
# VUES CLASSES POUR LIVRE
# ============================================

@method_decorator(csrf_exempt, name='dispatch')
class ListeLivresView(View):
    """GET : Liste tous les livres
       POST : Crée un nouveau livre
    """

    def get(self, request):
        livres = Livre.objects.all()
        data = [
            {
                "id": livre.id,
                "titre": livre.titre,
                "date_publication": livre.date_publication,
                "auteur_id": livre.auteur_id,
                "resume": livre.resume
            }
            for livre in livres
        ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            livre = Livre.objects.create(
                titre=data.get("titre"),
                date_publication=data.get("date_publication"),
                auteur_id=data.get("auteur_id"),
                resume=data.get("resume", "")
            )
            return JsonResponse({
                "id": livre.id,
                "message": "Livre créé avec succès"
            }, status=201)
        except Exception as e:
            return JsonResponse({"erreur": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class DetailLivreView(View):
    """GET, PUT, DELETE pour un livre spécifique"""

    def get(self, request, id):
        livre = get_object_or_404(Livre, id=id)
        data = {
            "id": livre.id,
            "titre": livre.titre,
            "date_publication": livre.date_publication,
            "auteur_id": livre.auteur_id,
            "auteur_nom": f"{livre.auteur.prenom} {livre.auteur.nom}",
            "resume": livre.resume
        }
        return JsonResponse(data)

    def put(self, request, id):
        livre = get_object_or_404(Livre, id=id)
        try:
            data = json.loads(request.body)
            livre.titre = data.get("titre", livre.titre)
            livre.date_publication = data.get("date_publication", livre.date_publication)
            livre.auteur_id = data.get("auteur_id", livre.auteur_id)
            livre.resume = data.get("resume", livre.resume)
            livre.save()
            return JsonResponse({"message": "Livre modifié avec succès"})
        except Exception as e:
            return JsonResponse({"erreur": str(e)}, status=400)

    def delete(self, request, id):
        livre = get_object_or_404(Livre, id=id)
        livre.delete()
        return JsonResponse({"message": "Livre supprimé avec succès"}, status=204)
