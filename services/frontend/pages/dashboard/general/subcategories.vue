<template>
    <div>
        <DataView class="!bg-transparent" :value="filteredSubcategoryData" data-key="id">
            <template #list="slotProps">
                <div class="flex flex-col gap-6">
                    <div v-for="(item, index) in slotProps.items" :key="index">
                        <div class="flex flex-row p-2 gap-2 border border-surface-200 bg-white shadow-md rounded-xl ">
                            <div class="w-18 md:w-20 relative">
                                <Image class="mt-2" :src="item.image" alt="Image" width="150" preview />
                            </div>
                            <div class="flex flex-col md:flex-row justify-between md:items-center flex-1 gap-6">
                                <div class="flex flex-row md:flex-col justify-between items-start gap-3">
                                    <div>
                                        <div class="flex flex-col md:flex-row gap-1 md:gap-2">
                                            <span class="text-base font-medium mt-2">{{ item.title }}</span>
                                            <span class="text-[12px] w-fit px-2 h-6 pt-1 mt-2 text-white rounded-md text-center bg-orange-500">{{ item.category__title}}</span>
                                        </div>

                                        <div class="mt-4 md:mt-2 flex flex-col gap-1 md:gap-3">
                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Descripción: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ item.description }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="flex mt-0 md:mt-4 flex-col md:items-end gap-3">
                                    <div class="flex flex-row-reverse md:flex-row gap-2">
                                        <Button class="!bg-[#4F61E3] !border-[#4F61E3]" @click="doEdit(item.id)" icon="pi pi-pencil" label="Editar"></Button>
                                        <Button @click="confirmDelete(item.id)" severity="danger" icon="pi pi-trash" label="Eliminar"></Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </template>

            <template #empty>
                <span class="mt-48 block !text-4xl text-gray-400/[0.8] pi pi-folder-open w-full text-center"></span>
                <span class="mt-4 block text-2xl text-gray-400/[0.8] w-full text-center">Sin subcategorías para mostrar</span>
            </template>
        </DataView>
    </div>

    <Toast />
    <ConfirmDialog></ConfirmDialog>

    <Dialog dismissable-mask v-model:visible="showEditModal" modal :header="formTitle" :style="{ width: '25rem' }">
        <form @submit.prevent="confirmEdit">
            <div class="mb-4">
                <label class="mb-2.5 block font-medium text-black dark:text-white" for="title">Título:</label>
                <InputText 
                v-model:model-value="subcategoryForm.title"
                class="w-full h-12" 
                placeholder="Ingresa un Título" 
                id="title" 
                :class="{'!border !border-red-500': $subcategoryValidator.title.$invalid && $subcategoryValidator.title.$dirty}"
                @input="$subcategoryValidator.title.$touch()" 
                aria-describedby="subcategory-title-help"
                />
                <small id="subcategory-title-help" v-if="$subcategoryValidator.title.required.$invalid && $subcategoryValidator.title.$dirty" class="text-red-600">Título requerido.</small>
                <small id="subcategory-title-help" v-else-if="$subcategoryValidator.title.minLength.$invalid && $subcategoryValidator.title.$dirty" class="text-red-600">Título demasiado corto.</small>
            </div>

            <div class="mb-4">
                <label class="mb-2.5 block font-medium text-black dark:text-white" for="title">Categoría:</label>
                <Select 
                :options="categoryOptions"
                option-label="label"
                option-value="value"

                v-model:model-value="subcategoryForm.category"
                class="w-full h-12" 
                placeholder="Selecciona una categoría" 
                id="category" 
                :class="{'!border !border-red-500': $subcategoryValidator.category.$invalid && $subcategoryValidator.category.$dirty}"
                @input="$subcategoryValidator.title.$touch()" 
                aria-describedby="subcategory-category-help"
                />
                <small id="subcategory-category-help" v-if="$subcategoryValidator.title.required.$invalid && $subcategoryValidator.title.$dirty" class="text-red-600">Título requerido.</small>
            </div>

            <div class="mb-4">
                <label class="mb-2.5 block font-medium text-black dark:text-white" for="description">Descripción:</label>
                <InputText
                :maxlength="30" 
                v-model:model-value="subcategoryForm.description"
                class="w-full h-12" 
                placeholder="Ingresa una Descripción" 
                id="description"
                />
            </div>

            <div class="mb-4">
                <label class="mb-2.5 block font-medium text-black dark:text-white" for="description">Imagen:</label>

                <FileUpload 
                id="main-upload"
                v-model="uploadedFiles"
                @select="onSelect"
                :customUpload="true"
                accept="image/*" 
                :maxFileSize="1000000"
                :auto="false"
                :file-limit="1"
                :multiple="false"
                ref="fileUpload"
                >
                    <template #content>
                        <div
                        class="mt-4 flex flex-col justify-center items-center h-40 border-dashed border-2 border-gray-300 p-4 rounded-lg cursor-pointer"
                        @click="triggerFileSelect"
                        >
                            <img v-if="previewImage" :src="previewImage" alt="Preview Image" class="max-w-full max-h-32 object-contain mb-2" />
                            
                            <div v-else class="flex flex-col justify-center items-center">
                                <i class="pi pi-inbox !text-4xl text-gray-400"></i>
                                <p class="text-gray-500 mt-2 text-center">Haz clic o arrastra un archivo aquí para cargarlo</p>
                            </div>
                        </div>
                    </template>
                </FileUpload>
            </div>

            <div class="flex justify-end gap-2">
                <Button type="button" label="Cancelar" severity="secondary" @click="showEditModal = false"></Button>
                <Button :disabled="loadingSubmit || $subcategoryValidator.title.$invalid || $subcategoryValidator.category.$invalid" :loading="loadingSubmit" type="submit" label="Guardar"></Button>
            </div>
        </form>
    </Dialog>
</template>

<script lang="ts" setup>
    import {ref, type UnwrapRef} from 'vue';
    import { cloneDeep } from 'lodash-es';

    import { useConfirm } from "primevue/useconfirm";
    import { useToast } from "primevue/usetoast";
    import { required, minLength } from '@vuelidate/validators';
    import useVuelidate from '@vuelidate/core';
    import type { FileUploadSelectEvent } from 'primevue/fileupload';

    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import { useListen } from '~/composables/useMitt';
    import type { SubCategoryItem, SubCategoryForm } from '~/types/dashboard/subcategories';
    import type { SelectOption } from '~/types';

    // Meta configuration
    const confirm = useConfirm();
    const toast = useToast();

    function resetForm(){
        subcategoryForm.title='';
        subcategoryForm.description='';
        subcategoryForm.image='';
        subcategoryForm.category='';

        previewImage.value=false;
        $subcategoryValidator.value.$reset();
    };
    const subcategoryRules = computed(() => ({
        title: {
            required,
            minLength: minLength(4),
        },
        category: {
            required
        }
    }));
    function getBase64(file: File) {
        return new Promise<string>((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result as string);
            reader.onerror = error => reject(error);
        });
    }
    /********************* 
    | DATA
    **********************/
    const currentId = ref<number>(-1);
    const loadingSubmit=ref<boolean>(false);
    const formTitle=ref<string>('Nueva SubCategoría');

    const showEditModal=ref<boolean>(false);
    const subcategoryData=ref<SubCategoryItem[]>([]);
    const filteredSubcategoryData=ref<SubCategoryItem[]>([]);

    const subcategoryForm:UnwrapRef<SubCategoryForm> = reactive({
        title: '',
        description: '',
        category: '',
        image: ''
    });

    const $subcategoryValidator=useVuelidate(subcategoryRules, subcategoryForm);

    const categoryOptions=ref<SelectOption[]>([]);
    const uploadedFiles = ref([]);
    const previewImage = ref();
    const fileUpload = ref(); 

    /********************* 
    | METHODS
    **********************/
    const triggerFileSelect = () => {
        fileUpload.value.$refs.fileInput.click(); 
    };

    const onSelect = async(event:FileUploadSelectEvent) => {
        const file = event.files[0];
        previewImage.value = URL.createObjectURL(file);
        subcategoryForm.image=await getBase64(file);
    };
    const doNew=()=>{
        resetForm();
        currentId.value=-1;
        formTitle.value='Nueva SubCategoría';
        showEditModal.value=true;
    };

    const doEdit = (id:number)=>{
        currentId.value=id;
        const index = filteredSubcategoryData.value.findIndex(obj => obj.id === currentId.value);
        const obj = filteredSubcategoryData.value[index];
        subcategoryForm.title=obj.title;
        subcategoryForm.description=obj.description;
        subcategoryForm.category=obj.category__id;
        previewImage.value=obj.image;

        formTitle.value='Editar SubCategoría';
        showEditModal.value=true;
    };

    const confirmDelete = (id:number) => {
        const index = filteredSubcategoryData.value.findIndex(obj => obj.id === id);
        const obj = filteredSubcategoryData.value[index];

        confirm.require({
            message: 'Seguro(a) que quieres borrar "'+obj.title+'"?',
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
                params.append('subcategory_ids', JSON.stringify([id]));
                await fetchWrapper.delete('/subcategories/delete?'+ params).then((msg)=>{
                    filteredSubcategoryData.value=filteredSubcategoryData.value.filter(item => item.id !== id);
                    subcategoryData.value=subcategoryData.value.filter(item => item.id !== id);

                    toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
                }).catch((e)=>{
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Error al eliminar: '+JSON.stringify(e), life: 6000 });
                });
            }
        });
    };

    const confirmEdit = async()=>{
        if(currentId.value === -1){
            await fetchWrapper.post('/subcategories/subcategory?', subcategoryForm).then((resp)=>{
                filteredSubcategoryData.value.push(resp['data']);

                toast.add({ severity: 'success', summary: 'Confirmación', detail: resp['msg'], life: 5000 });
                showEditModal.value = false;
            }).catch((e)=>{
                toast.add({ severity: 'error', summary: 'Error', detail: 'Error al guardar: '+JSON.stringify(e), life: 7000 });
            });
        }else{
            const params = new URLSearchParams();
            params.append('subcategory_id', currentId.value.toString());

            await fetchWrapper.put('/subcategories/category?'+params, subcategoryForm).then((resp)=>{
                const index = filteredSubcategoryData.value.findIndex(obj => obj.id === currentId.value);
                filteredSubcategoryData.value[index]=resp['data'];

                toast.add({ severity: 'success', summary: 'Confirmación', detail: resp['msg'], life: 5000 });
                showEditModal.value = false;
            }).catch((e)=>{
                toast.add({ severity: 'error', summary: 'Error', detail: 'Error al editar: '+JSON.stringify(e), life: 7000 });
            });      
        }
    };

    /********************* 
    | MOUNT
    **********************/
    useListen('application:add-new' , (message:any) => {
        doNew();
    });
    useListen('application:search' , (message:any) => {
        const search = (message.message as string).toLowerCase();
        filteredSubcategoryData.value=subcategoryData.value.filter(entry=>{
            return (
                entry.title.toLowerCase().includes(search) ||
                entry.description.toLowerCase().includes(search) 
            );
        });
    });

    onMounted(async()=>{
        subcategoryData.value=await fetchWrapper.get('/subcategories/subcategories');
        filteredSubcategoryData.value=cloneDeep(subcategoryData.value);

        categoryOptions.value=await fetchWrapper.get('/categories/options');
    });

</script>