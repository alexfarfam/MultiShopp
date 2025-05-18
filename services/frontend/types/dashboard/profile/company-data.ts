
interface CompanyItem{
    company_name: string,
    logo: string,
    url_facebook: string,
    url_instagram: string,
    customer_service_email: string,
    customer_service_telephone: string,
    whatsapp_telephone: string,
    service_price: number
};
interface CompanyForm{
    company_name: string,
    logo: string,
    url_facebook: string,
    url_instagram: string,
    customer_service_email: string,
    customer_service_telephone: string,
    whatsapp_telephone: string,
    service_price: number
};

export type{
    CompanyItem,
    CompanyForm
}