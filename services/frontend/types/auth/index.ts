import type { MenuItem } from "..";

interface LoginForm{
    username: string,
    password: string
}

interface UserLoginForm{
    email: string,
    password: string
}
interface UserRecoverForm{
    email: string
}
interface UserSubForm{
    email: string
}
interface UserConfirmRecoverForm{
    new_password: string,
    re_new_password: string,

    uid: string,
    token: string
}
interface UserRegisterForm{
    username: string,
    email: string,
    password: string,
    is_provider: boolean
}

interface User{
    id: number,
    username: string
    email: string,
    is_superuser: boolean,
    is_active: boolean,
    is_staff: boolean,
    profile: Array<MenuItem>,
    first_name: string,
    last_name: string,
    profile__name: string,
    company: string,
    logo: string,
    is_confirmed: boolean,

    expiration_days: number,
    is_first_register: boolean,
    expire: boolean,
    is_provider:boolean,
    
    access: string,
    refresh: string
}

//
export type{
    LoginForm,
    UserLoginForm,
    UserRegisterForm,
    User,
    UserSubForm,

    UserRecoverForm,
    UserConfirmRecoverForm
}