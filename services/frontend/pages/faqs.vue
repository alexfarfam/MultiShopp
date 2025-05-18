<template>
    <div v-if="faqs.length > 0">
        <div class="bg-gray-100 py-10">
            <div class="max-w-full md:max-w-[80%] mb-40 mx-auto px-4">
            <h1 class="text-3xl font-bold text-center mb-8">Preguntas Frecuentes</h1>
                <div class="space-y-4">
                    <div
                    v-for="(item, index) in faqs"
                    :key="index"
                    class="bg-white rounded-lg shadow-lg"
                    >
                        <button
                        @click="toggleAnswer(index)"
                        class="flex justify-between w-full px-4 py-6 text-left text-gray-800 font-semibold focus:outline-none"
                        >
                            <span class="text-xl">{{ (index + 1)+") "+item.question }}</span>
                            <svg
                            class="w-6 h-6 transform transition-transform duration-200"
                            :class="{ 'rotate-180': activeIndex === index }"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            >
                                <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M15 12h-6m6 0l-3 3m3-3l-3-3"
                                />
                            </svg>
                        </button>
                    <div
                    v-show="activeIndex === index"
                    class="px-4 py-6 bg-gray-50"
                    >
                        <div class="html-visualizer" v-html="item.answer"></div>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div v-else class="p-52">
        <svg-icon class="block mx-auto text-gray-500/[0.5] mb-4" size="55" type="mdi" :path="mdiPencilOff"></svg-icon>
        <span class="block text-center text-[29px] text-gray-500/[0.5]">Aún no hay datos para esta página.</span>
    </div>
</template>
<script lang="ts" setup>
    import { mdiPencilOff } from '@mdi/js';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import type { FAQItem } from '~/types/dashboard/extras';

    // Meta configuration
    definePageMeta({
        layout:'public'
    });
    const route = useRoute();

    /********************* 
    | DATA
    **********************/
    const faqs=ref<FAQItem[]>([]);
    const activeIndex = ref<number>(-1);

    /********************* 
    | METHODS
    **********************/
    //Header
    const toggleAnswer = (index:number) => {
        activeIndex.value = activeIndex.value === index ? -1 : index;
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        faqs.value=await fetchWrapper.get('/extras/'+route.name?.toString());
    });

</script>

<style scoped>
.rotate-180 {
  transform: rotate(180deg);
}
</style>