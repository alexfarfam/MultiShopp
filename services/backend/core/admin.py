from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

"""
Administrator for custom user
"""
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username", "email", "is_superuser", "is_staff", "is_active")
    list_filter = ("username", "email", "is_superuser", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("username", "email","password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password1", "password2", "is_staff", "is_superuser",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CompanyInfo)
admin.site.register(PaymentRecords)
admin.site.register(History)
admin.site.register(ProviderInfo)
admin.site.register(ClientInfo)
admin.site.register(Province)
admin.site.register(Locality)
admin.site.register(Extras)
admin.site.register(FAQ)

admin.site.register(Category)
admin.site.register(SubCategory)

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductOption)
admin.site.register(ProductOffer)

admin.site.register(Service)
admin.site.register(ServiceDetail)
admin.site.register(ServiceImage)
admin.site.register(ServiceAvailability)
admin.site.register(Reservation)

admin.site.register(Order)
admin.site.register(OrderDetail)

admin.site.register(Comment)