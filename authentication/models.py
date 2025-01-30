from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    # Ajoutez vos champs personnalisés si nécessaire
    email = models.EmailField(unique=True)

    # Résolvez les conflits en définissant explicitement les related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Nom unique pour éviter les conflits
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Nom unique pour éviter les conflits
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )