from django.db import models

class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    nationalite = models.CharField(max_length=100)
    date_naissance = models.DateField()
    biographie = models.TextField(blank=True)  

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    date_publication = models.DateField()
    nombre_pages = models.IntegerField(null=True, blank=True)
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE, related_name='livres')
    disponible = models.BooleanField(default=True)
    resume = models.TextField(blank=True)

    def __str__(self):
        return self.titre

class Emprunt(models.Model):
    nom_lecteur = models.CharField(max_length=200)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='emprunts')
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom_lecteur} emprunte {self.livre.titre}"