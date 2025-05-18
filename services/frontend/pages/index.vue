<template>
    <div>
        <div class="w-full mt-4">
            <span class="text-2xl font-medium tracking-wide top-1 pl-2 relative">
                Todas Nuestras Categor&iacute;as
            </span>
            
            <DataView class="mt-5 !h-[16rem] overflow-x-auto overflow-hidden" :value="categoriesData" layout="grid" data-key="id">
                <template #empty>
                    <span class="top-20 relative flex justify-center text-center items-center text-lg text-slate-400">
                        Sin Subcategorias para mostrar
                    </span>
                </template>

                <template #grid="slotProps">
                    <div id="main-categories-container" style="grid-auto-flow: column;overflow-x: auto;" class="grid md:grid-cols-10 gap-4">
                        <div
                        v-for="(item, index) in slotProps.items" 
                        :key="index" 
                        class="bg-transparent my-3 px-4 py-2 cursor-pointer col-span-1"
                        >
                            <nuxt-link @mouseover="stopInterval" @mouseleave="startInterval" class="w-full flex flex-col" :to="'/store/collections/'+item.id">
                                <Avatar class="!m-auto !w-28 !h-28" :image="item.image" shape="circle" />
                                <div v-if="item.description.trim() !== '' " class="w-28 xl:w-32 top-[-1rem] relative rounded-full text-white bg-[#D4AF37] p-1 m-auto text-sm text-center">
                                    {{ item.description }}
                                </div>
                                <div v-if="item.title.trim() !== ''" :class="item.description ? 'top-[-0.5rem]':'top-5'" class="text-[15px] mb-0 relative text-center uppercase">{{ item.title }}</div>
                            </nuxt-link>
                        </div>
                    </div>
                </template>
            </DataView>
        </div>

        <div class="w-full mt-10">
            <ProductItemSelectorComponent :title="'Nuevos Productos/Servicios'" :products="productItems" :is-category="false"/>
        </div>
    </div>
</template>

<script lang="ts" setup>
    import {ref} from 'vue';
    import { useMediaQuery } from '@vueuse/core';

    import type { ItemListbox } from '~/types';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import type { ProductItem } from '~/types/dashboard/products';
    
    // Meta configuration
    definePageMeta({
        'layout': 'public'
    });
    
    /********************* 
    | DATA
    **********************/
    //
    const isMobile = useMediaQuery('(max-width: 600px)');
    const categoriesData = ref<Array<ItemListbox>>([]);
    const scrollSpeed = 2;
    const productItems=ref<ProductItem[]>([]);

    /********************* 
    | METHODS
    **********************/
    var scrollInterval = null as NodeJS.Timeout|null;
    const stopInterval = ()=>{
        if (scrollInterval) {
            clearInterval(scrollInterval);
        }
    };
    const startInterval = () => {
        scrollInterval = setInterval(() => {
            const scrollContainer1 = document.querySelector("#main-categories-container");
            if (scrollContainer1) {
                const scrollStep = () => {
                    scrollContainer1.scrollLeft += scrollSpeed;
                    if (scrollContainer1.scrollLeft >= (scrollContainer1.scrollWidth - scrollContainer1.clientWidth - 1)) {
                        scrollContainer1.scrollLeft = 0; 
                    }
                };

                if (scrollInterval) {
                    clearInterval(scrollInterval);
                }
                scrollInterval = setInterval(scrollStep, 50);
            }
        }, 10);
    };


    /********************* 
    | MOUNT
    **********************/
    onMounted(async() => {
        categoriesData.value = await fetchWrapper.get('/categories/public');
        productItems.value=await fetchWrapper.get('/products/public');
        productItems.value=productItems.value.concat(await fetchWrapper.get('/services/public'));
    });

    onMounted(()=>{
        startInterval();
    });
    onBeforeUnmount(() => {
        if (scrollInterval) {
            clearInterval(scrollInterval);
        }
    });

</script>