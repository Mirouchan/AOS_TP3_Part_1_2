from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CompteManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username obligatoire")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
    
class Compte(AbstractUser):
    ROLES = (
        ('lecteur', 'Lecteur'),
        ('bibliothecaire', 'Bibliothecaire'),
    )

    role = models.CharField(max_length=20, choices=ROLES, default='lecteur')

    objects = CompteManager()

    def __str__(self):
        return self.username   