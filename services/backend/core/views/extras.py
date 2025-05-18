from django.http import HttpRequest
from typing import Dict
from json import loads

from django.conf import settings
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes

from ..models import Extras, FAQ
from .permissions.custom import IsAdminUser
from ..models.auth import History, CustomUser, Action

"""
Crud API for extras data
"""
def get_faq(id:int):
    faq:FAQ=FAQ.objects.filter(pk=id).values("id", "answer", "question")[0]
    return faq

class Extras_APIView(APIView):

    def get(self, request:HttpRequest, action, *args, **kwargs):
        if action in ('about', 'company', 'history', 'workflow', 'support', 'privacy_policy', 'terms_condition'):
            extra=Extras.objects.first()

            if extra == None:
                return Response('No Encontrado!', status=status.HTTP_404_NOT_FOUND)
            
            data=extra.about
            if action == 'company':
                data=extra.company
            elif action == 'history':
                data=extra.history
            elif action == 'workflow':
                data=extra.workflow
            elif action == 'support':
                data=extra.support
            elif action == 'privacy_policy':
                data=extra.privacy_policy
            elif action == 'terms_condition':
                data=extra.terms_condition

            return Response(data, status=status.HTTP_200_OK)
        elif action == 'faqs':
            data=FAQ.objects.all().values('id', 'question', 'answer')
            return Response(data, status=status.HTTP_200_OK)
        elif action == 'admin':
            data=Extras.objects.first()
            dt={
                'about': '',
                'company': '',
                'history': '',
                'workflow': '',
                'support': '',
                'privacy_policy': '',
                'terms_condition': ''
            }
            if data != None:
                dt={
                    'about': data.about,
                    'company':data.company,
                    'history': data.history,
                    'workflow': data.workflow,
                    'support': data.support,
                    'privacy_policy': data.privacy_policy,
                    'terms_condition': data.terms_condition
                }

            return Response(dt, status=status.HTTP_200_OK)
        else: 
            return Response('Acción no Encontrada!', status=status.HTTP_404_NOT_FOUND)
        
    @permission_classes([IsAdminUser])
    def post(self, request:HttpRequest, action, *args, **kwargs):
        responsible:CustomUser=request.user
        new_data=request.data
        
        if action == 'extras':
            data=Extras.objects.first()
            if data:
                extra = Extras.objects.filter(pk=data.id)
                extra.update(**new_data)

                history=History()
                history.module="extras"
                history.action=Action.ACTUALIZACION.value
                history.datetime=now()
                history.responsible=responsible
                history.save()

                return Response('Datos actualizados correctamente!', status=status.HTTP_200_OK)      

            extra=Extras(**new_data)
            extra.save()

            history=History()
            history.module="extras"
            history.action=Action.CREACION.value
            history.datetime=now()
            history.responsible=responsible
            history.save()

            return Response('Datos guardados correctamente!', status=status.HTTP_200_OK)
        elif action == 'faq':
            faq=FAQ(**new_data)
            faq.save()

            resp={
                "msg": f"Pregunta '{faq.answer}' creada correctamente.",
                "data": get_faq(faq.id)
            }
            return Response(resp, status=status.HTTP_200_OK)
        else: 
            return Response('Acción no Encontrada!', status=status.HTTP_404_NOT_FOUND)
    
    @permission_classes([IsAdminUser])
    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            faq_id=request.GET.get('faq_id')
            new_data:Dict[str,str]=request.data
            new_data["last_update_date"]=now()

            faq=FAQ.objects.filter(pk=faq_id)
            has_faq=faq.first()
            if has_faq is None:
                return Response(f"FAQ con ID '{faq_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
            else:
                faq.update(**new_data)
                history=History()
                history.module="faq"
                history.action=Action.ACTUALIZACION.value
                history.datetime=now()
                history.responsible=responsible
                history.save()
            resp = {
                "msg": f"FAQ  actualizada correctamente.",
                "data": get_faq(has_faq.id)
            }
            return Response(resp, status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @permission_classes([IsAdminUser])
    def delete(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            faq_ids=loads(request.GET.get('faq_ids'))

            for faq_id in faq_ids:
                faq=FAQ.objects.filter(pk=int(faq_id))
                has_faq=faq.first()
                if has_faq is None:
                    return Response(f"FAQ con ID '{faq_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
                else:
                    faq.delete()
                    history=History()
                    history.module="faq"
                    history.action=Action.ELIMINACION.value
                    history.datetime=now()
                    history.responsible=responsible
                    history.save()
                
            return Response(f"FAQ(s) eliminada(s) correctamente.", status=status.HTTP_200_OK)

        except Exception as e:
            if settings.DEBUG:
                raise e
            return Response(f"Error interno, por favor, intentelo mas tarde.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
