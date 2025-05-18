<template>
    <div class="flex flex-col" v-if="errorPage.trim() === ''">
        <Breadcrumb :home="home" :model="items">
            <template #item="{ item, props }">
                <nuxt-link v-if="item.route" :to="item.route">
                    <span :class="[item.icon, 'text-color']" />
                    <span class="ml-2 text-primary font-semibold">{{ item.label }}</span>
                </nuxt-link>
                <span v-else class="truncate text-surface-700 dark:text-surface-0">{{ item.label }}</span>
            </template>
        </Breadcrumb>

        <div class="flex flex-row flex-wrap gutter-4 mt-10" v-if="flag === 'info'">
            <nuxt-link class="mx-0 my-4 md:mx-4 w-28 md:w-32" :to="'/store/collections/category/'+item.id" v-for="(item, index) in subCategoryItems">
                <img class="w-24 md:w-28 h-24 md:h-[108px] rounded-full" :src="item.image" :alt="item.title">
                <span class="mt-4 break-words text-base md:text-lg text-center w-full block">{{ item.title }}</span>
            </nuxt-link>
        </div>

        <ProductItemSelectorComponent :title="currentCategoryTitle" :products="productItems" :is-category="true" :is-sub-category="false"/>
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
    import type {ProductItem} from '~/types/dashboard/products';
    import type { CategoryItem } from '~/types/dashboard/categories';
    import type { LoosObject } from '~/types';
    import {qualifications} from '~/helpers/constants'
    import {fetchWrapper} from "~/helpers/fetch-wrapper";

    // Meta configuration
    definePageMeta({
        layout:'public'
    });
    const route=useRoute();
    const router=useRouter();

    /********************* 
    | DATA
    **********************/
    // Main
    const errorPage=ref<string>('');
    const currentCategoryTitle=ref<string>('');
    const flag=ref<string>('');
    const globalLoading=ref<boolean>(true);

    const subCategoryItems=ref<CategoryItem[]>([]);
    const productItems=ref<ProductItem[]>([]);

    //
    const home = ref({
        icon: 'pi pi-home',
        label: 'Inicio',
        route: '/'
    });
    const items = ref<object[]>([]);

    /********************* 
    | METHODS
    **********************/

    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        const extras=['best-sellers', 'discounts', 'newcomers', 'promotions'];
        const extrasObj:LoosObject={
            'best-sellers': 'Más Vendidos',
            'discounts': 'Descuentos',
            'newcomers': 'Recién Llegados',
            'promotions': 'Promociones'
        };

        const category_id=route.params.id.toString();
        flag.value= extras.indexOf(category_id) > -1 ? 'extras':'info';
        const params=new URLSearchParams();
        
        if (flag.value === 'info'){
            params.append('category_id', category_id);
            const data = await fetchWrapper.get('/categories/info?'+params).catch((err:string)=>{
                errorPage.value=err;
            });

            subCategoryItems.value=await fetchWrapper.get('/subcategories/public?'+params);
            currentCategoryTitle.value=data["title"];
        }else{
            params.append('top', category_id);
            currentCategoryTitle.value=extrasObj[category_id];
        }

        items.value.push({label: currentCategoryTitle.value});
        productItems.value=await fetchWrapper.get('/products/public?'+params);
        productItems.value=productItems.value.concat(await fetchWrapper.get('/services/public?'+params));
        
        globalLoading.value=false;
    });
</script>