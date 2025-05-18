from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import *

app_name='api'

urlpatterns=[
    path('summary/<str:action>', Summary_APIView.as_view()),
    path('globals/<str:action>', Globals_APIView.as_view()),
    path('categories/<str:action>', Categories_APIView.as_view()),
    path('subcategories/<str:action>', SubCategories_APIView.as_view()),
    path('products/<str:action>', Products_APIView.as_view()),
    path('services/<str:action>', Services_APIView.as_view()),
    path('reservations/<str:action>', Reservations_APIView.as_view()),

    path('clients/<str:action>', Clients_APIView.as_view()),
    path('providers/<str:action>', Providers_APIView.as_view()),
    path('orders/<str:action>', Orders_APIView.as_view()),
    path('payments/<str:action>', Payments_APIView.as_view()),
    path('comments/<str:action>', Comments_APIView.as_view()),
    path('accounts/<str:action>', Accounts_APIView.as_view()),
    path('company-data/<str:action>', CompanyData_APIView.as_view()),
    path('contact-data/<str:action>', ContactData_APIView.as_view()),
    path('extras/<str:action>', Extras_APIView.as_view()),

    path('auth/login', EmailTokenObtainPairView().as_view(), name='token_optain_pair'),
    #path('auth/logout', jwt_views.TokenBlacklistView.as_view(), name='token_blacklist'),
    
    path('auth/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/<str:action>', Auth_APIView.as_view())
]