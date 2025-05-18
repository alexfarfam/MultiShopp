from typing import Dict
from json import loads
import base64

from django.utils.timezone import now
from django.conf import settings
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.files.base import ContentFile

from ..models.auth import History, CustomUser, Action, ClientInfo

"""
Crud API for the ClientInfo module.
"""

def get_ClientInfo(id:int):
    client_info:ClientInfo=ClientInfo.objects.filter(pk=id).values("id", "fullname", "email_order", "telephone", "departament__name", "province__name", "district__name", "address", "reference")[0]     
    return client_info

class ClientInfos_APIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request:HttpRequest, action, *args, **kwargs):
        responsible:CustomUser=request.user
        data:BaseManager[ClientInfo]= ClientInfo.objects.filter(user=responsible).values("id", "fullname", "email_order", "telephone", "departament__name", "province__name", "district__name", "address", "reference")
        if data.count() == 0:
            return Response(f"Usuario no encontrado!", status=status.HTTP_404_NOT_FOUND)
        data=data[0]
        return Response(data, status=status.HTTP_200_OK)
        
    def post(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            ClientInfo=ClientInfo.objects.filter(user=responsible).first()
            if ClientInfo:
                return Response("Ya existe informacion para este usuario.", status=status.HTTP_400_BAD_REQUEST)
            new_data=request.data
            new_data["creation_date"]=now()
            new_data["last_update_date"]=now()
            new_data["responsible"]=responsible
            
            ClientInfo=ClientInfo(**new_data)
            ClientInfo.save()
            
            history=History()
            history.module="ClientInfo"
            history.action=Action.CREACION.value
            history.datetime=now()
            history.responsible=responsible
            history.save()

            resp={
                "msg": f"Datos guardados correctamente.",
                "data": get_ClientInfo(ClientInfo.id)
            }
            return Response(resp, status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            new_data:Dict[str,str]=request.data
            new_data["last_update_date"]=now()
            new_data["responsible"]=responsible

            ClientInfo=ClientInfo.objects.filter(user=responsible)
            has_ClientInfo=ClientInfo.first()
            if has_ClientInfo is None:
                return Response(f"Usuario no existe.", status=status.HTTP_404_NOT_FOUND)
            else:
                ClientInfo.update(**new_data)

                history=History()
                history.module="ClientInfo"
                history.action=Action.ACTUALIZACION.value
                history.datetime=now()
                history.responsible=responsible
                history.save()
            
            resp = {
                "msg": f"Datos actualizados correctamente.",
                "data": get_ClientInfo(ClientInfo.id)
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
            return Response("No implementado!", status=status.HTTP_501_NOT_IMPLEMENTED)
        except Exception as e:
            if settings.DEBUG:
                raise e
            return Response(f"Error interno, por favor, intentelo mas tarde.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    