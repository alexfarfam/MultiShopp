from datetime import datetime
from djoser import email

from .models import CompanyInfo

#https://github.com/sunscrapers/djoser/blob/master/djoser/templates/email/activation.html
class CustomActivationEmail(email.ActivationEmail):
    template_name = 'email/activation.html'

    def get_context_data(self):
        context = super().get_context_data()
        try:
            company = CompanyInfo.objects.first()
            if not company:
                raise CompanyInfo.DoesNotExist
            
            context['company_name'] = company.company_name
            context['developer'] = "Al3x D3v"
            context['developer_url'] = "https://web.facebook.com/profile.php?id=1000864433652272"
            context['url_facebook'] = company.url_facebook
            context['customer_service_email'] = company.customer_service_email
            context['customer_service_telephone'] = company.customer_service_telephone
            context['current_year']=datetime.now().year

        except CompanyInfo.DoesNotExist:
            context['company_name'] = 'No Disponible'
            context['developer'] = "Al3x D3v"
            context['developer_url'] = "https://web.facebook.com/profile.php?id=100086443365227"
            context['url_facebook'] = 'No Disponible'
            context['customer_service_email'] = 'No Disponible'
            context['customer_service_telephone'] = 'No Disponible'
            context['current_year']=datetime.now().year
        
        return context

class CustomResetPasswordEmail(email.PasswordResetEmail):
    template_name = 'email/reset.html'

    def get_context_data(self):
        context = super().get_context_data()
        try:
            company = CompanyInfo.objects.first()
            if not company:
                raise CompanyInfo.DoesNotExist
            
            context['company_name'] = company.company_name
            context['developer'] = "Al3x D3v"
            context['developer_url'] = "https://web.facebook.com/profile.php?id=1000864433652272"
            
            context['customer_service_email'] = company.customer_service_email
            context['customer_service_telephone'] = company.customer_service_telephone
            context['current_year']=datetime.now().year

        except CompanyInfo.DoesNotExist:
            context['company_name'] = 'No Disponible'
            context['developer'] = "Al3x D3v"
            context['developer_url'] = "https://web.facebook.com/profile.php?id=100086443365227"
           
            context['customer_service_email'] = 'No Disponible'
            context['customer_service_telephone'] = 'No Disponible'
            context['current_year']=datetime.now().year
        
        return context
