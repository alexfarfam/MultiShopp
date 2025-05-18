from typing import Dict
from json import loads
import base64

from django.utils.timezone import now
from django.conf import settings
from django.db.models import F
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.core.files.base import ContentFile

from ..models.categories import Category
from ..models.auth import History, CustomUser, Action

"""
Crud API for the categories module.
"""

def get_category(id:int, request:HttpRequest):
    category:Category=Category.objects.filter(pk=id).values("id", "title", "description", "image")[0]
    category["image"]=f"{request.scheme}://{request.get_host()}/{category['image'] if category['image'] else ''}"
    return category

class Categories_APIView(APIView):
    def get(self, request:HttpRequest, action, *args, **kwargs):
        try:
            category_id=request.GET.get("category_id")
            if action == "categories":
                obj:BaseManager[Category]= Category.objects.filter(pk=category_id) if category_id else Category.objects.all()

                data=obj.values("id", "title", "description", "image")
                if category_id:
                    if data.count() == 0:
                        return Response(f"Categoria con ID '{category_id}' no encontrada!", status=status.HTTP_404_NOT_FOUND)
                    data=data[0]
                    data["image"]=f"{request.scheme}://{request.get_host()}/{data['image'] if data['image'] else ''}"
                else:
                    for category in data:
                        category["image"]=f"{request.scheme}://{request.get_host()}/{category['image'] if category['image'] else ''}"
                
                return Response(data, status=status.HTTP_200_OK)
            
            elif action == "public":
                obj:BaseManager[Category]= Category.objects.all()

                data=obj.values("id", "title", "description", "image")
                for category in data:
                    category["image"]=f"{request.scheme}://{request.get_host()}/{category['image'] if category['image'] else ''}"
                return Response(data, status=status.HTTP_200_OK)
            
            elif action == "options":
                obj:BaseManager[Category]= Category.objects.all()
                data=obj.values(value=F("id"), label=F("title"))
                for category in data:
                    category["value"]=str(category["value"])

                return Response(data, status=status.HTTP_200_OK)
            elif action == "info":
                obj:BaseManager[Category]=Category.objects.filter(pk=category_id)
                if obj.count() == 0:
                    return Response(f"Categoria con ID '{category_id}' no encontrada!", status=status.HTTP_404_NOT_FOUND)
                    
                data=obj.values('title')[0]
                return Response(data, status=status.HTTP_200_OK)
            
            else:
                return Response("Accion no encontrada.", status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError):
            return Response('No Encontrado!', status=status.HTTP_404_NOT_FOUND)
       
    @permission_classes([IsAuthenticated])
    def post(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            new_data=request.data

            new_data["creation_date"]=now()
            new_data["responsible"]=responsible
            
            # Procesa y guarda la imagen base64 en ImageField
            image_data = new_data.pop('image', None)  # Extrae la imagen base64 del diccionario de datos
            category=Category(**new_data)
            if image_data:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]  # Determina la extensión del archivo
                image_data = ContentFile(base64.b64decode(imgstr), name=f'image_{now().strftime("%Y%m%d_%H%M%S")}.{ext}')

                category.image.save(image_data.name, image_data, save=True)  # Guarda la imagen en el campo ImageField

            category.save()
            
            history=History()
            history.module="category"
            history.action=Action.CREACION.value
            history.datetime=now()
            history.responsible=responsible
            history.save()

            resp={
                "msg": f"Categoria '{category.title}' creada correctamente.",
                "data": get_category(category.id, request)
            }
            return Response(resp, status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @permission_classes([IsAuthenticated])
    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            category_id=request.GET.get('category_id')
            new_data:Dict[str,str]=request.data
            new_data["last_update_date"]=now()
            new_data["responsible"]=responsible

            category=Category.objects.filter(pk=category_id)
            has_category=category.first()
            if has_category is None:
                return Response(f"Categoria con ID '{category_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
            elif not responsible.is_staff:
                return Response(f"No tienes los permisos para actualizar esta categoria.", status=status.HTTP_401_UNAUTHORIZED)
            else:
                # Procesa y guarda la imagen base64 en ImageField
                image_data = new_data.pop('image', None)  # Extrae la imagen base64 del diccionario de datos
                
                category = Category.objects.get(pk=category_id)
                for key, value in new_data.items():
                    setattr(category, key, value)
                
                if image_data and not image_data.startswith('http'):
                    format, imgstr = image_data.split(';base64,')
                    ext = format.split('/')[-1]  # Determina la extensión del archivo
                    image_data = ContentFile(base64.b64decode(imgstr), name=f'image_{now().strftime("%Y%m%d_%H%M%S")}.{ext}')
          
                    category.image.save(image_data.name, image_data, save=True)  # Guarda la imagen en el campo ImageField
                category.save()
                
                history=History()
                history.module="category"
                history.action=Action.ACTUALIZACION.value
                history.datetime=now()
                history.responsible=responsible
                history.save()
            
            resp = {
                "msg": f"Categoria '{new_data['title']}' actualizada correctamente.",
                "data": get_category(category.id, request)
            }
            return Response(resp, status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @permission_classes([IsAuthenticated])
    def delete(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            category_ids=loads(request.GET.get('category_ids'))

            category_titles=[]
            for category_id in category_ids:
                category=Category.objects.filter(pk=int(category_id))
                has_category=category.first()
                if has_category is None:
                    return Response(f"Categoria con ID '{category_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
                elif not responsible.is_staff:
                    return Response(f"No tienes los permisos para eliminar esta categoria.", status=status.HTTP_401_UNAUTHORIZED)
                else:
                    category.delete()
                    history=History()
                    history.module="category"
                    history.action=Action.ELIMINACION.value
                    history.datetime=now()
                    history.responsible=responsible
                    history.save()
                category_titles.append(has_category.title)
                
            string_categorys_titles=', '.join(category_titles).rstrip(', ')
            return Response(f"Categoria(s) '{string_categorys_titles}' eliminada(s) correctamente.", status=status.HTTP_200_OK)

        except Exception as e:
            if settings.DEBUG:
                raise e
            return Response(f"Error interno, por favor, intentelo mas tarde.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    