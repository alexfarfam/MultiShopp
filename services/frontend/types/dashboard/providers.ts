interface ProviderItem {
    id: number,
    username: string,
    email: string,
    date_joined: string,
    is_active: boolean,
    last_login: string
}

interface ProviderForm{
    is_active: boolean
};

export type {
    ProviderItem,
    ProviderForm
}