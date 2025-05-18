import base64

from django.http import HttpRequest
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.files.base import ContentFile

from .permissions.custom import IsProviderUser
from ..models.auth import History, CustomUser, Action, ProviderInfo

"""
Crud API for the contact data module.
"""
class ContactData_APIView(APIView):
    permission_classes=[IsProviderUser]

    def get(self, request:HttpRequest, action, *args, **kwargs):
        responsible:CustomUser=request.user
        data={}
        if action == "contact":
            data1=ProviderInfo.objects.filter(user=responsible).values('id', 'url_instagram', 'whatsapp_telephone', 'url_facebook', 'email', 'telephone', 'address', 'logo', 'company_name')
            if data1.count() == 1:
                data = data1[0]
                data["logo"]=f"{request.scheme}://{request.get_host()}/{data['logo'] if data['logo'] else ''}"
        else:
            data=CustomUser.objects.filter(pk=responsible.id).values('id', 'username', 'email', 'is_confirmed', 'joined_date', 'company_name')[0]
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request:HttpRequest, action, *args, **kwargs):
        responsible:CustomUser=request.user

        data=ProviderInfo.objects.filter(user=responsible).first()
        new_data=request.data
        new_data["creation_date"]=now()
        new_data["user"]=responsible
        image_data = new_data.pop('logo', None)  # Extrae la imagen base64 del diccionario de datos
        
        if data:
            provider_info = ProviderInfo.objects.get(pk=data.id)
            for key, value in new_data.items():
                setattr(provider_info, key, value)
                
            if image_data and not image_data.startswith('http'):
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]  # Determina la extensión del archivo
                image_data = ContentFile(base64.b64decode(imgstr), name=f'image_{now().strftime("%Y%m%d_%H%M%S")}.{ext}')
          
                provider_info.logo.save(image_data.name, image_data, save=True)  # Guarda la imagen en el campo ImageField
            provider_info.save()
            return Response('Datos actualizados correctamente!', status=status.HTTP_200_OK)      

        provider_info=ProviderInfo(**new_data)
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]  # Determina la extensión del archivo
            image_data = ProviderInfo(base64.b64decode(imgstr), name=f'image_{now().strftime("%Y%m%d_%H%M%S")}.{ext}')

            provider_info.logo.save(image_data.name, image_data, save=True)  # Guarda la imagen en el campo ImageField

        provider_info.save()


        provider_info=ProviderInfo(**new_data)
        provider_info.save()

        history=History()
        history.module="provider_info"
        history.action=Action.CREACION.value
        history.datetime=now()
        history.responsible=responsible
        history.save()

        return Response('Datos guardados correctamente!', status=status.HTTP_200_OK)
    