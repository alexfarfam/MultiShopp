from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import F, Case, When, Value, CharField

from ..models.auth import CustomUser, CompanyInfo, Province, Locality, History, ACTIONS, ProviderInfo

"""
API for General Data
"""
class Globals_APIView(APIView):

    def get(self, request:HttpRequest, action, *args, **kwargs):
        if action == 'provinces':
            provinces=Province.objects.all().values(value=F("id"), label=F("name"))
            return Response(provinces, status=status.HTTP_200_OK)
        
        elif action == 'localities':
            province_id=request.GET.get("province_id")

            localities=Locality.objects.filter(province__id=province_id).values(value=F("id"), label=F("name"))
            return Response(localities, status=status.HTTP_200_OK)
        
        elif action == 'provider-info':
            provider_id=request.GET.get("provider_id")
            provider=CustomUser.objects.get(pk=provider_id, is_provider=True, is_superuser=False)
            data=ProviderInfo.objects.filter(user=provider)
            info={
                'company_name': '',
                'user__username': provider.username,
                'email': 'Sin Email',
                'url_facebook': '#',
                'url_instagram': '#',
                'whatsapp_telephone': 'Sin Whatsapp',
                'telephone': 'Sin Teléfono',
                'address': 'Sin Dirección'
            }

            if data.count() == 1:
                info=data.values('company_name', 'url_facebook', 'url_instagram', 'email', 'whatsapp_telephone', 'telephone', 'creation_date', 'address', 'user__username')[0]
            return Response(info, status=status.HTTP_200_OK)
        
        elif action == "company":
            company=CompanyInfo.objects.first()
            data={
                "developer": "Al3x D3v", 
                "developer_url": "https://web.facebook.com/profile.php?id=100086443365227", 
            }
            if company:
                data={
                    "company_name":company.company_name, 
                    "logo": f"{request.scheme}://{request.get_host()}/{company.logo.url}", 
                    "url_facebook": company.url_facebook, 
                    "customer_service_email": company.customer_service_email, 
                    "customer_service_telephone": company.customer_service_telephone
                }
            return Response(data, status=status.HTTP_200_OK)
        
        elif action == "logs":
            responsible:CustomUser=request.user
            if responsible.is_authenticated and responsible.is_superuser:
                actions_labels = Case(
                    *[When(action=key, then=Value(label)) for key, label in ACTIONS.items()],
                    output_field=CharField()
                )
                logs=History.objects.all().annotate(action_label=actions_labels).order_by('-datetime').values('module', 'datetime', 'responsible__username', 'action_label')

                return Response(logs, status=status.HTTP_200_OK)
            else:
                return Response('No tienes los permisos suficientes para acceder a este recurso.', status=status.HTTP_403_FORBIDDEN)
        else:
            return Response('Accion no encontrada.', status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request:HttpRequest, action, *args, **kwargs):
        data=request.data
        return Response('Correo subscrito corectamente!')

