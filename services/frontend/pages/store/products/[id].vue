<template>
    <div class="flex flex-col" v-if="errorPage.trim() === ''" >
        <Breadcrumb :home="home" :model="items">
            <template #item="{ item, props }">
                <nuxt-link v-if="item.route" :to="item.route">
                    <span :class="[item.icon, 'text-color']" />
                    <span class="text-sm md:text-lg ml-0 md:ml-2 text-primary font-semibold">{{ item.label }}</span>
                </nuxt-link>
                <span v-else class="block w-20 md:w-full truncate text-surface-700 dark:text-surface-0">{{ item.label }}</span>
            </template>
        </Breadcrumb>

        <div class="flex flex-col md:flex-row gap-6 my-8 mx-0">
            <div class="basis-[59%] flex flex-col gap-6">
                <div class="bg-white shadow-md rounded-lg p-4">
                    <Galleria 
                    v-if="imagesProduct.length > 0"
                    :thumbnailsPosition="isMobile ? 'bottom': 'left'" 
                    :value="imagesProduct" 
                    :numVisible="isMobile?3:5"
                    :showItemNavigators="true" 
                    :showItemNavigatorsOnHover="true"
                    >
                        <template #item="slotProps">
                            <VImageMagnifier 
                            class="w-[60rem] m-0 md:m-10 h-[28rem] md:h-[48rem] rounded-md block"
                            :src="slotProps.item.image"
                            />
                        </template>

                        <template #thumbnail="slotProps">
                            <div class="grid gap-4 justify-center">
                                <img class="block w-36 h-32" :src="slotProps.item.image" :alt="slotProps.item.name" />
                            </div>
                        </template>
                    </Galleria>
                    
                    <p v-else class="w-full py-20 text-center text-2xl text-gray-500/[0.6]">Aún no hay una imágenes para este producto.</p>
                    
                </div>

                <div v-if="currentProduct.description.trim() !== '<p><br></p>'" class="html-visualizer bg-white shadow-md rounded-lg p-4 w-full" v-html="currentProduct.description">
                </div>
                <div v-else class="bg-white shadow-md rounded-lg p-4 w-full">
                    <p class="w-full py-20 text-center text-2xl text-gray-500/[0.6]">Aún no hay una descripción para este producto.</p>
                </div>

                <div class="bg-white shadow-md rounded-lg p-4 w-full">
                    <CommentsComponent :item-id="route.params.id.toString()" :is-service="false"/>
                </div>
            </div>

            <div v-if="!isMobile" class="order-none flex-1 flex flex-col">
                <div class="flex flex-col bg-white shadow-md rounded-lg p-4 sticky top-10">
                    <div class="flex-auto flex items-end gap-2 justify-start px-2">
                        <Rating v-model="currentProduct.qualification" readonly/>
                        <span v-if="!isMobile" class="text-[#737B97] top-1 relative">{{ currentProduct.qualification === null ? qualifications[0]:qualifications[currentProduct.qualification] }} ({{ currentProduct.comments_count }})</span> 
                        <span class="px-1 top-[0.3rem] relative">|</span> <span class="text-surface-900 top-[0.2rem] relative text-sm">{{ currentProduct.orders }} Compras Realizadas</span>
                    </div>

                    <span class="w-full text-3xl mx-2 my-5 text-slate-700/[0.8]">{{ currentProduct.title }}</span>

                    <div class="w-full flex flex-row">
                        <span v-if="currentProduct.discount > 0" class="rounded-md px-2 py-1 bg-[#D4AF37] text-white text-sm mx-2">
                            {{currentProduct.discount}}% de descuento
                        </span>
                        <span v-if="currentProduct.header_tag" class="rounded-md px-2 py-1 bg-[#D4AF37] text-white text-sm mx-2">
                            {{ currentProduct.header_tag }}
                        </span>
                    </div>

                    <div class="flex flex-row gap-10 p-2 my-4">
                        <span class="text-3xl font-medium text text-[#737B97]">
                            {{ Globalization.currencyFormat.format(currentProduct.price) }}
                        </span>

                        <span class="text-[21px] mt-1 text-[#737B97]">
                            De <span class="line-through">{{ Globalization.currencyFormat.format(currentProduct.reference_price) }}</span>
                        </span>
                    </div>

                    <div class="flex flex-col gap-3 p-2 m-4">
                        <div class="flex flex-row gap-4">
                            <span class="basis-[85%] text-lg font-medium text-[#737B97]">Sub-Total:</span>
                            <span class="flex-1 text-lg text-right text-[#737B97]">{{ Globalization.currencyFormat.format(currentProduct.reference_price )}}</span>
                        </div>

                        <div class="flex flex-row gap-4">
                            <span class="basis-[85%] text-lg font-medium text-[#737B97]">Descuentos:</span>
                            <span class="flex-1 text-lg text-right text-[#737B97]">{{ Globalization.currencyFormat.format(currentProduct.reference_price - currentProduct.price )}}</span>
                        </div>

                        <div class="flex flex-row gap-4">
                            <span class="basis-[85%] text-lg font-medium text-[#737B97]">Total (1 artículos):</span>
                            <span class="flex-1 text-lg text-right text-[#737B97]">{{ Globalization.currencyFormat.format(currentProduct.price )}}</span>
                        </div>
                    </div>

                    <div class="flex flex-col mt-2">
                        <span class="text-[#737B97] font-semibold text-lg m-2">Datos del Proveedor:</span>
                        <div class="p-2 flex flex-row gap-4">
                            <span class="basis-5/12 font-medium text-[#737B97]"><i class="pi pi-facebook"></i> Facebook:</span>
                            <a class="text-blue-800 flex-1 text-right" :href="providerInfo?.url_facebook">{{ providerInfo?.user__username }}</a>
                        </div>
                        <div class="p-2 flex flex-row gap-4">
                            <span class="basis-5/12 font-medium text-[#737B97]"><i class="pi pi-envelope"></i> Correo:</span>
                            <a class="text-blue-800 flex-1 text-right" :href="'mailto:'+providerInfo?.email">{{ providerInfo?.email }}</a>
                        </div>
                        <div class="p-2 flex flex-row gap-4">
                            <span class="basis-5/12 font-medium text-[#737B97]"><i class="pi pi-phone"></i> Teléfono:</span>
                            <a class="text-blue-800 flex-1 text-right" :href="'tel:'+providerInfo?.email">{{ providerInfo?.telephone }}</a>
                        </div>

                        <div class="p-2 flex flex-row gap-4">
                            <span class="basis-5/12 font-medium text-[#737B97]"><i class="pi pi-map-marker"></i> Dirección:</span>
                            <span class="text-blue-800 flex-1 text-right">{{ providerInfo?.address }}</span>
                        </div>
                    </div>

                    <div class="flex flex-col gap-3 p-2 m-4">
                        <span class="font-medium text-[#737B97]"><i class="pi pi-lock text-green-600 text-lg"></i> Privacidad Segura</span>
                        <span class="text-sm text-[#737B97]">
                            Ten la seguridad de que tu información se mantendrá segura y libre de riesgos. No vendemos tu información personal por dinero y solo utilizaremos tu información de acuerdo con nuestra política de privacidad y cookies.
                        </span>
                    </div>

                    <Button @click="makePurchase" class="mt-2" icon="pi pi-whatsapp" size="large" label="Comprar" />

                </div>
            </div>
        </div>

    </div>

    <div class="flex flex-col" v-else>
        <div class="px-0 md:p-4 mx-0 md:mx-auto">
            <img src="/not-found.png" alt="not-found">
        </div>

        <span class="mt-4 text-2xl md:text-4xl w-full block text-center">Producto no Encontrado</span>
        <Button @click="()=>{router.push('/');}" label="Regresar al Inicio" size="large" class="mx-auto mt-4"/>
    </div>

    <Button v-if="isMobile" @click="makePurchase" size="large" class="!fixed top-[90%] left-[15%] w-60" icon="pi pi-whatsapp" label="Comprar"/>
    <PaymentFormComponent :items="productList"/>
</template>

<script lang="ts" setup>
    import {ref} from 'vue';
    import { useMediaQuery } from '@vueuse/core';

    import {qualifications} from '~/helpers/constants';
    import {Globalization} from '~/helpers/globalization';
    import {fetchWrapper} from "~/helpers/fetch-wrapper";
    import type { CartItem } from '~/types';
    import type { FormContact } from '~/types/form';
    import type {ImageProduct, ProductItem} from '~/types/dashboard/products';


    // Meta configuration
    definePageMeta({
        layout:'public'
    });

    const route=useRoute();
    const router=useRouter();
    const isMobile = useMediaQuery('(max-width: 600px)');

    /********************* 
    | DATA
    **********************/
    //
    const home = ref({
        icon: 'pi pi-home',
        label:isMobile?'':'Inicio',
        route: '/'
    });
    const items = ref<object[]>([]);

    // Main
    const showPaymentModal=ref<boolean>(false);
    const providerInfo = ref<FormContact>();
    const errorPage=ref<string>('');
    const currentProduct=ref<ProductItem>({
        id: -1,
        title: '',
        header_tag: '',
        description: '',
        price: -1,
        reference_price: -1,
        show_offerts: false,
        discount: -1,
        main_image: '',
        category__id: -1,
        category__title: '',
        subcategory__id: -1,
        subcategory__title: '',
        qualification: 1,
        comments_count: 0,
        orders: 0,
        last_update_date: '',
        responsible__id: -1,
        responsible: -1
    });
    const imagesProduct=ref<ImageProduct[]>([]);
    const productList=ref<CartItem[]>([]);

    /********************* 
    | METHODS
    **********************/
    //Header

    const makePurchase = ()=>{
        productList.value=[{
            id: currentProduct.value.id,
            title: currentProduct.value.title,
            img: currentProduct.value.main_image,
            price: currentProduct.value.price,
            reference_price: currentProduct.value.reference_price,
            discount: currentProduct.value.discount,
            amount: 1,
            total: currentProduct.value.price,
            header_tag: currentProduct.value.header_tag,
            responsible__id: currentProduct.value.responsible__id,
            selected: true
        }];

        sendEvent('modal:payment-form', {item_id: currentProduct.value.id, provider_id: currentProduct.value.responsible});
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        const params=new URLSearchParams();
        params.append('product_id', route.params.id.toString());
        currentProduct.value = await fetchWrapper.get('/products/info?'+params).catch((err:string)=>{
            errorPage.value=err;
        });

        imagesProduct.value= await fetchWrapper.get('/products/images?'+params);
        imagesProduct.value.push({
            id: -1,
            name: "Imagen Principal",
            image: currentProduct.value.main_image
        });

        items.value.push({label: currentProduct.value.category__title, route: '/store/collections/'+currentProduct.value.category__id });
        items.value.push({label: currentProduct.value.subcategory__title, route: '/store/collections/category/'+currentProduct.value.subcategory__id });
        items.value.push({label: currentProduct.value.title});

        const params2 = new URLSearchParams();
        params2.append('provider_id', currentProduct.value.responsible.toString());
        providerInfo.value = await fetchWrapper.get('/globals/provider-info?'+params2);
    });

</script>

<style>
.p-galleria-thumbnails{
    margin-left: 2rem;
}
.p-galleria-thumbnails-viewport {
    height: 48rem!important;
}
.p-galleria-item {
    justify-content: unset!important;
    align-items: unset!important; 
}

@media (max-width: 600px) {
    .p-galleria-thumbnails{
        margin-left: 0px;
    }
    .p-galleria-thumbnails-viewport {
        height: unset!important;
    }
}
</style>