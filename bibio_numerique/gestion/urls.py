from django.urls import path
from . import views

urlpatterns = [
    # AUTEURS ✅ URLs DISTINCTES
    path('auteurs/', views.liste_auteurs, name='liste_auteurs'),
    path('auteurs/<int:id>/', views.detail_auteur, name='detail_auteur'),
    path('auteurs/<int:id>/modifier/', views.modifier_auteur, name='modifier_auteur'),
    path('auteurs/<int:id>/supprimer/', views.supprimer_auteur, name='supprimer_auteur'), 
    
    # LIVRES
    path('livres/', views.ListeLivresView.as_view(), name='liste_livres'),
    path('livres/<int:id>/', views.DetailLivreView.as_view(), name='detail_livre'),
    
    # EMPRUNTS
    path('emprunts/', views.ListeEmpruntsView.as_view(), name='liste_emprunts'),
    path('emprunts/<int:id>/', views.DetailEmpruntView.as_view(), name='detail_emprunt'),
]