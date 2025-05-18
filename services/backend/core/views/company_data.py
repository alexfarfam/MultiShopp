import base64

from django.http import HttpRequest
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from django.core.files.base import ContentFile

from ..models import CompanyInfo
from .permissions.custom import IsAdminUser
from ..models.auth import History, CustomUser, Action

"""
Crud API for the company data module.
"""
class CompanyData_APIView(APIView):

    def get(self, request:HttpRequest, action, *args, **kwargs):
        data=CompanyInfo.objects.values("id", "company_name", "logo", "url_facebook", "url_instagram", "customer_service_email", "customer_service_telephone", "whatsapp_telephone", "service_price").first()
        data["logo"]=f"{request.scheme}://{request.get_host()}/{data['logo'] if data['logo'] else ''}"

        return Response(data, status=status.HTTP_200_OK)
    
    @permission_classes([IsAdminUser])
    def post(self, request:HttpRequest, action, *args, **kwargs):
        data=CompanyInfo.objects.first()
        responsible:CustomUser=request.user
        new_data=request.data
        new_data["creation_date"]=now()
        image_data = new_data.pop('logo', None)  # Extrae la imagen base64 del diccionario de datos
        
        if data:
            company_info = CompanyInfo.objects.get(pk=data.id)
            for key, value in new_data.items():
                setattr(company_info, key, value)
                
            if image_data and not image_data.startswith('http'):
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]  # Determina la extensión del archivo
                image_data = ContentFile(base64.b64decode(imgstr), name=f'image_{now().strftime("%Y%m%d_%H%M%S")}.{ext}')
          
                company_info.logo.save(image_data.name, image_data, save=True)  # Guarda la imagen en el campo ImageField
            company_info.save()
            return Response('Datos actualizados correctamente!', status=status.HTTP_200_OK)      

        company_info=CompanyInfo(**new_data)
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]  # Determina la extensión del archivo
            image_data = ContentFile(base64.b64decode(imgstr), name=f'image_{now().strftime("%Y%m%d_%H%M%S")}.{ext}')

            company_info.logo.save(image_data.name, image_data, save=True)  # Guarda la imagen en el campo ImageField

        company_info.save()

        history=History()
        history.module="company_info"
        history.action=Action.CREACION.value
        history.datetime=now()
        history.responsible=responsible
        history.save()

        return Response('Datos guardados correctamente!', status=status.HTTP_200_OK)
    