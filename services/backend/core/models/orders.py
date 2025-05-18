from datetime import datetime
import uuid

from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _

from .products import Product
from .services import Service
from .auth import CustomUser, Province, Locality

# Main Class
class Order(models.Model):
    order_number=models.CharField(_("Nº Orden"), max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fullname=models.CharField(_("Nombres"), max_length=200)
    email=models.CharField(_("Correo Electronico"), max_length=100)
    telephone=models.CharField(_("Telefono"), max_length=20)
    province=models.ForeignKey(Province, verbose_name=_("Provincia"), on_delete=models.CASCADE)
    locality=models.ForeignKey(Locality, verbose_name=_("Localidad"), on_delete=models.CASCADE)
    city=models.CharField(_("Ciudad/Pueblo"), max_length=100)
    address=models.CharField(_("Direccion"), max_length=500)
    reference=models.URLField(_("Referencia"), max_length=500)
    source_detail = models.CharField(_("Origen Detalle"), max_length=50)
    provider_id=models.IntegerField(default=-1)
    
    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    last_update_date=models.DateTimeField(_("Fecha Actualizacion"), null=True, default=None)
    client=models.ForeignKey(CustomUser, verbose_name=_("Cliente"), on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural="Pedidos"
    def __str__(self):
        return f"Pedido '{self.order_number} - {self.fullname}'"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        date_str = datetime.now().strftime('%Y%m%d')
        unique_id = str(uuid.uuid4()).split('-')[0]  # Use a portion of UUID for uniqueness
        return f'{date_str}-{unique_id}'
    
# Aditional Classes
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("Pedido"), on_delete=models.CASCADE)
    title=models.CharField(_("Titulo"), max_length=200, blank=True)
    product = models.ForeignKey(Product, verbose_name=_("Producto"), on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, verbose_name=_("Servicio"), on_delete=models.CASCADE, null=True, blank=True)

    amount=models.DecimalField(_("Cantidad"), max_digits=18, decimal_places=2)
    price=models.DecimalField(_("Precio"), max_digits=18, decimal_places=2)
    discount=models.DecimalField(_("Descuento"), max_digits=18, decimal_places=2)
    total=models.DecimalField(_("Total"), max_digits=18, decimal_places=2)
    options=models.JSONField(default=list)

    class Meta:
        verbose_name_plural="Pedidos"
    def __str__(self):
        return f'Pedido {self.product.title} ({self.amount})'