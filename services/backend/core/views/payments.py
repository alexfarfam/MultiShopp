from dateutil.relativedelta import relativedelta
from django.db.models import F, fields, Count, Case, When, BooleanField, Value, Func
from django.utils.timezone import now
from django.db.models.functions import Now
from django.conf import settings
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .permissions.custom import IsAdminUser
from ..models.auth import History, CustomUser, Action, PaymentRecords, CompanyInfo

"""
Crud API for the payment module.
"""
def get_payment(id:int):
    payment:PaymentRecords=PaymentRecords.objects.filter(pk=id).values("id", "amount", "expiration_date", "provider__email", "creation_date")[0]     
    return payment

class DaysDifference(Func):
    function = 'DATEDIFF'
    template = "%(function)s(day, %(expressions)s)"
    output_field = fields.IntegerField()

class Payments_APIView(APIView):
    def get(self, request:HttpRequest, action, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            if action == "all":
                if not responsible.is_superuser:
                    return Response('No tienes los permisos suficientes para acceder a este recurso.', status=status.HTTP_403_FORBIDDEN) 

                _filter = request.GET.get("_filter")
                obj:BaseManager[PaymentRecords]=PaymentRecords.objects
                if (_filter == 'pending'):
                    obj=obj.filter(is_payment=False, expiration_date__gt=now()).annotate(
                        days_difference=DaysDifference( Now(), F('expiration_date'))
                    ).order_by('expiration_date', 'days_difference')
                elif (_filter == 'paid'):
                    obj=obj.filter(is_payment=True).order_by('expiration_date')
                else:
                    obj=obj.filter(is_payment=False, expiration_date__lt = now()).order_by('expiration_date')
                
                data=obj.values("id", "amount", "payment_date", "expiration_date", "provider__email", "creation_date") 
                if _filter == 'pending':
                    data=obj.values("id", "amount", "days_difference", "expiration_date", "provider__email", "creation_date") 

                payment_status_counts = PaymentRecords.objects.annotate(
                    estado=Case(
                        When(is_payment=True, then=Value('paid')),
                        When(expiration_date__gt=now(), is_payment=False, then=Value('pending')),
                        default=Value('payment_due'),
                        output_field=BooleanField(),
                    )
                ).values('estado').annotate(count=Count('id'))
                status_dict = {item['estado']: item['count'] for item in payment_status_counts}
                return Response({'data': data, 'status': status_dict}, status=status.HTTP_200_OK)
            
            elif action == "by_provider":
                if not responsible.is_provider:
                    return Response('No tienes los permisos suficientes para acceder a este recurso.', status=status.HTTP_403_FORBIDDEN) 

                obj:BaseManager[PaymentRecords]=PaymentRecords.objects.filter(provider=responsible).annotate(
                        days_difference=DaysDifference( Now(), F('expiration_date'))
                    ).order_by('expiration_date', 'days_difference')
                data=obj.values("id", "amount", "days_difference", "payment_date", "expiration_date", "is_payment", "creation_date") 
     
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("Accion no encontrada.", status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError) as e:
            return Response("No encontrado!", status=status.HTTP_404_NOT_FOUND)
   
    def post(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
           raise NotImplemented
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @permission_classes([IsAdminUser])
    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            amount=30000
            company_info=CompanyInfo.objects.first()
            if company_info:
                amount=company_info.service_price
            responsible:CustomUser=request.user
            payment_id=request.GET.get('payment_id')
            
            new_data={
                "is_payment": True,
                "payment_date": now()
            }

            payment = PaymentRecords.objects.filter(id=payment_id)
            if(payment.count() == 0):
                return Response(f"Pago con id {payment_id} no encontrado.", status=status.HTTP_404_NOT_FOUND)
            
            payment.update(**new_data)
            next_payment=PaymentRecords()
            next_payment.expiration_date=payment[0].expiration_date + relativedelta(months=1)
            next_payment.provider=CustomUser.objects.get(pk=payment[0].provider.id)
            next_payment.creation_date=now()
            next_payment.is_payment=False
            next_payment.amount=amount
            next_payment.save()

            history=History()
            history.module="payments"
            history.action=Action.ACTUALIZACION.value
            history.datetime=now()
            history.responsible=responsible
            history.save()

            return Response({"data": get_payment(next_payment.id),"msg": "Pago realizado correctamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            raise NotImplemented
        except Exception as e:
            if settings.DEBUG:
                raise e
            return Response(f"Error interno, por favor, intentelo mas tarde.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    