<template>
    <Accordion value="0">
        <AccordionPanel value="0">
            <AccordionHeader class="flex flex-row gap-4 !uppercase !bg-slate-400/[0.2]">
                <span class="flex-1">Acerca de</span>
                <Button @click="doSave" class="mr-5" size="small" icon="pi pi-save" label="Guardar cambios" />
            </AccordionHeader>
            <AccordionContent>
                <SummernoteEditor class="mb-5 top-5 relative" v-model="extrasForm.about"/>
            </AccordionContent>
        </AccordionPanel>

        <AccordionPanel value="1">
            <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Nuestra Compañia</AccordionHeader>
            <AccordionContent>
                <SummernoteEditor class="mb-5 top-5 relative" v-model="extrasForm.company"/>
            </AccordionContent>
        </AccordionPanel>

        <AccordionPanel value="2">
            <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Nuestra Historia</AccordionHeader>
            <AccordionContent>
                <SummernoteEditor class="mb-5 top-5 relative" v-model="extrasForm.history"/>
            </AccordionContent>
        </AccordionPanel>

        <AccordionPanel value="3">
            <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">¿Cómo Trabajamos?</AccordionHeader>
            <AccordionContent>
                <SummernoteEditor class="mb-5 top-5 relative" v-model="extrasForm.workflow"/>
            </AccordionContent>
        </AccordionPanel>

        <AccordionPanel value="4">
            <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Soporte</AccordionHeader>
            <AccordionContent>
                <SummernoteEditor class="mb-5 top-5 relative" v-model="extrasForm.support"/>
            </AccordionContent>
        </AccordionPanel>

        <AccordionPanel value="5">
            <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Políticas de Privacidad</AccordionHeader>
            <AccordionContent>
                <SummernoteEditor class="mb-5 top-5 relative" v-model="extrasForm.privacy_policy"/>
            </AccordionContent>
        </AccordionPanel>

        <AccordionPanel value="6">
            <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Términos y Condiciones</AccordionHeader>
            <AccordionContent>
                <SummernoteEditor class="mb-5 top-5 relative" v-model="extrasForm.terms_condition"/>
            </AccordionContent>
        </AccordionPanel>

        <AccordionPanel value="7">
            <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Preguntas Frecuentes (FAQ)</AccordionHeader>
            <AccordionContent class="p-2 flex flex-col">
                <div class="m-4 flex-1 flex flex-col items-end">
                    <Button @click="doNew" icon="pi pi-plus" label="Nueva"/>
                </div>

                <div v-if="filteredFaqsData.length === 0" class="p-4">
                    <svg-icon class="block mx-auto text-gray-500/[0.5] mb-4" size="55" type="mdi" :path="mdiPencilOff"></svg-icon>
                    <span class="block text-center text-2xl text-gray-500/[0.5] mb-10">Sin datos que mostrar.</span>
                </div>

                <div v-else class="p-4 flex flex-col gap-4">
                    <div class="m-4 shadow-lg rounded-md p-4 flex flex-row gap-4" v-for="(item, index) in filteredFaqsData">
                        <div class="basis-[4rem]">
                            <Avatar icon="pi pi-question-circle" class="mr-2" size="large" shape="circle" />
                        </div>

                        <div class="flex-1 flex flex-col gap-4">
                            <div class="flex flex-row gap-4">
                                <span class="flex-1 text-gray-500 text-lg">{{ item.question}}</span>
                                <div class="flex-none flex items-end flex-row-reverse md:flex-row gap-2">
                                    <Button size="small" class="!bg-[#4F61E3] !border-[#4F61E3]" @click="doEdit(item.id)" icon="pi pi-pencil" label="Editar"></Button>
                                    <Button size="small" @click="confirmDelete(item.id)" severity="danger" icon="pi pi-trash" label="Eliminar"></Button>
                                </div>

                            </div>

                            <div class="flex flex-col">
                                <div class="html-visualizer" v-html="item.answer"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </AccordionContent>
        </AccordionPanel>
    </Accordion>

    <Dialog dismissable-mask v-model:visible="showEditModal" modal :header="formquestion" :style="{ width: '25rem' }">
        <form @submit.prevent="confirmEdit">
            <div class="mb-4">
                <label class="mb-2.5 block font-medium text-black dark:text-white" for="question">Pregunta:</label>
                <InputText 
                v-model:model-value="faqForm.question"
                class="w-full h-12" 
                placeholder="Pregunta" 
                id="question" 
                :class="{'!border !border-red-500': $faqValidator.question.$invalid && $faqValidator.question.$dirty}"
                @input="$faqValidator.question.$touch()" 
                aria-describedby="faq-question-help"
                />
                <small id="faq-question-help" v-if="$faqValidator.question.required.$invalid && $faqValidator.question.$dirty" class="text-red-600">Pregunta requerida.</small>
                <small id="faq-question-help" v-else-if="$faqValidator.question.minLength.$invalid && $faqValidator.question.$dirty" class="text-red-600">Pregunta demasiada corta.</small>
            </div>

            <div class="mb-4">
                <label class="mb-2.5 block font-medium text-black dark:text-white" for="answer">Respuesta:</label>
                <SummernoteEditor 
                v-model:model-value="faqForm.answer"
                placeholder="Respuesta" 
                id="answer"
                />
                <small id="faq-answer-help" v-if="$faqValidator.answer.required.$invalid && $faqValidator.answer.$dirty" class="text-red-600">Respuesta requerida.</small>
                <small id="faq-answer-help" v-else-if="$faqValidator.answer.minLength.$invalid && $faqValidator.answer.$dirty" class="text-red-600">Respuesta demasiada corta.</small>
            </div>

            <div class="flex justify-end gap-2">
                <Button type="button" label="Cancelar" severity="secondary" @click="showEditModal = false"></Button>
                <Button :disabled="$faqValidator.question.$invalid || $faqValidator.answer.$invalid || loadingSubmit" :loading="loadingSubmit" type="submit" label="Guardar"></Button>
            </div>
        </form>
    </Dialog>

    <Toast />
    <ConfirmDialog></ConfirmDialog>
</template>

<script lang="ts" setup>
    import {ref, type UnwrapRef} from 'vue';
    import { useToast } from "primevue/usetoast";
    import { useConfirm } from "primevue/useconfirm";

    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import type { ExtrasForm, FAQForm, FAQItem } from '~/types/dashboard/extras';
    import { mdiPencilOff } from '@mdi/js';
    import useVuelidate from '@vuelidate/core';
    import { minLength, required } from '@vuelidate/validators';
    import { cloneDeep } from 'lodash-es';
        
    // Meta configuration
    definePageMeta({
        'layout': 'default'
    });
    function resetForm(){
        faqForm.answer='';
        faqForm.question='';

        $faqValidator.value.$reset();
    };

    const faqRules = computed(() => ({
        answer: {
            required,
            minLength: minLength(5),
        },
        question: {
            required,
            minLength: minLength(5),
        }
    }));

    const toast = useToast();
    const confirm=useConfirm();
    useListen('application:search' , (message:any) => {
        const search = (message.message as string).toLowerCase();
        filteredFaqsData.value=faqsData.value.filter(entry=>{
            return (
                entry.answer.toLowerCase().includes(search) ||
                entry.question.toLowerCase().includes(search) 
            );
        });
    });
    const doNew=()=>{
        resetForm();
        currentId.value=-1;
        formquestion.value='Nueva FAQ';
        showEditModal.value=true;
    };

    const doEdit = (id:number)=>{
        currentId.value=id;
        const index = filteredFaqsData.value.findIndex(obj => obj.id === currentId.value);
        const obj = filteredFaqsData.value[index];
        faqForm.question=obj.question;
        faqForm.answer=obj.answer;

        formquestion.value='Editar FAQ';
        showEditModal.value=true;
    };

    const confirmDelete = (id:number) => {
        const index = filteredFaqsData.value.findIndex(obj => obj.id === id);
        const obj = filteredFaqsData.value[index];

        confirm.require({
            message: 'Seguro(a) que quieres borrar "'+obj.question+'"?',
            header: 'Confirmar eliminación',
            icon: 'pi pi-info-circle',
            rejectLabel: 'Cancelar',
            rejectProps: {
                label: 'Cancelar',
                severity: 'secondary',
                outlined: true
            },
            acceptProps: {
                label: 'Confirmar',
                severity: 'danger'
            },
            accept: async() => {
                const params = new URLSearchParams();
                params.append('faq_ids', JSON.stringify([id]));
                await fetchWrapper.delete('/extras/faq?'+ params).then((msg)=>{
                    filteredFaqsData.value=filteredFaqsData.value.filter(item => item.id !== id);
                    faqsData.value=faqsData.value.filter(item => item.id !== id);

                    toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
                }).catch((e)=>{
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Error al eliminar: '+JSON.stringify(e), life: 6000 });
                });
            }
        });
    };

    const confirmEdit = async()=>{
        if(currentId.value === -1){
            await fetchWrapper.post('/extras/faq', faqForm).then((resp)=>{
                filteredFaqsData.value.push(resp['data']);

                toast.add({ severity: 'success', summary: 'Confirmación', detail: resp['msg'], life: 5000 });
                showEditModal.value = false;
            }).catch((e)=>{
                toast.add({ severity: 'error', summary: 'Error', detail: 'Error al guardar: '+JSON.stringify(e), life: 7000 });
            });
        }else{
            const params = new URLSearchParams();
            params.append('faq_id', currentId.value.toString());

            await fetchWrapper.put('/extras/faq?'+params, faqForm).then((resp)=>{
                const index = filteredFaqsData.value.findIndex(obj => obj.id === currentId.value);
                filteredFaqsData.value[index]=resp['data'];

                toast.add({ severity: 'success', summary: 'Confirmación', detail: resp['msg'], life: 5000 });
                showEditModal.value = false;
            }).catch((e)=>{
                toast.add({ severity: 'error', summary: 'Error', detail: 'Error al editar: '+JSON.stringify(e), life: 7000 });
            });      
        }
    };

    /********************* 
    | DATA
    **********************/
    const extrasForm:UnwrapRef<ExtrasForm> = reactive({
        about: '',
        company: '',
        history: '',
        workflow: '',
        support: '',
        privacy_policy: '',
        terms_condition: ''
    });

    const faqsData=ref<FAQItem[]>([]);
    const filteredFaqsData=ref<FAQItem[]>([]);

    const currentId = ref<number>(-1);
    const loadingSubmit=ref<boolean>(false);
    const formquestion=ref<string>('Nueva Pregunta/Respuesta');
    const showEditModal=ref<boolean>(false);

    const faqForm:UnwrapRef<FAQForm> = reactive({
        answer: '',
        question: ''
    });

    const $faqValidator=useVuelidate(faqRules, faqForm);

    /********************* 
    | METHODS
    **********************/
    const doSave= async()=>{
        await fetchWrapper.post('/extras/extras', extrasForm).then((msg)=>{
            toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
        }).catch((e)=>{
            toast.add({ severity: 'error', summary: 'Error', detail: 'Error al guardar: '+JSON.stringify(e), life: 6000 });
        });;
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        const data:ExtrasForm = await fetchWrapper.get('/extras/admin');
        extrasForm.about=data.about;
        extrasForm.company=data.company;
        extrasForm.history=data.history;
        extrasForm.privacy_policy=data.privacy_policy;
        extrasForm.support=data.support;
        extrasForm.terms_condition=data.terms_condition;
        extrasForm.workflow=data.workflow;

        faqsData.value= await fetchWrapper.get('/extras/faqs');
        filteredFaqsData.value=cloneDeep(faqsData.value);   
    });

</script>