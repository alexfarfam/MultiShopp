from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _

from .auth import CustomUser

# Main Class
class Category(models.Model):
    title=models.CharField(_("Titulo"), max_length=200, blank=True)
    description=models.CharField(_("Descripcion"), max_length=200, blank=True)
    image=models.ImageField(_("Imagen"), upload_to="uploads")

    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    last_update_date=models.DateTimeField(_("Fecha Actualizacion"), null=True, default=None)
    responsible=models.ForeignKey(CustomUser, verbose_name=_("Responsable"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural="Categorias"
    def __str__(self):
        return f"Categoria '{self.title}'"
    
class SubCategory(models.Model):
    title=models.CharField(_("Titulo"), max_length=200, blank=True)
    description=models.CharField(_("Descripcion"), max_length=200, blank=True)
    image=models.ImageField(_("Imagen"), upload_to="uploads")
    category=models.ForeignKey(Category, verbose_name=_("Categoria"), on_delete=models.CASCADE)

    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    last_update_date=models.DateTimeField(_("Fecha Actualizacion"), null=True, default=None)
    responsible=models.ForeignKey(CustomUser, verbose_name=_("Responsable"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural="SubCategorias"
    def __str__(self):
        return f"SubCategoria '{self.title}'"
    
