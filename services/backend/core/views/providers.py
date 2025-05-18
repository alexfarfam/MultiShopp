from typing import Dict
from json import loads
from typing import Dict

from django.utils.timezone import now
from django.conf import settings
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .permissions.custom import IsAdminUser
from ..models.auth import History, CustomUser, Action

"""
Crud API for the providers module.
"""

def get_provider(id:int):
    provider:CustomUser=CustomUser.objects.filter(pk=id, is_provider=True).values("id", "username", "email", "date_joined", "is_active", "last_login")[0]

    return provider

class Providers_APIView(APIView):
    permission_classes=[IsAdminUser]

    def get(self, request:HttpRequest, action, *args, **kwargs):
        try:
            provider_id=request.GET.get("provider_id")
            if action == "all":
                obj:BaseManager[CustomUser]=CustomUser.objects.filter(pk=provider_id, is_provider=True) if provider_id else CustomUser.objects.filter(is_provider=True)

                data=obj.values("id", "username", "email", "is_confirmed", "date_joined", "is_active", "last_login") 
                data=list(data)
                data_len=len(data)
                if provider_id:
                    if data_len == 0:
                        return Response(f"Proveedor con ID '{provider_id}' no encontrado!", status=status.HTTP_404_NOT_FOUND)
                    data=data[0]
                
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("Accion no encontrada.", status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError) as e:
            return Response("No encontrado!", status=status.HTTP_404_NOT_FOUND)
   
    def post(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
           raise NotImplemented
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            provider_id=request.GET.get('provider_id')
            new_data:Dict[str,str]={}
            new_data["last_update_date"]=now()
            new_data["is_active"] = request.data["is_active"]

            provider=CustomUser.objects.filter(pk=provider_id, is_provider=True)
            has_provider=provider.first()
            if has_provider is None:
                return Response(f"Proveedor con ID '{provider_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
            
            provider.update(**new_data)

            history=History()
            history.module="provider"
            history.action=Action.ACTUALIZACION.value
            history.datetime=now()
            history.responsible=responsible
            history.save()
            
            resp = {
                "msg": f"Proveedor '{has_provider.username}' actualizado correctamente.",
                "data": get_provider(has_provider.id)
            }
            return Response(resp, status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user

            provider_ids=loads(request.GET.get('provider_ids'))
            provider_titles=[]
            for provider_id in provider_ids:
                provider=CustomUser.objects.filter(pk=int(provider_id), is_provider=True)
                has_provider=provider.first()
                if has_provider is None:
                    return Response(f"Proveedor con ID '{provider_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
                else:
                    provider.delete()

                    history=History()
                    history.module="provider"
                    history.action=Action.ELIMINACION.value
                    history.datetime=now()
                    history.responsible=responsible
                    history.save()
                provider_titles.append(has_provider.username)
                
            string_providers_titles=', '.join(provider_titles).rstrip(', ')
            return Response(f"Proveedores(s) '{string_providers_titles}' eliminado(s) correctamente.", status=status.HTTP_200_OK)

        except Exception as e:
            if settings.DEBUG:
                raise e
            return Response(f"Error interno, por favor, intentelo mas tarde.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    