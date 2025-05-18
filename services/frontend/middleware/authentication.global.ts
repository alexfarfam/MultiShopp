import {storeToRefs} from "pinia";
import {useAuthStore} from '~/stores/auth.store';

const providerOptions=[
    '/dashboard',
    '/dashboard/general/products',
    '/dashboard/general/services',
    '/dashboard/general/orders',
    '/dashboard/general/comments',
    '/dashboard/general/reservations',

    '/dashboard/profile/contact-data',
    '/dashboard/profile/user-data',
    '/dashboard/profile/my-payments'
];

const adminOptions=[
    '/dashboard',
    '/dashboard/general/categories',
    '/dashboard/general/subcategories',
    '/dashboard/general/clients',
    '/dashboard/general/providers',
    '/dashboard/general/payments',
    '/dashboard/general/extras',

    '/dashboard/profile/company-data',
    '/dashboard/profile/accounts',
];

export default defineNuxtRouteMiddleware(async(to, from) => {
    const authRequired = to.path.startsWith('/dashboard');
    const authStore=useAuthStore();
    const {user} =storeToRefs(authStore);
    
    await authStore.my_user(); // Update user for each page change.
    if(authRequired && !user.value?.is_staff && !user.value?.is_provider && to.path !== '/dashboard/login'){
        return {
            path: '/dashboard/login',
            query: {returnUrl: to.fullPath}
        }
    }

    if(user.value?.id && authRequired){
        if(user.value?.is_superuser && adminOptions.indexOf(to.path) === -1){
            return {
                path: '/dashboard'
            }
        }else if(user.value?.is_provider && providerOptions.indexOf(to.path) === -1){
            return {
                path: '/dashboard'
            }
        }
    }

});