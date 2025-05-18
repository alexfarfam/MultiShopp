interface AccountItem {
    id: number,
    username: string,
    password: string,
    email: string,
    is_superuser: boolean,
    date_joined: string,
    is_active: boolean,
    last_login: string
}

interface AccountForm{
    username: string,
    password: string,
    email: string,
    is_superuser: boolean,
    is_active: boolean
};

export type {
    AccountItem,
    AccountForm
}