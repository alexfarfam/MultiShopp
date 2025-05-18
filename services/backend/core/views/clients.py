from typing import Dict
from json import loads

from django.utils.timezone import now
from django.conf import settings
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models.auth import History, CustomUser, Action

"""
Crud API for the clients module.
"""

def get_client(id:int):
    client:CustomUser=CustomUser.objects.filter(pk=id, is_superuser=0, is_staff=0, is_provider=0).values("id", "password", "username", "email", "is_active", "is_confirmed", "joined_date")[0]     
    return client

class Clients_APIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request:HttpRequest, action, *args, **kwargs):
        client_id=request.GET.get("client_id")
        if action == "clients":
            obj:BaseManager[CustomUser]=CustomUser.objects.filter(pk=client_id, is_superuser=0, is_staff=0, is_provider=0) if client_id else CustomUser.objects.filter(is_superuser=0, is_staff=0, is_provider=0)

            data=obj.values("id", "password", "username", "email", "is_active", "last_login", "is_confirmed", "joined_date") if client_id else obj.values("id", "password", "username", "email", "is_active", "last_login", "is_confirmed", "joined_date") 
            if client_id:
                if data.count() == 0:
                    return Response(f"Cliente con ID '{client_id}' no encontrado!", status=status.HTTP_404_NOT_FOUND)
                data=data[0]
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("Accion no encontrada.", status=status.HTTP_404_NOT_FOUND)

    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            client_id=request.GET.get('client_id')
            new_data:Dict[str,str]=request.data
            new_data["last_update_date"]=now()

            client=CustomUser.objects.filter(pk=client_id, is_superuser=0, is_staff=0, is_provider=0)
            has_client=client.first()
            if has_client is None:
                return Response(f"Cliente con ID '{client_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
            elif not responsible.is_staff:
                return Response(f"No tienes los permisos para actualizar este Cliente.", status=status.HTTP_401_UNAUTHORIZED)
            else:
                client.update(**new_data)
                history=History()
                history.module="client"
                history.action=Action.ACTUALIZACION.value
                history.datetime=now()
                history.responsible=responsible
                history.save()
            resp = {
                "msg": f"Cliente '{has_client.username}' actualizado correctamente.",
                "data": get_client(has_client.id)
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
            client_ids=loads(request.GET.get('client_ids'))

            client_titles=[]
            for client_id in client_ids:
                client=CustomUser.objects.filter(pk=int(client_id), is_superuser=0, is_staff=0, is_provider=0)
                has_client=client.first()
                if has_client is None:
                    return Response(f"Cliente con ID '{client_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
                elif not responsible.is_staff:
                    return Response(f"No tienes los permisos para eliminar este client.", status=status.HTTP_401_UNAUTHORIZED)
                else:
                    client.delete()
                    history=History()
                    history.module="client"
                    history.action=Action.ELIMINACION.value
                    history.datetime=now()
                    history.responsible=responsible
                    history.save()
                client_titles.append(has_client.username)
                
            string_clients_titles=', '.join(client_titles).rstrip(', ')
            return Response(f"Cliente(s) '{string_clients_titles}' eliminado(s) correctamente.", status=status.HTTP_200_OK)

        except Exception as e:
            if settings.DEBUG:
                raise e
            return Response(f"Error interno, por favor, intentelo mas tarde.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    