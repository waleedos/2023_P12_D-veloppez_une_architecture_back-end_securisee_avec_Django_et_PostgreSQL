from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator
from django.contrib.auth.models import Group


class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('L\'email doit être défini'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    class Department(models.TextChoices):
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
    first_name = models.CharField(_('prénom'), max_length=30, blank=True)
    last_name = models.CharField(_('nom de famille'), max_length=30, blank=True)
    phone_number = models.CharField(_('numéro de téléphone'), max_length=20, blank=True)
    department = models.CharField(
        _('département'),
        max_length=3,
        choices=Department.choices,
        default=Department.COMMERCIAL
    )
    is_staff = models.BooleanField(_('membre du staff'), default=False)
    is_active = models.BooleanField(_('actif'), default=True)

    objects = UtilisateurManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self):
        return self.first_name

    def assign_role(self, role):
        # Assurez-vous que le rôle (département) existe
        group, created = Group.objects.get_or_create(name=role)
        self.groups.add(group)
