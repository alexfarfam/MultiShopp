from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _

from .auth import CustomUser

# Main Class
class FAQ(models.Model):
    question=models.TextField(_('Pregunta'))
    answer=models.TextField(_('Respuesta'))
    
    creation_date=models.DateTimeField(_("Fecha Registro"), default=now)
    last_update_date=models.DateTimeField(_("Fecha Actualizacion"), null=True, default=None)
    responsible=models.ForeignKey(CustomUser, verbose_name=_("Responsable"), on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural="FAQ"
    def __str__(self):
        return f"Pregunta '{self.question} - {self.responsible.username}'"

class Extras(models.Model):
    about=models.TextField(_('Acerca de'))
    company=models.TextField(_('Compañia'))
    history=models.TextField(_('Historia'))
    workflow=models.TextField(_('Flujo de Trabajo'))
    support=models.TextField(_('Soporte'))
    privacy_policy=models.TextField(_('Política de Privacidad'))
    terms_condition=models.TextField(_('Política de Privacidad'))

    class Meta:
        verbose_name_plural="Extras"
    def __str__(self):
        return f"Extras"
    
