interface OrderForm{
    fullname: string,
    email: string,
    telephone: string,
    province: string,
    locality: string,
    city: string,
    address: string,
    reference: string,
    source_detail: string,
    provider_id: number,

    details: object[]
}

export type {
    OrderForm
}