interface MenuItem {
    text: string;
    icon: string;
    url: string;
}

interface MenuSection {
    title: string;
    childrens: MenuItem[];
}
interface ItemListbox{
    id: number,
    title: string,
    description: string,
    image: string
}
type Key = string | number;

interface LoosObject {
    [key: string]: any
};

//
interface NotificationItem{
    id: string,
    title: string,
    content: string,
    actionText: string,
    actionEvent: any
};
interface SearchForm{
    search: string
};
interface SelectOption{
    value: number|string,
    label: string,
};
//
type MyHeaders = HeadersInit & {
    'Content-Type'?: string;
    'Authorization': string,
    [key: string]: string | undefined;
};

interface RequestOptions{
    credentials?: RequestCredentials
}

//
interface CartItem{
    id: number,
    title: string,
    img: string,
    price: number,
    reference_price: number,
    discount: number,
    amount: number,
    total: number,
    header_tag: string,
    responsible__id: number,
    selected: boolean
}
interface SmallItem{
    title: string,
    amount: number,
    price: number
}
interface GenericObject {
    [key: string]: any;
}
export type {
    MenuItem,
    MenuSection,
    Key,
    LoosObject,
    ItemListbox,
    NotificationItem,

    MyHeaders,
    RequestOptions,
    SearchForm,
    SelectOption,
    CartItem,
    SmallItem,
    GenericObject
}