<template>
    <div class="px-0 md:px-4 my-2">
        <div v-if="filteredOrderData.length > 0" class="flex flex-col gap-4">
            <div v-for="(order, index) in filteredOrderData" class="m-4 shadow-lg rounded-md p-4 flex flex-row gap-4">
                <div class="basis-[4rem]">
                    <Avatar icon="pi pi-truck" class="mr-2" size="large" shape="circle" />
                </div>

                <div class="flex-1 flex flex-col gap-4">
                    <div class="flex flex-row gap-4">
                        <div class="basis-[90%] flex flex-row gap-4">
                            <span class="text-gray-500 text-lg">{{ isMobile? 'Nº':'Nº Pedido:' }} {{ order.order_number}}</span>
                        </div>

                        <span v-tooltip.top="dayjs(order.last_update_date).format('YYYY-MM-DD HH:mm:ss')" class="!hidden md:block flex-1 mt-2 text-center text-gray-500 text-sm">{{dayjs(order.last_update_date).fromNow() }}</span>
                    </div>

                    <div class="flex flex-col md:flex-row gap-4">
                        <div class="flex flex-row gap-4">
                            <span class="text-lg font-medium">Total: </span> <span class="text-lg text-gray-500">{{ Globalization.currencyFormat.format(order.total) }}</span>
                        </div>
                        <div class="flex flex-row gap-4">
                            <span class="text-lg font-medium">Dirección: </span> <span class="text-lg text-gray-500">{{ order.address }}</span>
                        </div>
                        <div class="flex-1 flex flex-row gap-4">
                            <span class="text-lg font-medium">Referencia: </span> <span class="text-lg text-gray-500">{{ order.reference }}</span>
                        </div>

                        <div class="w-36">
                            <Button size="small" @click="doViewDetails(order.order_number)" icon="pi pi-eye" label="Ver detalles" fluid />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="py-40" v-else>
            <svg-icon class="block text-gray-400/[0.8] w-full text-center" size="70" type="mdi" :path="mdiTruckFastOutline"></svg-icon>
            <span class="mt-4 mx-10 block text-2xl text-gray-400/[0.8] text-center font-medium">Aún no hay pedidos para mostrar.</span>
        </div>
    </div>

    <Dialog dismissable-mask v-model:visible="showOrderDetails" modal header="Detalles" :style="{ width: '90vw' }">
        <ViewOrderDetailComponent :order-number="currentOrderNumber" :show-bread-crumb="false" :force-update="showOrderDetails"/>
    </Dialog>
    
</template>

<script lang="ts" setup>
    import type { OrderItem } from '~/types/dashboard/products';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import { mdiTruckFastOutline } from '@mdi/js';
    import dayjs from 'dayjs';
    import locale_es from 'dayjs/locale/es';
    import { cloneDeep } from 'lodash-es';
    import relativeTime from 'dayjs/plugin/relativeTime';
    import { Globalization } from '~/helpers/globalization';
    import { useMediaQuery } from '@vueuse/core';

    // Meta configuration
    dayjs.extend(relativeTime);
    dayjs.locale('es');

    useListen('application:search' , (message:any) => {
        const search = (message.message as string).toLowerCase();
        filteredOrderData.value=orderData.value.filter(entry=>{
            return (
                entry.order_number.toLowerCase().includes(search) ||
                entry.fullname.toString().includes(search) ||
                Globalization.currencyFormat.format(entry.total).includes(search) ||
                entry.address.toString().includes(search) ||
                entry.reference.toString().includes(search) ||
                Globalization.dateFormat2(entry.last_update_date, true).toString().includes(search) 
            );
        });
    });

    /********************* 
    | Data
    **********************/
    const orderData=ref<OrderItem[]>([]); 
    const filteredOrderData=ref<OrderItem[]>([]); 
    const showOrderDetails = ref<boolean>(false);
    const currentOrderNumber = ref<string>('');
    const isMobile = useMediaQuery('(max-width: 600px)');

    /********************* 
    | METHODS
    **********************/
    //
    const doViewDetails=async(orderNumber: string)=>{
        currentOrderNumber.value=orderNumber;
        showOrderDetails.value=true;
    };
    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        orderData.value=await fetchWrapper.get('/orders/orders');
        filteredOrderData.value=cloneDeep(orderData.value);
    });
</script>