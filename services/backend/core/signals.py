from django.dispatch import receiver
from djoser.signals import user_activated
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .models.auth import CustomUser, PaymentRecords,CompanyInfo

@receiver(user_activated)
def create_payment_record(sender, user:CustomUser, request, **kwargs):
    obj=CustomUser.objects.get(pk=user.id)
    obj.is_confirmed=True
    obj.joined_date=timezone.now()
    obj.save()

    amount=30000
    company_info=CompanyInfo.objects.first()
    if company_info:
        amount=company_info.service_price

    if obj.is_provider:
        PaymentRecords.objects.create(
            amount=amount,
            expiration_date=timezone.now() + relativedelta(months=1),
            provider=user
        )