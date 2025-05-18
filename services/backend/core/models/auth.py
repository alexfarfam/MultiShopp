from enum import Enum
from collections import OrderedDict

from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..managers import CustomUserManager

class Action(Enum):
    CREACION="01"
    ACTUALIZACION="02"
    ELIMINACION="03"

ACTIONS = OrderedDict((
    ('01', 'Creación'),
    ('02', 'Actualización'),
    ('03', 'Eliminación')
))

class Province(models.Model):
    id=models.CharField(_('Codigo'), max_length=2, primary_key=True, null=False)
    name=models.CharField(_('Nombre'), max_length=45)
    class Meta:
        verbose_name_plural="Provincias"
    def __str__(self):
        return f"Provincia '{self.name}'"

class Locality(models.Model):
    id=models.CharField(_('Codigo'), max_length=4, primary_key=True, null=False)
    name=models.CharField(_('Nombre'), max_length=45)
    province=models.ForeignKey(Province, verbose_name=_("Provincia"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural="Localidades"
    def __str__(self):
        return f"Provincia '{self.name}'"
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_provider=models.BooleanField(default=False)
    is_confirmed=models.BooleanField(default=False)
    joined_date=models.DateTimeField(_("Fecha Registro"), null=True, default=None)
    last_update_date=models.DateTimeField(_("Fecha Actualización"), null=True, default=None)
    
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()
    REQUIRED_FIELDS = ['username']
    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_sha256$"):
            self.set_password(self.password)
        super(CustomUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural="Usuarios"
    def __str__(self):
        return f"Usuario '{self.username}'"

class PaymentRecords(models.Model):
    amount=models.DecimalField(_("Monto"), max_digits=18, decimal_places=2)
    payment_date=models.DateTimeField(_("Fecha Pago"), null=True, default=None)
    expiration_date=models.DateTimeField(_("Fecha Vencimiento"))
    is_payment=models.BooleanField(default=False)
    provider=models.ForeignKey(CustomUser, verbose_name=_("Proveedor"), on_delete=models.CASCADE)
    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    
    def is_within_5_days(self):
        current_date = now()
        days_difference = (self.expiration_date - current_date).days
        return days_difference <= 5, days_difference

class History(models.Model):
    module=models.CharField(_("Modulo"), max_length=500)
    action=models.CharField(_("Accion"), max_length=2, choices=ACTIONS)
    datetime=models.DateTimeField(_("Fecha Registro"))
    responsible=models.ForeignKey(CustomUser, verbose_name=_("Responsable"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural="Historial"
    def __str__(self):
        return f"Historial '{self.action}-{self.responsible}'"

class CompanyInfo(models.Model):
    id=models.CharField(_("Codigo"), primary_key=True, max_length=4)
    company_name=models.CharField(_("Nombre Compañia"), max_length=500)
    logo=models.ImageField(_("Logo"), upload_to="uploads")
    
    url_facebook=models.URLField(_("Facebook"), max_length=500, blank=True)
    url_instagram=models.URLField(_("Instagram"), max_length=500, blank=True)
    customer_service_email=models.EmailField(_("Atencion Cliente Email"), max_length=500, blank=True)
    customer_service_telephone=models.CharField(_("Atención Cliente Teléfono"), max_length=20, blank=True)
    whatsapp_telephone=models.CharField(_("WhatsApp Teléfono"), max_length=20, blank=True)
    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    service_price=models.FloatField(_("Precio por servicio"), default=30000)

    class Meta:
        verbose_name_plural="Info Compañia"
    def __str__(self):
        return f"Compañia '{self.company_name}'"

class ProviderInfo(models.Model):
    logo=models.ImageField(_("Logo"), upload_to="uploads")
    company_name=models.URLField(_("Nombre Empresa"), max_length=500, blank=True)
    url_facebook=models.URLField(_("Facebook"), max_length=500, blank=True)
    url_instagram=models.URLField(_("Instagram"), max_length=500, blank=True)
    email=models.EmailField(_("Email"), max_length=500, blank=True)
    telephone=models.CharField(_("Teléfono"), max_length=20, blank=True)
    whatsapp_telephone=models.CharField(_("Teléfono"), max_length=20, blank=True)
    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    address=models.CharField(_("Direccion"), max_length=500, blank=True)

    user=models.ForeignKey(CustomUser, verbose_name=_("Usuario"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural="Info Proveedor"
    def __str__(self):
        return f"Info '{self.user.username}'"
    
class ClientInfo(models.Model):
    user=models.ForeignKey(CustomUser, verbose_name=_("Usuario"), on_delete=models.CASCADE)
    fullname=models.CharField(_("Nombres"), max_length=300, blank=True)
    email_order=models.CharField(_("Correo"), max_length=100, blank=True)
    telephone=models.CharField(_("Telefono"), max_length=20, blank=True)
    province=models.ForeignKey(Province, verbose_name=_("Provincia"), on_delete=models.CASCADE)
    locality=models.ForeignKey(Locality, verbose_name=_("Localidad"), on_delete=models.CASCADE)
    address=models.CharField(_("Direccion"), max_length=500)
    reference=models.CharField(_("Referencia"), max_length=500)

    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    last_update_date=models.DateTimeField(_("Fecha Actualizacion"), null=True, default=None)
    class Meta:
        verbose_name_plural="Info Cliente"
    def __str__(self):
        return f"Info '{self.user.username}'"

