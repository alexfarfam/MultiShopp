<template>
    <div class="w-full mt-10">
        <div class="flex flex-row w-full gap-5 bg-white shadow-lg rounded-xl m-2 p-4">
            <div class="hidden md:block basis-5/12">
                <span class="text-2xl font-medium tracking-wide top-1 pl-2 relative">{{ props.title }}</span>
            </div>

            <div class="basis-6/12 md:basis-3/12">
                <IconField>
                    <InputIcon class="pi pi-search" />
                    <InputText v-model:model-value="currentFilterProduct" @keyup="filterProduct" size="small" class="w-full" placeholder="Realizar una búsqueda" />
                </IconField>
            </div>

            <div class="basis-6/12 md:basis-3/12">
                <Select v-model:model-value="currentOrder" @change="orderProduct" class="w-full text-sm" :options="filters" option-label="name" option-value="code" placeholder="Ordenar por" />
            </div>

            <div class="hidden md:flex grow justify-end">
                <SelectButton v-model="layout" :options="options" :allowEmpty="false">
                    <template #option="{ option }">
                        <i :class="[option === 'list' ? 'pi pi-bars' : 'pi pi-table']" />
                    </template>
                </SelectButton>
            </div>
        </div>

        <DataView class="mt-4" :value="filteredProductItems" :layout="layout" data-key="id">
            <template #list="slotProps">
                <div class="flex flex-col">
                    <div v-for="(item, index) in slotProps.items" :key="index">
                        <div class="flex flex-col sm:flex-row sm:items-center p-6 gap-4 shadow-md bg-white my-2" :class="{ 'border-t border-surface-200 dark:border-surface-700': index !== 0 }">
                            <nuxt-link class="md:w-40 relative" :to="(item.price?'/store/products/':'/store/services/')+item.id">
                                <img class="block xl:block mx-auto rounded w-full" :src="item.main_image" :alt="item.title" />
                                <span v-if="item.discount > 0" class="absolute top-0 left-0 rounded-md px-2 py-1 bg-[#D4AF37] text-white text-xs">
                                    {{item.discount}}% de descuento
                                </span>
                            </nuxt-link>
                            <div class="flex flex-col md:flex-row justify-between md:items-center flex-1 gap-6">
                                <div class="flex flex-row md:flex-col gap-2">
                                    <div class="flex flex-row gap-2">
                                        <span class="flex font-medium text-surface-500 dark:text-surface-400 text-sm">{{ item.subcategory__title }}</span>
                                        <div class="flex items-end gap-2 justify-end px-2">
                                            <Rating v-model="item.qualification" readonly/>
                                            <span class="text-surface-900 top-[0.2rem] relative font-medium text-sm">{{ item.qualification }}</span>
                                        </div>
                                    </div>

                                    <div>
                                        <div class="text-lg mt-1 flex gap-2">
                                            <span v-if="item.header_tag" class="rounded-md px-2 py-1 bg-[#D4AF37] text-white text-xs mr-1">
                                                {{ item.header_tag }}
                                            </span>
                                            <span class="truncate w-72 uppercase" :title="item.title">{{ item.title}}</span>
                                        </div>
                                    </div>
                                </div>

                                <div class="flex flex-col md:items-end gap-8">
                                    <div v-if="item.price" class="flex gap-5">
                                        <span class="text-[#D4AF37] flex-auto text-2xl font-semibold">{{Globalization.currencyFormat.format(item.price)}}</span>
                                        <span class="flex-auto pt-[0.2rem] text-lg font-normal text-slate-500 line-through">{{ Globalization.currencyFormat.format(item.reference_price) }}</span>
                                    </div>

                                    <Button @click="()=>{makePurchase(item)}" class="basis-full grow whitespace-nowrap !bg-[#D4AF37] !border-[#D4AF37]" icon="pi pi-shopping-cart" :label="item.price === undefined?'Solicitar':'Comprar' "></Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </template>

            <template #grid="slotProps">
                <div class="grid grid-cols-1 gap-4 md:grid-cols-4">
                    <div v-for="(item, index) in slotProps.items" :key="index" class="col-span-1 p-2">
                        <div class="shadow-md border border-surface-200 dark:border-surface-700 bg-surface-0 dark:bg-surface-900 rounded flex flex-col">
                            <nuxt-link class="flex justify-start" :to="(item.price?'/store/products/':'/store/services/')+item.id">
                                <img class="w-full h-80" :src="item.main_image" :alt="item.title" style="max-width: 500px"/>
                                <span v-if="item.discount > 0" class="absolute rounded-md px-2 py-1 bg-[#D4AF37] text-white text-xs">
                                    {{item.discount}}% de descuento
                                </span>
                            </nuxt-link>

                            <div class="p-4 md:p-6">
                                <div class="flex flex-col gap-2">
                                    <div class="flex flex-full">
                                        <span class="top-2 relative flex-auto font-medium text-surface-500 dark:text-surface-400 text-sm">{{ item.subcategory__title }}</span>
                                        <div class="flex-auto flex items-end gap-2 justify-end px-2">
                                            <Rating v-model="item.qualification" readonly/>
                                            <span class="text-surface-900 top-[0.2rem] relative font-medium text-sm">{{ item.qualification }}</span>
                                           
                                        </div>
                                    </div>

                                    <div>
                                        <div class="text-lg overflow-hidden truncate max-w-72 mt-1">
                                            <span v-if="item.header_tag" class="rounded-md px-2 py-1 bg-[#D4AF37] text-white text-xs mr-1">
                                                {{ item.header_tag }}
                                            </span>
                                            <span :title="item.title">{{ item.title}}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex flex-row gap-1 mt-4 md:mt-6">
                                    <span v-if="item.price" class="text-[#D4AF37] basis-20 text-2xl font-semibold">{{ Globalization.currencyFormat.format(item.price)}}</span>
                                    <span v-if="item.reference_price" class="basis-20 pt-[0.2rem] text-lg font-normal text-slate-500 line-through">{{ Globalization.currencyFormat.format(item.reference_price) }}</span>
                                    <Button @click="makePurchase(item)" class="basis-full grow !bg-[#D4AF37] !border-[#D4AF37]" :icon="item.price === undefined?'pi pi-thumbs-up':'pi pi-shopping-cart'" :label="item.price === undefined?'Solicitar': isMobile?'':'Comprar'"></Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </template>

            <template #empty>
                <div class="flex flex-col w-full my-10">
                    <span class="mt-10 block !text-4xl text-gray-500/[0.7] pi pi-folder-open w-full text-center"></span>
                
                    <h2 class="mt-4 mb-4 block font-normal text-[28px] text-gray-500/[0.7] w-full text-center" v-if="currentFilterProduct.trim() === ''  && (isCategory||isSubCategory)">{{ props.title }}</h2>
                    <h2 class="mt-4 mb-4 block font-normal text-[28px] text-gray-500/[0.7] w-full text-center" v-if="currentFilterProduct.trim() !== ''">Producto no Encontrado</h2>

                    <span class="mb-30 block text-[22px] text-gray-400/[0.8] w-full text-center" v-if="currentFilterProduct.trim() === '' && (isCategory||isSubCategory)">No hay productos para esta {{isSubCategory?'sub':''}}categor&iacute;a</span>
                    <span class="mb-30 block text-[22px] text-gray-400/[0.8] w-full text-center" v-if="currentFilterProduct.trim() !== ''">No hay productos para '{{ currentFilterProduct }}'</span>

                    <div class="w-full text-center mt-4">
                        <Button v-if="route.path !== '/'" @click="()=>{router.push('/');}" size="large" label="Regresar al Inicio" class="mt-4"/>
                    </div>
                </div>
            </template>
        </DataView>
    </div>

    <PaymentFormComponent :items="productList"/>
    <Payment2FormComponent :items="productList"/>
    
</template>

<script lang="ts" setup>
    import {ref} from 'vue';
    import { useMediaQuery } from '@vueuse/core';
    import { sendEvent } from '~/composables/useMitt';

    import type { CartItem } from '~/types';
    import type {ProductItem} from '~/types/dashboard/products';
    import { Globalization } from '~/helpers/globalization';

    // Meta configuration
    definePageMeta({
        layout:'public'
    });
    const props=defineProps(
        ['products', 'title', 'isCategory', 'isSubCategory']
    );
    const route=useRoute();
    const router=useRouter();

    /********************* 
    | DATA
    **********************/
    //
    const filters = ref([
        { name: 'Destacados', code: 'featured' },
        { name: 'Más Vendidos', code: 'best_sellers' },
        { name: 'Más Recientes', code: 'most_recent' },
        { name: 'Precios Altos a Bajos', code: 'high_to_low_prices' },
        { name: 'Precios Bajos a Altos', code: 'low_to_high_prices' }
    ]);

    const isMobile = useMediaQuery('(max-width: 600px)');
    const layout =  ref<'list' | 'grid' | undefined>('grid');
    const options = ref<string[]>(['list', 'grid']);
    
    // Filter
    const globalLoading = ref<boolean>(true);
    const currentFilterProduct=ref<string>('');
    const discountOptions=ref<number[]>([]);

    const tagOptions=ref<string[]>([]);

    // Main
    const currentOrder=ref<string>('featured');
    const productList=ref<CartItem[]>([]);

    const filteredProductItems=ref<ProductItem[]>([]);
    const productItems=ref<ProductItem[]>([]);
    
    /********************* 
    | METHODS
    **********************/
    //Filter
    const filterProduct = ()=>{
        const filter=currentFilterProduct.value.toLowerCase();
        filteredProductItems.value=productItems.value.filter(entry=>{
            return (
                entry.title.toLowerCase().includes(filter) || entry.header_tag.toLowerCase().includes(filter) ||
                (entry.discount?entry.discount.toString().includes(filter):false) || (entry.price?(Globalization.currencyFormat.format(entry.price)).toString().includes(filter):false) ||
                (entry.reference_price?(Globalization.currencyFormat.format(entry.reference_price)).toString().includes(filter):false)
            );
        });
    }

    // Main
    const orderProduct=async ()=>{
        switch(currentOrder.value){
            case "featured":
                filteredProductItems.value.sort((a,b) => (
                   b.qualification - a.qualification
                ));
                break;
            case "best_sellers":
                filteredProductItems.value.sort((a,b) => (
                   b.orders - a.orders
                ));
            case "most_recent":
                filteredProductItems.value.sort((a,b) => (
                   new Date(b.last_update_date).getTime() - new Date(a.last_update_date).getTime()
                ));
                break;
            case "high_to_low_prices":
                filteredProductItems.value.sort((a,b) => (
                    (b.price) - (a.price)
                ));
                break;
            case "low_to_high_prices":
                filteredProductItems.value.sort((a,b) => (
                    (a.price) - (b.price)
                ));
                break;
        }
    };
    const initialize = () => {
        productItems.value = props.products;
        filteredProductItems.value = productItems.value;

        const discounts = productItems.value.map(item => item.discount);
        discountOptions.value = [...new Set(discounts)];
        discountOptions.value.sort((a, b) => a - b);

        const tags = productItems.value.map(item => item.header_tag);
        tagOptions.value = [...new Set(tags)];
        tagOptions.value.sort((a, b) => a.localeCompare(b));
        globalLoading.value=false;
    };

    //
    const makePurchase = (item:ProductItem)=>{
        productList.value=[{
            id: item.id,
            title: item.title,
            img: item.main_image,
            price: item.price,
            reference_price: item.reference_price,
            discount: item.discount,
            amount: 1,
            total: item.price,
            header_tag: item.header_tag,
            responsible__id: item.responsible__id,
            selected: true
        }];

        if(item.with_reservation){
            sendEvent('modal:payment-form2', {item_id: item.id, provider_id: item.responsible__id});
        }else{
            sendEvent('modal:payment-form', {product_id: item.id, provider_id: item.responsible__id});
        }

        
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(initialize);

    watch(() => props.products, (newProducts) => {
        initialize();
        globalLoading.value=false;
        currentFilterProduct.value=' ';
    });

</script>