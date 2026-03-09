from django.urls import path
from . import views

urlpatterns = [

    # LISTE
    path('auteurs/', views.liste_auteurs, name='liste_auteurs'),

    # CREER
    path('auteurs/creer/', views.creer_auteur, name='creer_auteur'),

    # DETAIL
    path('auteurs/<int:id>/', views.detail_auteur, name='detail_auteur'),

    # MODIFIER
    path('auteurs/<int:id>/modifier/', views.modifier_auteur, name='modifier_auteur'),

    # SUPPRIMER
    path('auteurs/<int:id>/supprimer/', views.supprimer_auteur, name='supprimer_auteur'),

# ============================================
 # URLs POUR LIVRE ( VUES CLASSES )
 #=============================================
        path('livres/', views.ListeLivresView.as_view(), name='liste_livres'),
    path('livres/<int:id>/', views.DetailLivreView.as_view(), name='detail_livre'),
]