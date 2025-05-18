interface ExtrasForm{
    about: string,
    company: string,
    history: string,
    workflow: string,
    support: string,
    privacy_policy: string,
    terms_condition: string
}

interface FAQForm{
   question: string,
   answer: string
}
interface FAQItem{
    id: number,
    question: string,
    answer: string
 }

export type {
    ExtrasForm,
    FAQForm,
    FAQItem
}