from typing import Dict
from json import loads

from django.utils.timezone import now
from django.conf import settings
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .permissions.custom import IsAdminUser
from ..models.auth import History, CustomUser, Action

"""
Crud API for the accounts module.
"""

def get_user(id:int):
    user:CustomUser=CustomUser.objects.filter(Q(id=id) & (Q(is_superuser=True) | Q(is_staff=True))).values("id", "password", "username", "email", "is_active", "is_superuser", "joined_date", "last_login")[0]     
    return user

class Accounts_APIView(APIView):
    permission_classes=[IsAdminUser]
    def get(self, request:HttpRequest, action, *args, **kwargs):
        if action == "accounts":
            obj:BaseManager[CustomUser]=CustomUser.objects.filter((Q(is_superuser=True) | Q(is_staff=True)))
            data=obj.values("id", "password", "username", "email", "is_active", "is_superuser", "joined_date", "last_login") 
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("Accion no encontrada.", status=status.HTTP_404_NOT_FOUND)

    def post(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            new_data=request.data
            new_data["last_update_date"]=now()
            
            user=CustomUser(**new_data)
            user.save()

            history=History()
            history.module="accounts"
            history.action=Action.CREACION.value
            history.datetime=now()
            history.responsible=responsible
            history.save()

            resp={
                "msg": f"Usuario '{user.username}' creado correctamente.",
                "data": get_user(user.id)
            }
            return Response(resp, status=status.HTTP_200_OK)
        except Exception as e:
            err=repr(e)
            if 'duplicate key' in err:
                value=err.split('The duplicate key value is (')[1].split(').')[0]
                resp=f'{value} ya existe!'
                return Response(resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            user_id=request.GET.get('account_id')
            new_data:Dict[str,str]=request.data
            new_data["last_update_date"]=now()

            user=CustomUser.objects.filter(Q(id=user_id) & (Q(is_superuser=True) | Q(is_staff=True)))
            has_user=user.first()
            if has_user is None:
                return Response(f"Usuario con ID '{user_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
            else:
                user.update(**new_data)
                history=History()
                history.module="accounts"
                history.action=Action.ACTUALIZACION.value
                history.datetime=now()
                history.responsible=responsible
                history.save()
            resp = {
                "msg": f"Usuario '{has_user.username}' actualizado correctamente.",
                "data": get_user(has_user.id)
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
            user_ids=loads(request.GET.get('account_ids'))

            user_names=[]
            for user_id in user_ids:
                user=CustomUser.objects.filter(Q(id=user_id) & (Q(is_superuser=True) | Q(is_staff=True)))
                has_user=user.first()
                if has_user is None:
                    return Response(f"Usuario con ID '{user_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
                else:
                    user.delete()
                    history=History()
                    history.module="accounts"
                    history.action=Action.ELIMINACION.value
                    history.datetime=now()
                    history.responsible=responsible
                    history.save()
                user_names.append(has_user.username)
                
            string_users_names=', '.join(user_names).rstrip(', ')
            return Response(f"Usuario(s) '{string_users_names}' eliminado(s) correctamente.", status=status.HTTP_200_OK)

        except Exception as e:
            if settings.DEBUG:
                raise e
            return Response(f"Error interno, por favor, intentelo mas tarde.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    