interface ClientItem {
    id: number,
    username: string,
    email: string,
    date_joined: string,
    is_active: boolean,
    last_login: string
}

interface ClientForm{
    is_active: boolean
};

export type {
    ClientItem,
    ClientForm
}