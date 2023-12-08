from django.db import models
# Importer 'models' de Django pour définir des modèles de base de données personnalisés

from django.utils.translation import gettext_lazy as _
# Importer 'gettext_lazy' pour permettre la traduction des chaînes de caractères dans les modèles
# 'gettext_lazy' est utilisé pour marquer les chaînes pour la traduction sans les traduire immédiatement

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Importer 'AbstractBaseUser' et 'PermissionsMixin' pour créer un modèle d'utilisateur personnalisé
# 'AbstractBaseUser' fournit les fonctionnalités de base d'un utilisateur
# 'PermissionsMixin' ajoute la gestion des permissions et des groupes pour l'utilisateur

from django.core.validators import EmailValidator
# Importer 'EmailValidator' pour valider les adresses emails dans les champs de modèle

from django.contrib.auth.models import Group
# Importer 'Group' pour gérer et assigner des groupes (rôles) aux utilisateurs


class UtilisateurManager(BaseUserManager):
    # Gestionnaire personnalisé pour les utilisateurs qui définit comment les utilisateurs sont créés et gérés

    def create_user(self, email, password=None, **extra_fields):
        # Créer et sauvegarder un nouvel utilisateur avec l'adresse email et le mot de passe fournis
        if not email:
            # Vérifier si l'email est fourni, sinon lever une exception
            raise ValueError(_('L\'email doit être défini'))
        email = self.normalize_email(email)  # Normaliser l'adresse email
        user = self.model(email=email, **extra_fields)  # Créer un nouvel objet utilisateur
        user.set_password(password)  # Définir le mot de passe de l'utilisateur
        user.save(using=self._db)  # Sauvegarder l'utilisateur dans la base de données
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Créer et sauvegarder un superutilisateur avec l'adresse email et le mot de passe fournis
        extra_fields.setdefault('is_staff', True)  # Définir is_staff sur True
        extra_fields.setdefault('is_superuser', True)  # Définir is_superuser sur True
        return self.create_user(email, password, **extra_fields)  # Créer l'utilisateur en utilisant create_user


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    # Définition du modèle Utilisateur, qui étend AbstractBaseUser et PermissionsMixin

    class Department(models.TextChoices):
        # Classe interne pour définir les choix de département de l'utilisateur
        ADMINISTRATION = 'ADM', _('Administration')
        COMMERCIAL = 'COM', _('Commercial')
        SUPPORT = 'SUP', _('Support')
        GESTION = 'GES', _('Gestion')
        TEST = 'TST', _('Test')

    email = models.EmailField(
        _('adresse email'),
        unique=True,
        validators=[EmailValidator(message=_("Entrez une adresse email valide."))]
    )
    # Champs de base pour l'utilisateur
    first_name = models.CharField(_('prénom'), max_length=30, blank=True)
    last_name = models.CharField(_('nom de famille'), max_length=30, blank=True)
    phone_number = models.CharField(_('numéro de téléphone'), max_length=20, blank=True)
    department = models.CharField(
        _('département'),
        max_length=3,
        choices=Department.choices,
        default=Department.COMMERCIAL
    )
    is_staff = models.BooleanField(_('membre du staff'), default=False)  # Détermine si l'utilisateur peut accéder à
    # l'admin Django
    is_active = models.BooleanField(_('actif'), default=True)  # Indique si le compte de l'utilisateur est actif

    objects = UtilisateurManager()  # Associer le gestionnaire personnalisé à ce modèle

    USERNAME_FIELD = 'email'  # Utiliser l'email comme identifiant principal pour l'authentification
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Champs requis en plus de l'email lors de la création de l'utilisateur

    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')

    def __str__(self):
        # Représentation en chaîne de l'utilisateur, affiche son email
        return self.email

    def get_full_name(self):
        # Renvoie le nom complet de l'utilisateur
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self):
        # Renvoie le prénom de l'utilisateur
        return self.first_name

    def assign_role(self, role):
        # Assigner un rôle (département) à l'utilisateur
        group, created = Group.objects.get_or_create(name=role)  # Créer le groupe si nécessaire
        self.groups.add(group)  # Ajouter l'utilisateur au groupe
