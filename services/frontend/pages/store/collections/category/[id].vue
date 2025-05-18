<template>
    <div class="flex flex-col" v-if="errorPage.trim() === ''">
        <Breadcrumb :home="home" :model="items">
            <template #item="{ item, props }">
                <nuxt-link v-if="item.route" :to="item.route">
                    <span :class="[item.icon, 'text-color']" />
                    <span class="ml-2 text-primary font-semibold">{{ item.label }}</span>
                </nuxt-link>
                <span v-else class="block w-20 md:w-full truncate text-surface-700 dark:text-surface-0">{{ item.label }}</span>
            </template>
        </Breadcrumb>

        <ProductItemSelectorComponent :title="currentSubCategoryTitle" :products="productItems" :is-category="false" :is-sub-category="true"/>

    </div>

    <div class="flex flex-col" v-else>
        <div class="px-0 md:p-4 mx-0 md:mx-auto">
            <img src="/not-found.png" alt="not-found">
        </div>

        <span class="mt-4 text-2xl md:text-4xl w-full block text-center">Categoría no encontrada</span>
        <Button @click="()=>{router.push('/');}" label="Regresar al Inicio" size="large" class="mx-auto mt-4"/>
    </div>
</template>

<script lang="ts" setup>
    import { useMediaQuery } from '@vueuse/core';
    import {ref} from 'vue';

    import {fetchWrapper} from "~/helpers/fetch-wrapper";
    import type {ProductItem} from '~/types/dashboard/products';

    // Meta configuration
    definePageMeta({
        layout:'public'
    });
    const route=useRoute();
    const router=useRouter();

    /********************* 
    | DATA
    **********************/
    const isMobile = useMediaQuery('(max-width: 600px)');

    // Main
    const errorPage=ref<string>('');

    const currentCategoryTitle=ref<string>('');
    const currentSubCategoryTitle=ref<string>('');
    const currentCategoryId=ref<number>(-1);

    const productItems=ref<ProductItem[]>([]);

    const home = ref({
        icon: 'pi pi-home',
        label:  isMobile? '':'Inicio',
        route: '/'
    });
    const items = ref<object[]>([]);

    /********************* 
    | METHODS
    **********************/
    // Main

    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        const params=new URLSearchParams();
        params.append('subcategory_id', route.params.id.toString());
        const data = await fetchWrapper.get('/subcategories/info?'+params).catch((err:string)=>{
            errorPage.value=err;
        });
        productItems.value=await fetchWrapper.get('/products/public?'+params);
        productItems.value=productItems.value.concat(await fetchWrapper.get('/services/public?'+params));

        currentCategoryId.value=data["category__id"];
        currentCategoryTitle.value=data["category__title"];
        currentSubCategoryTitle.value=data["title"];

        items.value.push({label: currentCategoryTitle.value, route: '/store/collections/'+currentCategoryId.value});
        items.value.push({label: currentSubCategoryTitle});
    });
</script>