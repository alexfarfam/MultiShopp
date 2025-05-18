from rest_framework.permissions import BasePermission
from django.http import HttpRequest

from ...models.auth import PaymentRecords

class IsAdminUser(BasePermission):
    """
    Allows access only to Admin users.
    """

    def has_permission(self, request:HttpRequest, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff and not request.user.is_provider)
    
class IsProviderUser(BasePermission):
    """
    Allows access only to Provider users.
    """

    def has_permission(self, request:HttpRequest, view):
        latest_payment_record=PaymentRecords.objects.filter(provider=request.user, is_payment=0).order_by('-expiration_date')[:1]
        expire=False
        if latest_payment_record:
            latest_payment_record=latest_payment_record[0]
            _, days = latest_payment_record.is_within_5_days()
            expire=days < 0

        return not expire and bool(request.user and request.user.is_authenticated and request.user.is_provider)

