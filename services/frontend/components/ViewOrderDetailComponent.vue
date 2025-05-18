<template>
    <div :class="showBreadCrumb ? 'py-4':''" v-if="errorPage.trim() === ''">
        <Breadcrumb v-if="props.showBreadCrumb" :home="home" :model="items">
            <template #item="{ item, props }">
                <nuxt-link  v-if="item.route" :to="item.route">
                    <span :class="[item.icon, 'text-color']" />
                    <span class="ml-2 text-primary font-semibold">{{ item.label }}</span>
                </nuxt-link>
                <span v-else class="text-surface-700 dark:text-surface-0">{{ item.label }}</span>
            </template>
        </Breadcrumb>

        <div :class="showBreadCrumb ? 'py-8':''">
            <div class="p-2 md:p-4">
                <div class="flex justify-between items-center">
                    <h3 class="text-lg font-semibold">{{ isMobile ? 'Nº '+currentOrder.order_number : 'Pedido Nº '+currentOrder.order_number }}</h3>
                    <Button @click="doExport" icon="pi pi-download" :label="isMobile?'Descargar':'Descargar PDF'" />
                </div>

                <div class="grid grid-cols-2 md:grid-cols-6 mt-6 border border-gray-300/[0.4]">
                    <div class="col-span-2 flex flex-row">
                        <span class="w-32 md:w-52 bg-[#FAFAFA] p-5 border-gray-300/[0.4] border-b border-r">Nombres:</span>
                        <span class="p-5 truncate bg-white border-b border-r flex-1">{{ currentOrder.fullname }}</span>
                    </div>
                    <div class="col-span-2 flex flex-row">
                        <span class="w-32 md:w-52 bg-[#FAFAFA] p-5 border-gray-300/[0.4] border-b border-r">Email:</span>
                        <span class="p-5 truncate bg-white border-b flex-1">{{ currentOrder.email }}</span>
                    </div>
                    <div class="col-span-2 flex flex-row">
                        <span class="w-32 md:w-52 bg-[#FAFAFA] p-5 border-gray-300/[0.4] border-b border-r">Teléfono:</span>
                        <span class="p-5 truncate bg-white border-b border-r flex-1">{{ currentOrder.telephone }}</span>
                    </div>

                    <div class="col-span-2 flex flex-row">
                        <span class="w-32 md:w-52 bg-[#FAFAFA] p-5 border-gray-300/[0.4] border-b border-r">Provincia:</span>
                        <span class="p-5 truncate bg-white border-b flex-1">{{ currentOrder.province__name }}</span>
                    </div>
                    <div class="col-span-2 flex flex-row">
                        <span class="w-32 md:w-52 bg-[#FAFAFA] p-5 border-gray-300/[0.4] border-b border-r">Localidad:</span>
                        <span class="p-5 truncate bg-white border-b flex-1">{{ currentOrder.locality__name }}</span>
                    </div>
                    <div class="col-span-2 flex flex-row">
                        <span class="w-32 md:w-52 bg-[#FAFAFA] p-5 border-gray-300/[0.4] border-b border-r">Ciudad:</span>
                        <span class="p-5 truncate bg-white border-b flex-1">{{ currentOrder.city }}</span>
                    </div>

                    <div class="col-span-2 flex flex-row">
                        <span class="w-32 md:w-52 bg-[#FAFAFA] p-5 border-gray-300/[0.4] border-b border-r">Referencia:</span>
                        <span class="p-5 truncate bg-white border-b flex-1">{{ currentOrder.reference }}</span>
                    </div>
                    <div class="col-span-2 md:col-span-4 flex flex-row">
                        <span class="w-32 md:w-52 bg-[#FAFAFA] p-5 border-gray-300/[0.4] border-b border-r">Dirección:</span>
                        <span class="p-5 truncate bg-white border-b flex-1">{{ currentOrder.address }}</span>
                    </div>
                </div>
            </div>

            <div class="flex flex-col gap-4">
                <div class="mt-5 mx-5 flex flex-col items-start">
                    <span class="text-xl font-medium">Detalles:</span>
                </div>
                <div v-for="(detail, index) in currentOrder.details" class="m-4 shadow-lg rounded-md p-4 flex flex-row gap-4">
                    <div class="basis-[4rem]">
                        <nuxt-link :to="'/store/products/'+detail.detail_id">
                            <Avatar :image="detail.image_url" class="mr-2" size="xlarge" shape="circle" />
                        </nuxt-link>
                    </div>

                    <div class="flex-1 flex flex-col gap-4">
                        <div class="flex flex-row gap-4">
                            <div class="basis-[90%] flex flex-row gap-4">
                                <span class="text-gray-500 text-lg">{{ detail.title}}</span>
                                <span v-if="detail.discount > 0" class="hidden md:block text-[12px] w-fit px-2 h-6 pt-1 mt-2 text-white rounded-md text-center bg-orange-500">{{ detail.discount}}% Descuento</span>
                            </div>
                        </div>

                        <div class="flex items-center flex-col md:flex-row flex-wrap gap-4">
                            <div class="flex flex-row gap-4">
                                <span class="text-lg font-medium">Cantidad: </span> <span class="text-lg text-gray-500">{{ detail.amount}}</span>
                            </div>
                            <div class="flex flex-row gap-4">
                                <span class="text-lg font-medium">SubTotal: </span> <span class="text-lg text-gray-500">{{ Globalization.currencyFormat.format(detail.price / (1 - (detail.discount / 100))) }}</span>
                            </div>
                            <div class="flex-1 flex flex-row gap-4">
                                <span class="text-lg font-medium">Descuentos: </span> <span class="text-lg text-gray-500">{{ Globalization.currencyFormat.format((detail.price / (1 - (detail.discount / 100))) - detail.price)}}</span>
                            </div>
                            <div class="flex-1 items-end flex flex-col mx-5">
                                <div class="flex flex-row gap-4">
                                    <span class="text-lg font-medium">Total: </span> <span class="text-lg text-gray-500">{{ Globalization.currencyFormat.format(detail.total) }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

                <div class="mx-10 flex flex-col items-end">
                    <div class="flex-1 items-end flex flex-row gap-4">
                        <span class="text-lg font-medium">Total: </span> <span class="text-lg text-gray-500">{{ Globalization.currencyFormat.format(totals.totalAmount) }}</span>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <div class="flex flex-col" v-else>
        <div class="px-0 md:p-4 mx-0 md:mx-auto">
            <img src="/not-found.png" alt="not-found">
        </div>

        <span class="mt-4 text-2xl md:text-4xl w-full block text-center">Pedido no Encontrado</span>
        <Button @click="()=>{router.push('/');}" label="Regresar al Inicio" size="large" class="mx-auto mt-4"/>
    </div>
    <Toast />
</template>

<script lang="ts" setup>
    import {ref, defineProps} from 'vue';

    import { useToast } from "primevue/usetoast";
    import { useMediaQuery } from '@vueuse/core';
    import { Globalization } from '~/helpers/globalization';
    import type { OrderItem } from '~/types/dashboard/products';
    import {fetchWrapper} from "~/helpers/fetch-wrapper";

    // Meta configuration
    definePageMeta({
        layout:'public'
    });
    const props = defineProps<{ readonly orderNumber: string, readonly showBreadCrumb: boolean, readonly forceUpdate: boolean}>();
    const toast = useToast();
    const router=useRouter();
    const isMobile = useMediaQuery('(max-width: 600px)');

    /********************* 
    | DATA
    **********************/
    // Main
    const errorPage=ref<string>('');
    const currentOrder=ref<OrderItem>({
        order_number: '',
        total: 0,
        email:  '',
        fullname:  '',
        telephone:  '',
        province__name:  '',
        locality__name:  '',
        city:  '',
        address:  '',
        reference:  '',
        last_update_date:  '',
        provider_id: -1,

        details: []
    });

    const totals = computed(() => {
        let totalAmount=0;
        currentOrder.value.details.forEach(({ total }) => {
            totalAmount+=total;
        });
        return { totalAmount };
    });

    const home = ref({
        icon: 'pi pi-home',
        label: 'Inicio',
        route: '/'
    });
    const items = ref<object[]>([{
            label: 'Mis Pedidos',
            route: '/store/orders/'
        },
        {
            label: 'Detalles'
        }
    ]);

    /********************* 
    | METHODS
    **********************/
    const doExport = async () => {
        const params=new URLSearchParams();
        params.append('_format', 'pdf');
        params.append('order_number', currentOrder.value.order_number);

        const meta= import.meta.env.VITE_API_URL === undefined?'https://emprender-radix.com/api' : import.meta.env.VITE_API_URL;
        const url = `${meta}/orders/export?${params}`;
        fetch(url, {
            method: 'GET'
        }).then(response => {
            if (response.ok) {
                return response.blob();
            }
            throw new Error('Network response was not ok.');
        }).then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'Pedido-'+currentOrder.value.order_number+'.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        }).catch(error => toast.add({ severity: 'error', summary: 'Error', detail: 'Error al eliminar: '+JSON.stringify('There was a problem with the fetch operation:', error), life: 6000 }));
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        const params=new URLSearchParams();
        params.append('order_id', props.orderNumber);
        currentOrder.value=await fetchWrapper.get('/orders/info?'+params).catch((err:string)=>{
            errorPage.value=err;
        });
    });

    watch([() => props.orderNumber, () => props.forceUpdate], async(newOrders) => {
        const params=new URLSearchParams();
        params.append('order_id', props.orderNumber);
        currentOrder.value=await fetchWrapper.get('/orders/info?'+params).catch((err:string)=>{
            errorPage.value=err;
        });
    });
</script>
