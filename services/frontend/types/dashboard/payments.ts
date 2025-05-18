interface PaymentItem {
    id: number,
    amount: number,
    payment_date: string,
    expiration_date: string,
    provider__email: string,
    creation_date: string,
    days_difference: number
}
interface PaymentForm {
    id: number,
    amount: number,
    expiration_date: string,
    provider__email: string,
}

interface PaymentStatus {
    estado: string,
    count: number
}
export type {
    PaymentItem,
    PaymentStatus,
    PaymentForm
}