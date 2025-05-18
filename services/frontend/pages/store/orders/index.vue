<template>
    <Breadcrumb :home="home" :model="items">
        <template #item="{ item, props }">
            <nuxt-link v-if="item.route" :to="item.route">
                <span :class="[item.icon, 'text-color']" />
                <span class="ml-2 text-primary font-semibold">{{ item.label }}</span>
            </nuxt-link>
            <span v-else class="text-surface-700 dark:text-surface-0">{{ item.label }}</span>
        </template>
    </Breadcrumb>

    <div class="px-0 md:px-4 my-2" v-if="user?.username">
        <div v-if="orders.length > 0" class="flex flex-col gap-2 md:gap-4">
            <div v-for="(order, index) in orders" class="m-2 md:m-4 shadow-lg rounded-md p-4 flex flex-row gap-4">
                <div class="basis-[4rem]">
                    <Avatar icon="pi pi-truck" class="mr-2" size="large" shape="circle" />
                </div>

                <div class="flex-1 flex flex-col gap-4">
                    <div class="flex flex-row gap-4">
                        <div class="basis-[90%] flex flex-row gap-4">
                            <span class="text-gray-500 text-lg">Nº{{ isMobile? '':' Pedido' }}: {{ order.order_number}}</span>
                        </div>

                        <span class="hidden md:block flex-1 mt-2 text-center text-gray-500 text-sm" v-tooltip.top="dayjs(order.last_update_date).format('YYYY-MM-DD HH:mm:ss')">{{dayjs(order.last_update_date).fromNow() }}</span>
                    </div>

                    <div class="flex flex-row gap-4">
                        <div class="hidden md:flex flex-row gap-4">
                            <span class="text-lg font-medium">Total: </span> <span class="text-lg text-gray-500">{{ Globalization.currencyFormat.format(order.total) }}</span>
                        </div>
                        <div class="hidden md:flex flex-row gap-4">
                            <span class="text-lg font-medium">Dirección: </span> <span class="text-lg text-gray-500">{{ order.address }}</span>
                        </div>
                        <div class="flex-1 hidden md:flex flex-row gap-4">
                            <span class="text-lg font-medium">Referencia: </span> <span class="text-lg text-gray-500">{{ order.reference }}</span>
                        </div>
                        <div class="w-36">
                            <Button size="small" @click="doViewDetails(order.order_number)" icon="pi pi-eye" label="Ver detalles" fluid />
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="w-[80%] md:w-[25%] py-20 mx-auto flex flex-col flex-wrap gap-4" v-else>
            <svg-icon class="block text-gray-700 w-full text-center" size="70" type="mdi" :path="mdiCartArrowRight"></svg-icon>
            <span class="text-xl font-medium text-center">A&uacute;n no realizas pedidos.</span>
            <Button @click="doShowProducts" fluid class="mx-auto" label="Ver nuestros productos"/>
        </div>
    </div>

    <div class="px-4 my-32" v-else>
        <div class="w-[25%] mx-auto flex flex-row flex-wrap gap-4">
            <div class="basis-[15%] text-center">
                <i class="pi pi-user !text-5xl text-gray-500"></i>
            </div>

            <div class="basis-[80%] flex flex-col gap-2">
                <span class="text-xl font-medium text-center">Aún no has Iniciado Sesión</span>
                <span class="text-lg text-gray-500 text-center">Identifícate para ver tú historial de pedidos.</span>
            </div>

            <div class="flex-1">
                <Button @click="doShowLogin" fluid class="mx-auto" icon="pi pi-sign-in" label="Iniciar Sesión"/>
            </div>
        </div>
    </div>

</template>

<script lang="ts" setup>
    import { storeToRefs } from 'pinia';
    
    import { 
        mdiCartArrowRight
    } from '@mdi/js';
    import type { SmallOrderItem } from '~/types/dashboard/products';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import dayjs from 'dayjs';
    import { useMediaQuery } from '@vueuse/core';
    import locale_es from 'dayjs/locale/es'
    import relativeTime from 'dayjs/plugin/relativeTime';
    import { Globalization } from '~/helpers/globalization';
    import { useAuthStore } from '~/stores/auth.store';

    // Meta configuration
    definePageMeta({
        layout:'public'
    });

    const router=useRouter();
    const authStore=useAuthStore();
    const {user} = storeToRefs(authStore);
    dayjs.extend(relativeTime);
    dayjs.locale('es');
    const isMobile = useMediaQuery('(max-width: 600px)');

    /********************* 
    | Data
    **********************/
    const orders=ref<SmallOrderItem[]>([]); 
    const home = ref({
        icon: 'pi pi-home',
        label: 'Inicio',
        route: '/'
    });
    const items = ref<object[]>([{
        label: 'Mis Pedidos'
    }]);
    /********************* 
    | METHODS
    **********************/
    //
    const doShowProducts=async()=>{
        router.push('/store/collections/promotions');
    };
    const doShowLogin=async()=>{
        sendEvent('modal:login-register-client', {severity: 'normal', message: ''});
    };

    const doViewDetails=async(order_number: string)=>{
        router.push('/store/orders/'+order_number);
    };
    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        orders.value=await fetchWrapper.get('/orders/my-orders');
    });
</script>