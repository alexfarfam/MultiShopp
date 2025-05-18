from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _

from .auth import CustomUser
from .products import Product
from .services import Service

# Main Class
class Comment(models.Model):
    description=models.TextField(_("Descripcion"))
    product=models.ForeignKey(Product, verbose_name=_("Producto"), on_delete=models.CASCADE, null=True)
    service=models.ForeignKey(Service, verbose_name=_("Servicio"), on_delete=models.CASCADE, null=True)
    starts=models.IntegerField(_("Estrellas"))
    deleted=models.BooleanField(_("Eliminado"), default=False)
    
    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    last_update_date=models.DateTimeField(_("Fecha Actualizacion"), null=True, default=None)
    responsible=models.ForeignKey(CustomUser, verbose_name=_("Responsable"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural="Comentarios"
    def __str__(self):
        return f"Comentario '{self.description}'"