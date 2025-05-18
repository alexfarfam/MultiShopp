from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _

from .categories import SubCategory
from .auth import CustomUser

# Main Class 
class Product(models.Model):
    title=models.CharField(_("Titulo"), max_length=200, blank=True)
    header_tag=models.CharField(_("Tag"), max_length=200, blank=True)
    description=models.TextField(_("Descripcion"))
    price=models.DecimalField(_("Precio"), max_digits=18, decimal_places=2)
    discount=models.DecimalField(_("Descuento"), max_digits=18, decimal_places=2)
    reference_price=models.DecimalField(_("Precio Referencia"), max_digits=18, decimal_places=2)
    main_image=models.ImageField(_("Imagen"), upload_to="uploads")
    subcategory=models.ForeignKey(SubCategory, verbose_name=_("SubCategory"), on_delete=models.DO_NOTHING)

    show_offerts=models.BooleanField("Mostrar Ofertas", default=True)

    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    last_update_date=models.DateTimeField(_("Fecha Actualizacion"), null=True, default=None)
    responsible=models.ForeignKey(CustomUser, verbose_name=_("Responsable"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural="Productos"
    def __str__(self):
        return f"Producto '{self.title}'"
    
# Other Classes
class ProductImage(models.Model):
    image=models.ImageField(_("Imagen"), upload_to="uploads")
    product=models.ForeignKey(Product, verbose_name=_("Producto"), on_delete=models.CASCADE)

class ProductOption(models.Model):
    title=models.CharField(_("Titulo"), max_length=200, blank=True)
    values=models.JSONField(default=list)
    product=models.ForeignKey(Product, verbose_name=_("Producto"), on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="Productos Opciones"
    def __str__(self):
        return f"Opcion Producto '{self.product.title}'"

class ProductOffer(models.Model):
    title=models.CharField(_("Titulo"), max_length=200, blank=True)
    header_tag=models.CharField(_("Tag"), max_length=200, blank=True)
    amount=models.IntegerField(_("Cantidad"))
    price=models.DecimalField(_("Precio"), max_digits=18, decimal_places=2)
    reference_price=models.DecimalField(_("Precio Referencia"), max_digits=18, decimal_places=2)
    discount=models.DecimalField(_("Descuento"), max_digits=18, decimal_places=2)
    product=models.ForeignKey(Product, verbose_name=_("Producto"), on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural="Oferta Producto"
    def __str__(self):
        return f"Oferta Producto '{self.product.title}'"
