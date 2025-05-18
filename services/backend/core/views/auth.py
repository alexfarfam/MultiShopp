from django.utils import timezone
from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView

from ..serializers import TokenObtainPairSerializer
from ..models import CustomUser, PaymentRecords, ProviderInfo

"""
API for user authentication. In addition to user information, 
it returns information about the associated company.
"""
class Auth_APIView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request:HttpRequest, action, *args, **kwargs):
        if action == 'user':
            user = CustomUser.objects.filter(pk=request.user.pk).values(
                "id",
                "username",
                "is_confirmed",
                "email",
                "first_name",
                "last_name",
                "is_superuser",
                "is_staff",
                "is_provider",
                "is_active"
            ).first()
            
            #if not user["is_staff"] or not user["is_provider"]:
            #+    return Response(f"El usuario '{request.user.username}' no tienen un acceso valido.", status=status.HTTP_404_NOT_FOUND)
            
            info=ProviderInfo.objects.filter(user=request.user).values('logo', 'company_name')
            logo='/avatar.png'
            company=''
            if info.count() == 1:
                info=info[0]
                logo='/avatar.png' if info['logo'] == '' else f"{request.scheme}://{request.get_host()}/{info['logo']}"
                company=info['company_name']

            user["profile__name"]="Administrador(a)" if user["is_staff"] else "Vendedor(a)"
            user["logo"]=logo
            user["company"]=company
            user["profile"]=[]
            user["expiration_days"]=-1
            user["expire"]=False
            user["is_first_register"]=False

            if user["is_provider"]:
                user["is_first_register"]=PaymentRecords.objects.filter(provider=request.user).count() == 1
                latest_payment_record = PaymentRecords.objects.filter(provider=request.user, is_payment=0).order_by('-expiration_date')[:1]
                
                if latest_payment_record:
                    latest_payment_record=latest_payment_record[0]
                    next_to_expire, days = latest_payment_record.is_within_5_days()
                    if next_to_expire: 
                        user["expiration_days"]=days
                        user["expire"]=days < 0

            update_user=CustomUser.objects.get(pk=request.user.pk)
            update_user.last_login=timezone.now()
            update_user.save()
            
            return Response(user, status=status.HTTP_200_OK)
        else:
            return Response('Metodo no encontrado.', status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request:HttpRequest, action, *args, **kwargs):
        return Response("Logout successful.", status=status.HTTP_200_OK)
    
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response("Logout successful.", status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response("Invalid token.", status=status.HTTP_400_BAD_REQUEST)
        
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
