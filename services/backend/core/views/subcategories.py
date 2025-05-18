from typing import Dict
from json import loads
import base64

from django.utils.timezone import now
from django.conf import settings
from django.db.models.manager import BaseManager
from django.db.models import F
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.core.files.base import ContentFile

from ..models.categories import SubCategory, Category
from ..models.auth import History, CustomUser, Action
from .permissions.custom import IsAdminUser

"""
Crud API for the subcategories module.
"""

def get_subcategory(id:int, request:HttpRequest):
    subcategory:SubCategory=SubCategory.objects.filter(pk=id).values("id", "title", "description", "category__title","image")[0]
    subcategory["image"]=f"{request.scheme}://{request.get_host()}/{subcategory['image'] if subcategory['image'] else ''}"
    
    return subcategory

class SubCategories_APIView(APIView):
    def get(self, request:HttpRequest, action, *args, **kwargs):
        try:
            subcategory_id=request.GET.get("subcategory_id")
            if action == "subcategories":
                obj:BaseManager[SubCategory]=SubCategory.objects.filter(pk=subcategory_id) if subcategory_id else SubCategory.objects.all()

                data=obj.values("id", "title", "description", "image", "category__id", "category__title") 
                if subcategory_id:
                    if data.count() == 0:
                        return Response(f"SubCategoria con ID '{subcategory_id}' no encontrada!", status=status.HTTP_404_NOT_FOUND)
                    data=data[0]
                    data["image"]=f"{request.scheme}://{request.get_host()}/{data['image'] if data['image'] else ''}"
                else:
                    for subcategory in data:
                        subcategory["category__id"]=str(subcategory["category__id"])
                        subcategory["image"]=f"{request.scheme}://{request.get_host()}/{subcategory['image'] if subcategory['image'] else ''}"
                
                return Response(data, status=status.HTTP_200_OK)
            
            elif action == "public":
                filter=request.GET.get('category_id')
                obj:BaseManager[SubCategory]=SubCategory.objects.filter(category_id=filter)

                data=obj.values("id", "title", "description", "image")
                for subcategory in data:
                    subcategory["image"]=f"{request.scheme}://{request.get_host()}/{subcategory['image'] if subcategory['image'] else ''}"
                return Response(data, status=status.HTTP_200_OK)
            elif action == "options":
                obj:BaseManager[SubCategory]= SubCategory.objects.all()
                data=obj.values(value=F("id"), label=F("title"))
                for subcategory in data:
                    subcategory["value"]=str(subcategory["value"])
                return Response(data, status=status.HTTP_200_OK)
            
            elif action == "info":
                obj:BaseManager[SubCategory]=SubCategory.objects.filter(pk=subcategory_id)
                if obj.count() == 0:
                    return Response(f"SubCategoria con ID '{subcategory_id}' no encontrada!", status=status.HTTP_404_NOT_FOUND)
                
                data=obj.values('title', 'category__id', 'category__title')[0]
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("Accion no encontrada.", status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError):
            return Response('No Encontrado!', status=status.HTTP_404_NOT_FOUND)
        
    @permission_classes([IsAdminUser])
    def post(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            new_data=request.data

            new_data["category"]=Category.objects.get(pk=new_data["category"])
            new_data["creation_date"]=now()
            new_data["responsible"]=responsible
            
            # Procesa y guarda la imagen base64 en ImageField
            image_data = new_data.pop('image', None)  # Extrae la imagen base64 del diccionario de datos
            subcategory=SubCategory(**new_data)
            if image_data:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]  # Determina la extensión del archivo
                image_data = ContentFile(base64.b64decode(imgstr), name=f'image_{now().strftime("%Y%m%d_%H%M%S")}.{ext}')

                subcategory.image.save(image_data.name, image_data, save=True)  # Guarda la imagen en el campo ImageField

            subcategory.save()
            
            history=History()
            history.module="subcategory"
            history.action=Action.CREACION.value
            history.datetime=now()
            history.responsible=responsible
            history.save()

            resp={
                "msg": f"SubCategoria '{subcategory.title}' creada correctamente.",
                "data": get_subcategory(subcategory.id, request)
            }
            return Response(resp, status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @permission_classes([IsAdminUser])
    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            subcategory_id=request.GET.get('subcategory_id')
            new_data:Dict[str,str]=request.data
            new_data["category"]=Category.objects.get(pk=new_data["category"])
            new_data["last_update_date"]=now()
            new_data["responsible"]=responsible

            subcategory=SubCategory.objects.filter(pk=subcategory_id)
            has_subcategory=subcategory.first()
            if has_subcategory is None:
                return Response(f"SubCategoria con ID '{subcategory_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
            else:
                # Procesa y guarda la imagen base64 en ImageField
                image_data = new_data.pop('image', None)  # Extrae la imagen base64 del diccionario de datos
                
                subcategory = SubCategory.objects.get(pk=subcategory_id)
                for key, value in new_data.items():
                    setattr(subcategory, key, value)
                
                if image_data and not image_data.startswith('http'):
                    format, imgstr = image_data.split(';base64,')
                    ext = format.split('/')[-1]  # Determina la extensión del archivo
                    image_data = ContentFile(base64.b64decode(imgstr), name=f'image_{now().strftime("%Y%m%d_%H%M%S")}.{ext}')
          
                    subcategory.image.save(image_data.name, image_data, save=True)  # Guarda la imagen en el campo ImageField
                subcategory.save()
                
                history=History()
                history.module="subcategory"
                history.action=Action.ACTUALIZACION.value
                history.datetime=now()
                history.responsible=responsible
                history.save()
            
            resp = {
                "msg": f"SubCategoria '{new_data['title']}' actualizada correctamente.",
                "data": get_subcategory(subcategory.id, request)
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
            subcategory_ids=loads(request.GET.get('subcategory_ids'))

            subcategory_titles=[]
            for subcategory_id in subcategory_ids:
                subcategory=SubCategory.objects.filter(pk=int(subcategory_id))
                has_subcategory=subcategory.first()
                if has_subcategory is None:
                    return Response(f"SubCategoria con ID '{subcategory_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
                else:
                    subcategory.delete()
                    history=History()
                    history.module="subcategory"
                    history.action=Action.ELIMINACION.value
                    history.datetime=now()
                    history.responsible=responsible
                    history.save()
                subcategory_titles.append(has_subcategory.title)
                
            string_subcategorys_titles=', '.join(subcategory_titles).rstrip(', ')
            return Response(f"SubCategoria(s) '{string_subcategorys_titles}' eliminada(s) correctamente.", status=status.HTTP_200_OK)

        except Exception as e:
            if settings.DEBUG:
                raise e
            return Response(f"Error interno, por favor, intentelo mas tarde.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    