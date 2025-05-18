from datetime import datetime
import uuid

from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _

from .auth import CustomUser
from .categories import SubCategory

# Main Class
class Service(models.Model):
    title=models.CharField(_("Titulo"), max_length=200, blank=True)
    description=models.TextField(_("Descripcion"), blank=True)
    main_image=models.ImageField(_("Imagen Principal"), upload_to="uploads")
    header_tag=models.CharField(_("Tag"), max_length=200, blank=True)
    subcategory=models.ForeignKey(SubCategory, verbose_name=_("SubCategory"), on_delete=models.DO_NOTHING)
    approximate_duration=models.DecimalField(_("Duración Aproximada"), max_digits=4, decimal_places=2)
    with_reservation=models.BooleanField(_("Con Reservación"), default=False)

    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    last_update_date=models.DateTimeField(_("Fecha Actualizacion"), null=True, default=None)
    responsible=models.ForeignKey(CustomUser, verbose_name=_("Responsable"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural="Servicios"
    def __str__(self):
        return f"Servicio '{self.title}'"

# Other Classes
class ServiceAvailability(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Lunes'),
        ('TUE', 'Martes'),
        ('WED', 'Miércoles'),
        ('THU', 'Jueves'),
        ('FRI', 'Viernes'),
        ('SAT', 'Sábado'),
        ('SUN', 'Domingo'),
    ]

    service = models.ForeignKey(Service, verbose_name=_("Servicio"), on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField(_("Hora Inicio"), blank=True, null=True)
    end_time = models.TimeField(_("Hora Fin"), blank=True, null=True)

    def __str__(self):
        return f"{self.service.title} - {self.day}: {self.start_time} to {self.end_time}"

class ServiceImage(models.Model):
    image=models.ImageField(_("Imagen"), upload_to="uploads")
    service=models.ForeignKey(Service, verbose_name=_("Servicio"), on_delete=models.CASCADE)

class ServiceDetail(models.Model):
    description=models.TextField(_("Descripción"))
    service=models.ForeignKey(Service, verbose_name=_("Servicio"), on_delete=models.CASCADE)
    
class Reservation(models.Model):
    reservation_number=models.CharField(_("Nº Orden"), max_length=100)
    fullname=models.CharField(_("Nombres"), max_length=200)
    email=models.CharField(_("Correo Electrónico"), max_length=100)
    telephone=models.CharField(_("Telefono"), max_length=20)
    notes=models.TextField()
    subservices=models.JSONField(_("Subservicios"), default=list)

    date = models.DateField(_("Fecha Reserva"), max_length=10)
    time = models.TimeField(_("Hora Reserva"), blank=True, null=True)

    active=models.BooleanField(_("Activo"))
    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    last_update_date=models.DateTimeField(_("Fecha Actualizacion"), null=True, default=None)
    client=models.ForeignKey(CustomUser, verbose_name=_("Cliente"), on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, verbose_name=_("Servicio"), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural="Reservaiones"
    def __str__(self):
        return f"Reservación '{self.reservation_number} - {self.fullname}'"
    
    def save(self, *args, **kwargs):
        if not self.reservation_number:
            self.reservation_number = self.generate_reservation_number()
        super().save(*args, **kwargs)

    def generate_reservation_number(self):
        date_str = datetime.now().strftime('%Y%m%d')
        unique_id = str(uuid.uuid4()).split('-')[0] 
        return f'{date_str}-{unique_id}'