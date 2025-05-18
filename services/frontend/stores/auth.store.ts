import {defineStore} from 'pinia';

import {fetchWrapper} from '~/helpers/fetch-wrapper';
import type{UserLoginForm, User} from '~/types/auth';

const meta= import.meta.env.VITE_API_URL === undefined?'https://emprender-radix.com/api' : import.meta.env.VITE_API_URL;
const baseUrl=`${meta}/auth`;

export const useAuthStore = defineStore("auth", {
    state: ()=>({
        user: null as User|null,
        showLoginRegisterModal: false as boolean,
        refreshTokenTimeout: null as NodeJS.Timeout | null
    }),

    actions: {
        async login({email, password}:UserLoginForm):Promise<void> {
            this.user=await fetchWrapper.post(
                `${baseUrl}/login`, 
                {email, password},
                {credentials: 'include'}
            );

            await this.my_user();
            this.startRefreshTokenTimer();
        },

        async my_user():Promise<void> {        
            if (this.user?.access){
                await fetchWrapper.get(`${baseUrl}/user`).then((data)=>{
                    const userData=data;
                    userData["access"]=this.user?.access;
                    userData["refresh"]=this.user?.refresh;
                    this.user=userData;
                }).catch((e)=>{
                    this.user=null;
                    //throw e;
                });
            }      
        },
        async logout(): Promise<void>{
            //await fetchWrapper.post(`${baseUrl}/logout`, {refresh: this.user?.refresh});
            this.user=null;
        },
        async refreshToken(): Promise<void>{
            const data:any=await fetchWrapper.post(
                `${baseUrl}/refresh`, 
                {refresh: this.user?.refresh}
            ).catch(async(e)=>{
                this.user=null;
                await this.stopRefreshTokenTimer();
            });
            if(this.user != null){
                const userData=JSON.parse(JSON.stringify(this.user));
                userData["access"]=data["access"];
                userData["refresh"]=data["refresh"];
                this.user=userData;
                await this.startRefreshTokenTimer();
            }
        },

        async startRefreshTokenTimer():Promise<void> {
            if (this.user?.refresh){
                const jwtBase64 = this.user.access.split('.')[1];
                const jwtToken = JSON.parse(atob(jwtBase64));
                const expires = new Date(jwtToken.exp * 1000);
                const timeout = (expires.getTime() - Date.now()) - ((60 * 2) * 1000);
                this.refreshTokenTimeout =  setTimeout(async()=>{
                    await this.refreshToken();
                }, timeout);
                console.log("Next Refresh Token: "+timeout);
            }
        },    
        async stopRefreshTokenTimer():Promise<void>{
            if(this.refreshTokenTimeout){
                clearTimeout(this.refreshTokenTimeout);
                this.refreshTokenTimeout=null;
            }
        }
    },
    persist: {
        storage: persistedState.localStorage,
    },
});