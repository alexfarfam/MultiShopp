from django.conf import settings
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone

from .permissions.custom import IsAdminUser, IsProviderUser
from ..models.auth import CustomUser
from ..models import Product, Service, Order, Comment, OrderDetail, PaymentRecords, Reservation

"""
Crud API for the dashboard summary.
"""
# PROVIDER
def get_orders_summary(provider_id:int):
    orders_per_day = (
        Order.objects.filter(provider_id=provider_id)
        .annotate(date=TruncDate('creation_date'))
        .values('date')
        .annotate(order_count=Count('id'))
        .order_by('date')
    )

    # Extraemos las etiquetas y datos del queryset
    labels = [entry['date'].strftime('%Y-%m-%d') for entry in orders_per_day]
    data = [entry['order_count'] for entry in orders_per_day]

    # Definimos los colores para el gráfico
    background_colors = [
        'rgba(249, 115, 22, 0.2)', 
        'rgba(6, 182, 212, 0.2)', 
        'rgb(107, 114, 128, 0.2)', 
        'rgba(139, 92, 246, 0.2)'
    ]
    border_colors = [
        'rgb(249, 115, 22)', 
        'rgb(6, 182, 212)', 
        'rgb(107, 114, 128)', 
        'rgb(139, 92, 246)'
    ]

    # Aseguramos que los colores se repitan si hay más fechas
    background_colors *= (len(labels) // len(background_colors)) + 1
    border_colors *= (len(labels) // len(border_colors)) + 1

    # Estructura final para Chart.js
    chart_data = {
        "labels": labels,
        "datasets": [
            {
                "label": "Pedidos por día",
                "data": data,
                "backgroundColor": background_colors[:len(labels)],
                "borderColor": border_colors[:len(labels)],
                "borderWidth": 1,
            }
        ]
    }

    return chart_data


def get_top_10_services(provider_id:int):
    top_services = (
        OrderDetail.objects
        .filter(service__isnull=False, order__provider_id=provider_id)
        .values('service__title')
        .annotate(total_orders=Count('service'))
        .order_by('-total_orders')[:10]
    )

    labels = [entry['service__title'] for entry in top_services]
    data = [entry['total_orders'] for entry in top_services]

    background_colors = [
        'rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)',
        'rgba(201, 203, 207, 0.2)', 'rgba(255, 99, 71, 0.2)',
        'rgba(60, 179, 113, 0.2)', 'rgba(255, 215, 0, 0.2)'
    ]
    border_colors = [
        'rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 206, 86)',
        'rgb(75, 192, 192)', 'rgb(153, 102, 255)', 'rgb(255, 159, 64)',
        'rgb(201, 203, 207)', 'rgb(255, 99, 71)', 'rgb(60, 179, 113)',
        'rgb(255, 215, 0)'
    ]

    chart_data = {
        "labels": labels,
        "datasets": [
            {
                "label": "Top 10 servicios más pedidos",
                "data": data,
                "backgroundColor": background_colors[:len(labels)],
                "borderColor": border_colors[:len(labels)],
                "borderWidth": 1,
            }
        ]
    }

    return chart_data

def get_top_10_products(provider_id:int):
    FIXED_COLORS = [
        "#06b6d4", "#f97316", "#6b7280", "#8b5cf6", "#ec4899",
        "#14b8a6", "#facc15", "#6366f1", "#22c55e", "#ef4444"
    ]

    def get_cyclic_colors(num_products):
        """Devuelve una lista de colores cíclicos."""
        return [FIXED_COLORS[i % len(FIXED_COLORS)] for i in range(num_products)]

    top_products = (
        OrderDetail.objects
        .filter(product__isnull=False, order__provider_id=provider_id)
        .values('product__title')
        .annotate(total_orders=Count('product'))
        .order_by('-total_orders')[:10]
    )

    labels = [entry['product__title'] for entry in top_products]
    data = [entry['total_orders'] for entry in top_products]

    num_products = len(top_products)
    background_colors = get_cyclic_colors(num_products)
    hover_colors = get_cyclic_colors(num_products)

    chart_data = {
        "labels": labels,
        "datasets": [
            {
                "data": data,
                "backgroundColor": background_colors,
                "hoverBackgroundColor": hover_colors,
            }
        ]
    }

    return chart_data


# ADMIN
def get_payment_history():
    months_spanish = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    
    now = timezone.now()
    payments= (
        PaymentRecords.objects
        .filter(payment_date__year=now.year)
        .annotate(month=TruncMonth('payment_date'))
        .values('month')
        .annotate(total_amount=Sum('amount'))
        .order_by('month')
    )

    # Extraemos las etiquetas y datos del queryset
    labels = [months_spanish[entry['month'].month - 1] for entry in payments]  # Mes en español
    data = [entry['total_amount'] for entry in payments]

    # Definimos los colores para el gráfico
    background_colors = [
        'rgba(249, 115, 22, 0.2)', 
        'rgba(6, 182, 212, 0.2)', 
        'rgb(107, 114, 128, 0.2)', 
        'rgba(139, 92, 246, 0.2)'
    ]
    border_colors = [
        'rgb(249, 115, 22)', 
        'rgb(6, 182, 212)', 
        'rgb(107, 114, 128)', 
        'rgb(139, 92, 246)'
    ]

    # Aseguramos que los colores se repitan si hay más fechas
    background_colors *= (len(labels) // len(background_colors)) + 1
    border_colors *= (len(labels) // len(border_colors)) + 1

    # Estructura final para Chart.js
    chart_data = {
        "labels": labels,
        "datasets": [
            {
                "label": "Monto Total",
                "data": data,
                "backgroundColor": background_colors[:len(labels)],
                "borderColor": border_colors[:len(labels)],
                "borderWidth": 1,
            }
        ]
    }

    return chart_data

class Summary_APIView(APIView):
    permission_classes=[IsAdminUser | IsProviderUser]

    def get(self, request:HttpRequest, action, *args, **kwargs):
        try:
            responsible:CustomUser=request.user
            summary={}
            if responsible.is_provider:
                summary['products_count']=Product.objects.filter(responsible=responsible).count()
                summary['reservations_count']=Reservation.objects.filter(service__responsible=responsible, active=True).count()
                summary['services_count']=Service.objects.filter(responsible=responsible).count()
                summary['orders_count']=Order.objects.filter(provider_id=responsible.pk).count()
                summary['comments_count']=Comment.objects.filter(product__responsible=responsible, deleted=False).count()
                summary['summary_sales']=get_orders_summary(responsible.pk)
                summary['summary_top_10_products']=get_top_10_products(responsible.pk)
                summary['get_top_10_services']=get_top_10_services(responsible.pk)
            else:
                summary['clients_count']=CustomUser.objects.filter(is_provider=False, is_staff=False, is_superuser=False).count()
                summary['providers_count']=CustomUser.objects.filter(is_provider=True).count()
                summary['payments_count']=PaymentRecords.objects.filter(is_payment=True).count()
                summary['summary_payment_history']=get_payment_history()

            return Response(summary, status=status.HTTP_200_OK)
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
    
    def put(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
           raise NotImplemented
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request:HttpRequest, action, format=None, *args, **kwargs):
        try:
           raise NotImplemented
        except Exception as e:
            err=f"Error interno, por favor, intentelo mas tarde."
            if settings.DEBUG:
                raise e
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)