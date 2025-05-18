interface ContactForm{
    company_name: string,
    logo: string,
    url_instagram: string,
    whatsapp_telephone: string,
    url_facebook: string,
    email: string,
    telephone: string,
    address: string
};
interface ContactForm2{
    company_name: string,
    logo: string,
    url_instagram: string,
    whatsapp_telephone: string,
    url_facebook: string,
    email: string,
    telephone: string,
    address: string,
    user__username: string
};

export type{
    ContactForm,
    ContactForm2
}