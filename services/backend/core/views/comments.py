from typing import Dict
from json import loads

from django.utils.timezone import now
from django.conf import settings
from django.db.models import Q
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .services import Service
from .products import Product
from ..models.comments import Comment
from ..models.auth import History, CustomUser, Action

"""
Crud API for the comments module.
"""

def get_comment(id:int):
    comment:Comment=Comment.objects.filter(pk=id, deleted=False).values("id", "description", "starts", "creation_date", "product__title", "service__title", "responsible__username", "responsible__id")[0]     
    return comment

class Comments_APIView(APIView):
    def get(self, request:HttpRequest, action, *args, **kwargs):
        responsible=request.user
        if action == "comments":
            if not responsible.is_authenticated or not responsible.is_provider:
                return Response("Se requiere autenticacion para acceder a este recurso.", status=status.HTTP_403_FORBIDDEN)
            
            obj:BaseManager[Comment]= Comment.objects.filter(    
                (Q(product__responsible__id=responsible.id) | Q(service__responsible__id=responsible.id)) &
                (Q(product__isnull=False) | Q(service__isnull=False))
            ) 
            data=obj.values("id", "description", "starts", "creation_date", "product__title", "service__title", "responsible__username", "creation_date", "deleted").order_by('-creation_date')
                
            return Response(data, status=status.HTTP_200_OK)
        
        elif action == "public":
            item_id=request.GET.get('item_id')
            initial=request.GET.get('initial')
            is_service=request.GET.get('is_service') == "1"
            obj:BaseManager[Comment]=None

            if initial == '1':
                obj = Comment.objects.filter(service_id=item_id, deleted=False).order_by("-creation_date")[:4] if is_service else Comment.objects.filter(product_id=item_id, deleted=False).order_by("-creation_date")[:4]
            else:
                obj = Comment.objects.filter(service_id=item_id, deleted=False).order_by("-creation_date") if is_service else Comment.objects.filter(product_id=item_id, deleted=False).order_by("-creation_date")

            data=obj.values("id", "description", "starts", "creation_date", "service__title", "product__title", "responsible__username", "responsible__id")
            return Response({
                "comments": data,
                "count": Comment.objects.filter(service_id=item_id, deleted=False).count() if is_service else Comment.objects.filter(product_id=item_id, deleted=False).count()
            }, status=status.HTTP_200_OK)
        else:
            return Response("Accion no encontrada.", status=status.HTTP_404_NOT_FOUND)

    @permission_classes([IsAuthenticated])
    def post(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user 
            new_data=request.data

            new_data["product"]=None if new_data["product"] == "" else Product.objects.get(pk=new_data["product"])
            new_data["service"]=None if new_data["service"] == "" else Service.objects.get(pk=new_data["service"])
            new_data["creation_date"]=now()
            new_data["last_update_date"]=now()
            new_data["responsible"]=responsible
            
            comment=Comment(**new_data)
            comment.save()
            
            history=History()
            history.module="comment"
            history.action=Action.CREACION.value
            history.datetime=now()
            history.responsible=responsible
            history.save()

            return Response({
                'msg': "Comentario guardado correctamente!",
                "data": get_comment(comment.id)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @permission_classes([IsAuthenticated])
    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            comment_id=request.GET.get('comment_id')

            comment=Comment.objects.filter(pk=comment_id)
            has_comment=comment.first()
            if has_comment is None:
                return Response(f"Comentario con ID '{comment_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
            elif has_comment.responsible.id != responsible.id:
                return Response(f"No tienes los permisos para {'eliminar' if action == 'delete' else 'actualizar'} este Comentario.", status=status.HTTP_401_UNAUTHORIZED)
            else:
                if action == "delete":
                    comment.update(**{'deleted': True})
                else:
                    new_data:Dict[str,str]=request.data
                    new_data["product"]=None if new_data["product"] == "" else Product.objects.get(pk=new_data["product"])
                    new_data["service"]=None if new_data["service"] == "" else Service.objects.get(pk=new_data["service"])
                    new_data["last_update_date"]=now()
                    new_data["responsible"]=responsible
                    comment.update(**new_data)
                
                history=History()
                history.module="comment"
                history.action=Action.ELIMINACION.value if action == 'delete' else Action.ACTUALIZACION.value
                history.datetime=now()
                history.responsible=responsible
                history.save()
            
            return Response({
                "msg": f"Comentario {'eliminado' if action == 'delete' else 'actualizado'} correctamente!",
                "data": {} if action == 'delete' else get_comment(comment_id) 
            }, status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @permission_classes([IsAuthenticated])
    def delete(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            comment_ids=loads(request.GET.get('comment_ids'))

            for comment_id in comment_ids:
                comment=Comment.objects.filter(pk=int(comment_id))
                has_comment=comment.first()
                item_responsible=(has_comment.product.responsible.pk if has_comment.product else has_comment.service.responsible.pk)
                if has_comment is None:
                    return Response(f"Comentario con ID '{comment_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
                elif (responsible.id != has_comment.responsible.id) or not (responsible.pk == item_responsible):
                    return Response(f"No tienes los permisos para eliminar este Comentario.", status=status.HTTP_401_UNAUTHORIZED)
                else:
                    comment.delete()
                    history=History()
                    history.module="comment"
                    history.action=Action.ELIMINACION.value
                    history.datetime=now()
                    history.responsible=responsible
                    history.save()
                
            return Response(f"Comentario(s) eliminado(s) correctamente.", status=status.HTTP_200_OK)

        except Exception as e:
            if settings.DEBUG:
                raise e
            return Response(f"Error interno, por favor, intentelo mas tarde.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    