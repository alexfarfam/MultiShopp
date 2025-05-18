<template>
    <div v-if="text.trim() !== ''" v-html="text" class="html-visualizer"></div>

    <div v-else class="p-52">
        <svg-icon class="block mx-auto text-gray-500/[0.5] mb-4" size="55" type="mdi" :path="mdiPencilOff"></svg-icon>
        <span class="block text-center text-[29px] text-gray-500/[0.5]">Aún no hay datos para esta página.</span>
    </div>
</template>
<script lang="ts" setup>
    import { mdiPencilOff } from '@mdi/js';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';

    // Meta configuration
    definePageMeta({
        layout:'public'
    });
    const route = useRoute();

    /********************* 
    | DATA
    **********************/
    const text=ref<string>('');

    /********************* 
    | METHODS
    **********************/
    //Header

    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        await fetchWrapper.get('/extras/'+route.name?.toString()).then((data:string)=>{
            text.value=data;
        }).catch(()=>{
            text.value='';
        });
    });

</script>