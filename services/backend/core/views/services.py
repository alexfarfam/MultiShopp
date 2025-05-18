from typing import Dict
from json import loads
import base64
from typing import Dict
from datetime import datetime

from django.utils.timezone import now
from django.conf import settings
from django.db.models.manager import BaseManager
from django.db.models import F, Avg, Sum, Q, IntegerField, Count
from django.db.models.functions import Coalesce
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.core.files.base import ContentFile

from .permissions.custom import IsProviderUser
from ..models.orders import OrderDetail
from ..models.categories import SubCategory
from ..models.services import Service, ServiceImage, ServiceAvailability, ServiceDetail
from ..models.auth import History, CustomUser, Action

"""
Crud API for the service module.
"""

def get_service(id:int, request:HttpRequest):
    service:Service=Service.objects.filter(pk=id).values("id", "title", "header_tag", "description", "main_image", "subcategory__id", "subcategory__title", "approximate_duration", "with_reservation")[0]
    service["main_image"]=f"{request.scheme}://{request.get_host()}/{service['main_image'] if service['main_image'] else ''}"

    availability=ServiceAvailability.objects.filter(service__id=id)
    availability_data = {}
    for item in availability:
        availability_data[item.day]={
            "start_time": item.start_time,
            "end_time": item.end_time
        }
    service["opening_hours"]=availability_data

    items=[]
    subservices=ServiceDetail.objects.filter(service__id=id)
    for item in subservices:
        items.append(item.description)
    service['subservices']=items          
    return service

class Services_APIView(APIView):
    def get(self, request:HttpRequest, action, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            service_id=request.GET.get("service_id")
            if action == "services":
                obj:BaseManager[Service]=Service.objects.filter(pk=service_id) if service_id else Service.objects.filter(responsible=responsible)

                data=obj.values("id", "title", "header_tag", "description", "main_image", "subcategory__id", "subcategory__title", "responsible__id", "approximate_duration", "with_reservation")              
                data=list(data)
                data_len=len(data)
                for x in range(data_len):
                    data[x]["main_image"]=f"{request.scheme}://{request.get_host()}/{data[x]['main_image'] if data[x]['main_image'] else ''}"
                
                for x in range(data_len):
                    availability=ServiceAvailability.objects.filter(service__id=data[x]["id"])
                    availability_data = {}
                    for item in availability:
                        availability_data[item.day]={
                            "start_time": item.start_time,
                            "end_time": item.end_time,
                        }
                    data[x]['opening_hours']=availability_data

                    items=[]
                    subservices=ServiceDetail.objects.filter(service__id=data[x]["id"])
                    for item in subservices:
                        items.append(item.description)
                    data[x]['subservices']=items                    

                if service_id:
                    if data_len == 0:
                        return Response(f"Servicio con ID '{service_id}' no encontrado!", status=status.HTTP_404_NOT_FOUND)
                    data=data[0]
                
                return Response(data, status=status.HTTP_200_OK)
            elif action == "images":
                data:BaseManager[ServiceImage]=ServiceImage.objects.filter(service_id=service_id).values("image", "id", name=F("image"))
                data=list(data)
                data_len=len(data)
                for x in range(data_len):
                    data[x]["image"]=f"{request.scheme}://{request.get_host()}/{data[x]['image'] if data[x]['image'] else ''}"

                return Response(data, status=status.HTTP_200_OK)
    
            elif action == "public":
                filter=request.GET.get('category_id')
                filter2=request.GET.get('subcategory_id')
                filter3=request.GET.get('top')

                obj:BaseManager[Service] = None
                if filter:
                    obj=Service.objects.filter(subcategory__category_id=filter)
                elif filter2:
                    obj=Service.objects.filter(subcategory_id=filter2)
                elif filter3:
                    if filter3 == 'discounts':
                        return Response([], status=status.HTTP_200_OK)

                    if filter3 == 'best-sellers':
                        top_service_ids = (
                            OrderDetail.objects
                            .values('service')
                            .annotate(total_sold=Sum('amount'))
                            .order_by('-total_sold')
                            .values_list('service', flat=True)[:10]
                        )
                        obj = Service.objects.filter(id__in=top_service_ids)
                    elif filter3 == 'newcomers':
                        obj=Service.objects.filter(creation_date__date = now()).order_by('-creation_date')
                    elif filter3 == 'promotions':
                        obj=Service.objects.exclude(header_tag="").order_by('-creation_date')
                else:
                    obj=Service.objects.order_by('-creation_date')

                data=obj.annotate(
                    orders=Coalesce(Sum('orderdetail__amount', output_field=IntegerField()), 0),
                    qualification=Coalesce(Avg('comment__starts', filter=Q(comment__deleted=False), output_field=IntegerField()), 0),
                    comments_count = Coalesce(Count('comment__starts', filter=Q(comment__deleted=False), output_field=IntegerField()), 0),
                ).values(
                    "id", "orders", "qualification", "comments_count", "title", "header_tag", "main_image", "subcategory__id", "subcategory__title", "subcategory__category_id", "subcategory__category__title", "last_update_date", "responsible__id", "approximate_duration", "with_reservation"
                ).order_by(*('-qualification', '-orders'))[:30]
                
                data=list(data)
                data_len=len(data)
                for x in range(data_len):
                    data[x]["main_image"]=f"{request.scheme}://{request.get_host()}/{data[x]['main_image'] if data[x]['main_image'] else ''}"
                return Response(data, status=status.HTTP_200_OK)
            
            elif action == "info":
                obj:BaseManager[Service]=Service.objects.filter(pk=service_id)
                if obj.count() == 0:
                    return Response(f"Servicio con ID '{service_id}' no encontrado!", status=status.HTTP_404_NOT_FOUND)
                
                data=obj.annotate(
                    orders=Coalesce(Sum('orderdetail__amount', output_field=IntegerField()), 0),
                    qualification=Coalesce(Avg('comment__starts', filter=Q(comment__deleted=False), output_field=IntegerField()), 0),
                    comments_count =Coalesce(Count('comment__starts', filter=Q(comment__deleted=False), output_field=IntegerField()), 0),
                ).values("id", "orders", "qualification", "comments_count", "title","description", "header_tag", "main_image", "subcategory__id", "subcategory__title", "last_update_date", "responsible__id", category__id=F("subcategory__category_id"), category__title=F("subcategory__category__title"))[0]
                
                data["main_image"]=f"{request.scheme}://{request.get_host()}/{data['main_image'] if data['main_image'] else ''}"
                
                return Response(data, status=status.HTTP_200_OK)
            
            elif action == "opening-hours":
                obj:BaseManager[Service]=Service.objects.filter(pk=service_id)
                data=obj.values("approximate_duration", "with_reservation")
                if obj.count() == 0:
                    return Response(f"Servicio con ID '{service_id}' no encontrado!", status=status.HTTP_404_NOT_FOUND)
                
                data=data[0]
                availability=ServiceAvailability.objects.filter(service__id=service_id)
                availability_data = []
                for item in availability:
                    availability_data.append({
                        "day": item.day,
                        "start_time": item.start_time,
                        "end_time": item.end_time,
                    })
                data['opening_hours']=availability_data

                return Response(data, status=status.HTTP_200_OK)
            
            elif action == "subservices":
                data:BaseManager[ServiceDetail]=ServiceDetail.objects.filter(service_id=service_id).values("description")
                return Response(data, status=status.HTTP_200_OK)
            
            else:
                return Response("Accion no encontrada.", status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError) as e:
            return Response("No encontrado!", status=status.HTTP_404_NOT_FOUND)
   
    @permission_classes([IsProviderUser])
    def post(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            new_data:dict=request.data

            new_data["subcategory"]=SubCategory.objects.get(pk=new_data["subcategory"])
            new_data["creation_date"]=now()
            new_data["last_update_date"]=now()
            new_data["responsible"]=responsible

            # Procesa y guarda la imagen base64 en ImageField
            image_data = new_data.pop('main_image', None)  # Extrae la imagen base64 del diccionario de datos
            images_data = new_data.pop('images', None) 
            opening_hours = new_data.pop('opening_hours', None)
            subservices = new_data.pop('subservices', None)
            service=Service(**new_data)
            if image_data:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]  # Determina la extensión del archivo
                image_data = ContentFile(base64.b64decode(imgstr), name=f'service_image__{now().strftime("%Y%m%d_%H%M%S")}.{ext}')
                service.main_image.save(image_data.name, image_data, save=True)  # Guarda la imagen en el campo ImageField
            service.save()

            ref=Service.objects.get(pk=service.id)
            if images_data:
                for img in images_data:
                    format, imgstr = img.split(';base64,')
                    ext = format.split('/')[-1] 
                    img = ContentFile(base64.b64decode(imgstr), name=f'service_image__{now().strftime("%Y%m%d_%H%M%S")}.{ext}')
                    pi=ServiceImage()
                    pi.service=ref
                    pi.image.save(img.name, img, save=True)  # Guarda la imagen en el campo ImageField
                    pi.save()               
            
            if subservices:
                for sub in subservices:
                    sd=ServiceDetail()
                    sd.service=ref
                    sd.description=sub
                    sd.save()

            for day in opening_hours:
                entry=opening_hours[day]
                start_time = entry.get('start_time')
                end_time = entry.get('end_time')
                    
                availability = ServiceAvailability(service=service, day=day)
                if start_time != None:
                    availability.start_time=datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                if end_time != None:
                    availability.end_time=datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                availability.save()
        
            history=History()
            history.module="service"
            history.action=Action.CREACION.value
            history.datetime=now()
            history.responsible=responsible
            history.save()

            resp={
                "msg": f"Servicio '{service.title}' creado correctamente.",
                "data": get_service(service.id, request)
            }
            return Response(resp, status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @permission_classes([IsProviderUser])
    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            service_id=request.GET.get('service_id')
            new_data:Dict[str,str]=request.data
            new_data["subcategory"]=SubCategory.objects.get(pk=new_data["subcategory"])
            new_data["last_update_date"]=now()
            new_data["responsible"]=responsible

            service=Service.objects.filter(pk=service_id)
            has_service=service.first()
            if has_service is None:
                return Response(f"Servicio con ID '{service_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
            elif has_service.responsible.id != responsible.id:
                return Response(f"No tienes los permisos para actualizar este servicio.", status=status.HTTP_401_UNAUTHORIZED)
            else:
                # Procesa y guarda la imagen base64 en ImageField
                image_data = new_data.pop('main_image', None)  # Extrae la imagen base64 del diccionario de datos
                images_data = new_data.pop('images', None)
                opening_hours = new_data.pop('opening_hours', None)
                subservices = new_data.pop('subservices', None)

                service = Service.objects.get(pk=service_id)
                for key, value in new_data.items():
                    setattr(service, key, value)
                
                if image_data and not image_data.startswith('http'):
                    format, imgstr = image_data.split(';base64,')
                    ext = format.split('/')[-1]  # Determina la extensión del archivo
                    image_data = ContentFile(base64.b64decode(imgstr), name=f'service_image__{now().strftime("%Y%m%d_%H%M%S")}.{ext}')
          
                    service.main_image.save(image_data.name, image_data, save=True)  # Guarda la imagen en el campo ImageField
                service.save()

                if images_data: 
                    for img in images_data:
                        if not img.startswith('http'):
                            format, imgstr = img.split(';base64,')
                            ext = format.split('/')[-1]  # Determina la extensión del archivo
                            img = ContentFile(base64.b64decode(imgstr), name=f'service_image__{now().strftime("%Y%m%d_%H%M%S")}.{ext}')
                
                            pi=ServiceImage()
                            pi.service=service
                            pi.image.save(img.name, img, save=True)  # Guarda la imagen en el campo ImageField
                            pi.save()                     

                ServiceAvailability.objects.filter(service=service).delete()
                for day in opening_hours:
                    entry=opening_hours[day]
                    start_time = entry.get('start_time')
                    end_time = entry.get('end_time')
                    
                    availability = ServiceAvailability(service=service, day=day)
                    if start_time != None:
                        availability.start_time=datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                    if end_time != None:
                        availability.end_time=datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                    availability.save()

                ServiceDetail.objects.filter(service=service).delete()
                for sub in subservices:
                    sd = ServiceDetail(service=service, description=sub)
                    sd.save()

                history=History()
                history.module="service"
                history.action=Action.ACTUALIZACION.value
                history.datetime=now()
                history.responsible=responsible
                history.save()
            
            resp = {
                "msg": f"Servicio '{new_data['title']}' actualizado correctamente.",
                "data": get_service(service.id, request)
            }
            return Response(resp, status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @permission_classes([IsProviderUser])
    def delete(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            if action == "image":
                img_id=request.GET.get('img_id')
                img_service=ServiceImage.objects.filter(pk=img_id)
                has_img=img_service.first()
                if has_img is None:
                    return Response(f"Imagen con ID '{img_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
                elif has_img.service.responsible.id != responsible.id:
                    return Response(f"No tienes los permisos para eliminar esta imagen.", status=status.HTTP_401_UNAUTHORIZED)  
                else:
                    has_img.delete()
                    return Response(f"Imagen con ID '{img_id}' eliminada correctamente!")

            service_ids=loads(request.GET.get('service_ids'))
            service_titles=[]
            for service_id in service_ids:
                service=Service.objects.filter(pk=int(service_id))
                has_service=service.first()
                if has_service is None:
                    return Response(f"Servicio con ID '{service_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
                elif has_service.responsible.id != responsible.id:
                    return Response(f"No tienes los permisos para eliminar este servicio.", status=status.HTTP_401_UNAUTHORIZED)
            
                else:
                    service.delete()
                    history=History()
                    history.module="service"
                    history.action=Action.ELIMINACION.value
                    history.datetime=now()
                    history.responsible=responsible
                    history.save()
                service_titles.append(has_service.title)
                
            string_services_titles=', '.join(service_titles).rstrip(', ')
            return Response(f"Servicio(s) '{string_services_titles}' eliminado(s) correctamente.", status=status.HTTP_200_OK)

        except Exception as e:
            if settings.DEBUG:
                raise e
            return Response(f"Error interno, por favor, intentelo mas tarde.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    