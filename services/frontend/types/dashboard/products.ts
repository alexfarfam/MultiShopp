interface ProductOfferForm{
    id: number,
    title: string,
    price: number,
    reference_price: number,
    discount: number,
    header_tag: string,
    amount: number,
    image: string,
    selected: boolean
}
interface ProductOfferItem{
    id: number,
    title: string,
    reference_price: number,
    price: number,
    discount: number,
    header_tag: string,
    amount: number
}
interface ProductCharacteristicItem{
    id:number,
    title: string,
    values: any
}
interface ImageProduct{
    id: number,
    name: string,
    image: string
}

interface ProductForm{
    title: string,
    header_tag: string,
    description: string,
    price: number,
    discount: number,
    reference_price: number,
    main_image: string,
    subcategory: number|string,
    images: string[],
    offers: ProductOfferItem[],
    show_offerts: boolean
}

interface ProductItem{
    id: number,
    title: string,
    header_tag: string,
    description: string,
    price: number,
    reference_price: number,
    discount: number,
    main_image: string,
    category__id: number,
    category__title: string,
    subcategory__id: number,
    subcategory__title: string,
    qualification: number,
    comments_count: number,
    orders: number,
    show_offerts: boolean,
    last_update_date: string,
    responsible: number,
    responsible__id: number,

    with_reservation: boolean
}

interface SmallOrderItem{
    order_number: string,
    fullname: string,
    total: number,
    last_update_date: string,
    address: string,
    reference: string
}

interface OrderDetailItem{
    detail_id: string,
    amount: number,
    price: number, 
    discount: number,
    total: number,
    title: string,
    image_url: string,

    order__source_product: string
}
interface OrderItem{
    order_number: string,
    total: number,
    email: string,
    fullname: string,
    telephone: string,
    province__name: string,
    locality__name: string,
    city: string,
    address: string,
    reference: string,
    last_update_date: string,
    provider_id: number,
    
    details: OrderDetailItem[]
}

export type {
    ProductForm,
    ProductItem,
    ImageProduct,

    ProductOfferForm,
    ProductOfferItem,
    ProductCharacteristicItem,

    SmallOrderItem,
    OrderItem
}           