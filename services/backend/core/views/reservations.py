from datetime import timedelta, datetime
from typing import List, Dict

from django.utils.timezone import now
from django.conf import settings
from django.db.models import Value, CharField

from django.db.models.functions import Concat
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes

from ..models.services import Reservation, Service
from .permissions.custom import IsAdminUser
from ..models.auth import History, CustomUser, Action

"""
Crud API for the reservations module.
"""

def get_reservations(id:int, filter:bool):
    reservations:Reservation=Reservation.objects.filter(service__responsible__pk=id, active=filter).annotate(
        title=Concat(Value('Reserva de '), 'service__title'),
        description=Concat(Value('Teléfono: '), 'telephone', Value('. Notas: '), 'notes', output_field=CharField())
    ).values("id", "title", "subservices", 'description', 'fullname', 'date', 'time', "active", "telephone", "service__approximate_duration")
    
    data:List[Dict[str, object]]=list(reservations)
    for x in range(len(data)):
        # - timedelta(hours=5)
        data[x]['start']=(datetime.combine(data[x]['date'], data[x]['time'])).strftime('%Y-%m-%d %H:%M')
        data[x]['end']=((datetime.combine(data[x]['date'], data[x]['time'])) + timedelta(minutes=float(data[x]["service__approximate_duration"]))).strftime('%Y-%m-%d %H:%M')
        data[x]['people']=[data[x]['fullname']]
        data[x]['subservices']=', '.join(data[x]['subservices']).rstrip(', ')
        #data[x]['calendarId']='work'

    return reservations

class Reservations_APIView(APIView):
    def get(self, request:HttpRequest, action, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            filter=request.GET.get('active') == '1'
            if responsible.is_provider and responsible.is_authenticated:
                data=get_reservations(responsible.pk, filter)
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response("Acceso denegado.", status=status.HTTP_403_FORBIDDEN)
        except (ValueError, TypeError) as e:
            return Response("No encontrado!", status=status.HTTP_404_NOT_FOUND)
   
    def post(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            new_data=request.data
            new_data["date"]=datetime.fromisoformat(new_data["date"].replace("Z", "+00:00"))
            new_data["time"]=datetime.fromisoformat(new_data["time"].replace("Z", "+00:00"))
            new_data["active"]=True

            if not responsible.is_anonymous:
                new_data["client"]=responsible
            new_data["service"]=Service.objects.get(pk=new_data["service"])
            new_data["creation_date"]=now()
            new_data["last_update_date"]=now()

            reservation=Reservation(**new_data)
            reservation.save()
           
            return Response("Reservación realizada correctamente! Se le notificará por whatsapp o correo...", status=status.HTTP_200_OK)
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            reservation_id=request.GET.get('reservation_id')
            action=request.GET.get('action')

            new_data:Dict[str,str]=request.data or {}
            new_data["active"]=False
            new_data["last_update_date"]=now()

            reservation=Reservation.objects.filter(pk=reservation_id)
            has_reservation=reservation.first()
            if has_reservation is None:
                return Response(f"Reservación con ID '{reservation_id}' no existe.", status=status.HTTP_404_NOT_FOUND)
            elif has_reservation.service.responsible.id != responsible.id:
                return Response(f"No tienes los permisos para actualizar este servicio.", status=status.HTTP_401_UNAUTHORIZED)
            else:
                reservation.update(**new_data)
                history=History()
                history.module="reservation"
                history.action=Action.ACTUALIZACION.value
                history.datetime=now()
                history.responsible=responsible
                history.save()
            
            return Response(f"Reservación {action.title()} correctamente!", status=status.HTTP_200_OK)
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
    