interface TimeSlot {
    start_time: string;  
    end_time: string;
}
interface Availability {
    [day: string]: TimeSlot;
}
interface Availability2 {
    day: string,
    start_time: string;  
    end_time: string;
}
interface ReservationForm {
    fullname: string,
    email: string,
    telephone: string,
    service: number,
    subservices:string[],
    
    notes: string,
    date: Date|null,
    time: Date|null
}
interface ImageService{
    id: number,
    name: string,
    image: string
}
interface ServiceForm{
    title: string,
    header_tag: string,
    description: string,
    main_image: string,
    approximate_duration: number,
    with_reservation: boolean,
    opening_hours:Availability,
    subservices: string[],

    subcategory: number|string,
    images: string[]
}
interface ExtraInfo{
    approximate_duration: number,
    with_reservation: boolean,
    opening_hours:Availability2[]
}

interface ServiceItem{
    id: number,
    title: string,
    header_tag: string,
    description: string,
    main_image: string,
    category__id: number,
    category__title: string,
    subcategory__id: number,
    subcategory__title: string,
    qualification: number,
    comments_count: number,
    with_reservation: boolean,
    approximate_duration: number,
    opening_hours:Availability,
    subservices: string[],

    orders: number,
    last_update_date: string,
    responsible__id: number,
    responsible: number
}

export type {
    ServiceForm,
    ServiceItem,
    ImageService,
    Availability,
    ExtraInfo,
    Availability2,
    ReservationForm
}           