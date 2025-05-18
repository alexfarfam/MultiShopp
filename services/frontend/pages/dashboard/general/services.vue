<template>
    <div>
        <DataView class="!bg-transparent" :value="filteredServiceData" data-key="id">
            <template #list="slotProps">
                <div class="flex flex-col gap-6">
                    <div v-for="(item, index) in slotProps.items" :key="index">
                        <div class="flex flex-row p-2 gap-2 border border-surface-200 bg-white shadow-md rounded-xl ">
                            <div class="w-18 md:w-20 relative">
                                <Image class="mt-2 !h-28 md:!h-12" :src="item.main_image" alt="Image" width="150" preview />
                            </div>
                            <div class="flex flex-col md:flex-row justify-between md:items-center flex-1 gap-6">
                                <div class="flex flex-row md:flex-col justify-between items-start gap-3">
                                    <div>
                                        <div class="flex flex-col md:flex-row gap-1 md:gap-2">
                                            <span class="text-base font-medium mt-2">{{ item.title }}</span>
                                            <span class="text-[12px] w-fit px-2 h-6 pt-1 mt-2 text-white rounded-md text-center bg-orange-500">{{ item.subcategory__title}}</span>
                                            <span v-if="item.header_tag" class="text-[12px] w-fit px-2 h-6 pt-1 mt-2 text-white rounded-md text-center bg-purple-500">{{ item.header_tag}}</span>
                                        </div>

                                        <div class="mt-4 md:mt-2 flex flex-col md:flex-row gap-1 md:gap-3">
                                            <!--<div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Dìas Disponibles: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ formatWeeks(item.weeks)}}</span>
                                            </div>
                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Hora Inicio: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ formatTo12Hour(item.start_time)}}</span>
                                            </div>
                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Hora Fin: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ formatTo12Hour(item.end_time)}}</span>
                                            </div> -->
                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Mostrar Reservación: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ item.with_reservation ? 'Sí':'No'}}</span>
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
                <span class="mt-4 block text-2xl text-gray-400/[0.8] w-full text-center">Sin servicios para mostrar</span>
            </template>
        </DataView>
    </div>

    <Dialog dismissable-mask v-model:visible="showEditModal" modal :header="formTitle" :style="{ width: '90vw' }">
        <Accordion value="0">
            <AccordionPanel value="0">
                <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Información Principal</AccordionHeader>
                <AccordionContent>
                    <form class="p-1 md:p-6 w-full">
                        <div class="flex flex-wrap w-full flex-col md:flex-row gap-4">
                            <div class="flex basis-[21%] flex-col gap-4 mb-4">
                                <label for="title" class="font-semibold">Título:</label>
                                <InputText 
                                v-model:model-value="serviceForm.title"
                                id="title" 
                                :class="{'!border !border-red-500': $serviceValidator.title.$invalid && $serviceValidator.title.$dirty}"
                                @input="$serviceValidator.title.$touch()" 
                                aria-describedby="service-title-help"

                                placeholder="Título" 
                                class="w-full"
                                />
                                <small id="category-title-help" v-if="$serviceValidator.title.required.$invalid && $serviceValidator.title.$dirty" class="text-red-600">Título requerido.</small>
                                <small id="category-title-help" v-else-if="$serviceValidator.title.minLength.$invalid && $serviceValidator.title.$dirty" class="text-red-600">Título demasiado corto.</small>
                            </div>

                            <div class="flex basis-[21%] flex-col gap-4 mb-4">
                                <label for="header-tag" class="font-semibold">Tag Cabecera:</label>
                                <InputText v-model:model-value="serviceForm.header_tag" id="header-tag" placeholder="Tag Cabecera" />
                            </div>

                            <div class="flex basis-[21%] flex-col gap-4 mb-4">
                                <label for="subcategory" class="font-semibold">Sub Categoría:</label>
                                <Select 
                                :options="subcategoryOptions"
                                option-label="label"
                                option-value="value"

                                v-model:model-value="serviceForm.subcategory"
                                id="subcategory" 
                                :class="{'!border !border-red-500': $serviceValidator.subcategory.$invalid && $serviceValidator.subcategory.$dirty}"
                                @input="$serviceValidator.subcategory.$touch()" 
                                aria-describedby="service-subcategory-help"

                                placeholder="Sub Categoría"
                                empty-message="Sin Categorías para mostrar"
                                />
                                <small id="service-subcategory-help" v-if="$serviceValidator.subcategory.required.$invalid && $serviceValidator.subcategory.$dirty" class="text-red-600">Subcategoría requerida.</small>
                            </div>
                            <div class="flex basis-[21%] flex-col gap-4 mb-4">
                                <label for="approximate_duration" class="font-semibold">Duración Sesión(en minutos):</label>
                                <InputNumber placeholder="Duración Sesión" v-model="serviceForm.approximate_duration" inputId="approximate_duration" suffix=" min" fluid />
                            </div>

                            <div class="flex basis-[10%] flex-row gap-4 mb-4">
                                <Checkbox class="relative top-0 md:top-14" v-model:model-value="serviceForm.with_reservation" :binary="true" inputId="with_reservation" />
                                <label for="with_reservation" class="relative top-0 md:top-14">Mostrar Horario</label>
                            </div>

                            <div class="flex basis-full flex-col md:flex-row gap-4 mb-4 flex-wrap">
                                <label for="subcategory" class="font-semibold basis-full">Horario de Atención:</label>
                                <div class="flex flex-row gap-2 basis-[24%]" v-for="day in daysOfWeek" :key="day.value">
                                    <label :for="day.value" class="w-[4.7rem] flex-none">{{ day.label }}: </label>
                                    <DatePicker v-model="availability[day.value].start_time" timeOnly hour-format="12" :stepMinute="30" placeholder="Hora de inicio"/>
                                    <DatePicker v-model="availability[day.value].end_time" timeOnly hour-format="12" :stepMinute="30" placeholder="Hora de fin"/>
                                </div>
                            </div>

                            <div class="flex basis-full flex-col gap-4 mb-4">
                                <div class="w-full flex flex-col gap-2">
                                    <label for="description" class="flex-auto font-semibold">Descripción:</label>
                                    <SummernoteEditor v-model="serviceForm.description"/>
                                </div>
                            </div>

                            <div class="flex basis-full flex-col gap-4 mb-4">
                                <label for="discount" class="font-semibold">Imagen Principal:</label>
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
                        </div>
                    </form>
                </AccordionContent>
            </AccordionPanel>

            <AccordionPanel value="1">
                <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Detalles</AccordionHeader>
                <AccordionContent>
                    <div class="my-6 flex flex-row gap-2">
                        <InputText v-model:model-value="subServiceTitle" placeholder="Subservicio"/>
                        <Button @click="addNewSubService" :disabled="subServiceTitle.trim() === ''" class="uppercase" label="Agregar" severity="sucess" icon="pi pi-plus" size="small" />
                    </div>

                    <div v-if="subServices.length > 0" class="flex flex-col gap-2">
                        <span class="mt-2 font-medium">Listado de Subservicios:</span>
                        <div v-for="(sub, index) in subServices" class="flex flex-row gap-2">
                            <InputText class="h-10" :disabled="!editingSubservice" v-model:model-value="subServices[index]" size="small"/>

                            <Button @click="editSubService(index)" severity="info" :icon=" editingSubservice ? 'pi pi-check':'pi pi-pencil' " rounded text />
                            <Button @click="removeSubService(index)" severity="warn" icon="pi pi-trash" rounded text />
                        </div>
                    </div>
                </AccordionContent>
            </AccordionPanel>

            <AccordionPanel value="2">
                <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Imágenes Extras</AccordionHeader>
                <AccordionContent>
                    <FileUpload 
                    :show-cancel-button="false" 
                    :show-upload-button="false" 
                    choose-label="Cargar"
                    class="normal"
                    accept="image/*" 
                    :maxFileSize="1000000"
                    :multiple="true"
                    @select="onSelectMultiple"
                    >
                        <template #content>
                            <div class="flex !h-80 overflow-scroll flex-col gap-8 pt-4">
                                <div v-if="images.length > 0">
                                    <div class="flex flex-wrap gap-4">
                                        <div v-for="(file, index) of images" :key="file.id" class="p-8 rounded-border flex flex-col border border-surface items-center gap-4">
                                            <div>
                                                <img role="presentation" :alt="file.name" :src="file.image" width="100" height="50" />
                                            </div>
                                            <span class="font-semibold text-ellipsis max-w-60 whitespace-nowrap overflow-hidden">{{ file.name }}</span>
                                            <Button @click="onRemoveMultiple(file.id, file.name, index)" icon="pi pi-times" outlined rounded severity="danger" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </template>

                        <template #empty>
                            <span v-if="images.length === 0" class="p-8 block text-center w-full text-2xl text-gray-400">
                                Arrastre y suelte archivos aquí para cargarlos.
                            </span>
                        </template>

                    </FileUpload>
                </AccordionContent>
            </AccordionPanel>
        </Accordion>

        <template #footer>
            <div class="flex flex-row gap-4">
                <Button severity="secondary" label="Cancelar" @click="showEditModal = false" />
                <Button @click="confirmEdit" :disabled="loadingSubmit" :loading="loadingSubmit" label="Aceptar" />
            </div>
        </template>
    </Dialog>

    <Toast />
    <ConfirmDialog></ConfirmDialog>
</template>

<script lang="ts" setup>
    import {ref, type UnwrapRef} from 'vue';
    import { cloneDeep} from 'lodash-es';

    import { useConfirm } from "primevue/useconfirm";
    import { useToast } from "primevue/usetoast";
    import { required, minLength } from '@vuelidate/validators';
    import useVuelidate from '@vuelidate/core';
    import type { FileUploadSelectEvent } from 'primevue/fileupload';

    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import { useListen } from '~/composables/useMitt';
    import type {ImageService, ServiceForm, ServiceItem} from '~/types/dashboard/services';
    import type { GenericObject, SelectOption } from '~/types';
    import { daysOfWeek } from '~/helpers/constants';

    // Meta configuration
    const confirm = useConfirm();
    const toast = useToast();

    function resetForm(){
        serviceForm.title='';
        serviceForm.header_tag='';
        serviceForm.description='';
        serviceForm.main_image='';
        serviceForm.subcategory='';
        serviceForm.images=[];

        previewImage.value=false;
        $serviceValidator.value.$reset();
    };
    const serviceRules = computed(() => ({
        title: {
            required,
            minLength: minLength(4),
        },
        subcategory: {
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
    function convertToTime(dateString:string) {
        if (!dateString) return null;
        if (typeof dateString === 'object') {
            return dateString;
        }

        const [hours, minutes, seconds] = dateString.split(":");
        const milliseconds = parseFloat(seconds) * 1000;

        const date = new Date(Date.UTC(
            new Date().getUTCFullYear(),
            new Date().getUTCMonth(),
            new Date().getUTCDate(),
            parseInt(hours, 10),
            parseInt(minutes, 10),
            0,
            milliseconds
        ));

        return date;
    }

    const availability = ref(daysOfWeek.reduce((acc:GenericObject, day) => {
        acc[day.value] = { start_time: null, end_time: null };
        return acc;
    }, {}));

    /********************* 
    | DATA
    **********************/
    const currentId = ref<number>(-1);
    const loadingSubmit=ref<boolean>(false);
    const formTitle=ref<string>('Nuevo Servicio');

    const showEditModal=ref<boolean>(false);
    const serviceData=ref<ServiceItem[]>([]);
    const filteredServiceData=ref<ServiceItem[]>([]);

    const serviceForm:UnwrapRef<ServiceForm> = reactive({
        title: '',
        header_tag: '',
        description: '',
        main_image: '',
        approximate_duration: 0,
        with_reservation: false,
        opening_hours: {},
        subservices:[],

        subcategory: '',
        images: [],
    });

    const subServiceTitle=ref<string>('');
    const subServices=ref<string[]>([]);
    const editingSubservice = ref<boolean>(false);

    const $serviceValidator=useVuelidate(serviceRules, serviceForm);

    const subcategoryOptions=ref<SelectOption[]>([]);
    const uploadedFiles = ref([]);
    const previewImage = ref();
    const fileUpload = ref(); 
    const images = ref<ImageService[]>([]);

    /********************* 
    | METHODS
    **********************/
    //
    const triggerFileSelect = () => {
        fileUpload.value.$refs.fileInput.click(); 
    };

    const onSelect = async(event:FileUploadSelectEvent) => {
        const file = event.files[0];
        previewImage.value = URL.createObjectURL(file);
        serviceForm.main_image=await getBase64(file);
    };
    const onSelectMultiple = async(event:FileUploadSelectEvent) => {
        const file = event.files[images.value.filter(entry=> !entry.image.startsWith('http')).length];
        images.value.push({
            id: Math.random(),
            name: file.name === undefined ? '' : file.name,
            image: await getBase64(file)
        });
    };
    const onRemoveMultiple = async(id:number, name: string, index:number)=>{
        const params = new URLSearchParams();
        params.append('img_id', id.toString());

        confirm.require({
            message: 'Seguro(a) que quieres borrar "'+name+'"?',
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
                params.append('img_id', JSON.stringify(id));
                await fetchWrapper.delete('/services/image?'+params).then((msg)=>{
                    serviceForm.images.splice(index, 1);

                    toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
                }).catch((e)=>{
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Error al eliminar: '+JSON.stringify(e), life: 6000 });
                });
            }
        });
    };

    const addNewSubService = ()=>{
        subServices.value.push(subServiceTitle.value);
        subServiceTitle.value='';
    };
    const editSubService = (index:number)=>{
        editingSubservice.value = !editingSubservice.value;
    };
    const removeSubService = (index:number)=>{
        confirm.require({
            message: 'Seguro(a) que quieres borrar el subservicio?',
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
                subServices.value.splice(index, 1);
            }
        });

    };
    const doNew =()=>{
        resetForm();
        currentId.value=-1;
        formTitle.value='Nuevo Servicio';
        showEditModal.value=true;
    };

    const doEdit = async (id:number)=>{
        currentId.value=id;
        const index = filteredServiceData.value.findIndex(obj => obj.id === currentId.value);
        const obj = filteredServiceData.value[index];

        serviceForm.title=obj.title;
        serviceForm.header_tag=obj.header_tag;
        serviceForm.description=obj.description;
        serviceForm.main_image=obj.main_image;
        serviceForm.subcategory=obj.subcategory__id.toString();
        serviceForm.approximate_duration=obj.approximate_duration;
        serviceForm.with_reservation=obj.with_reservation;
        serviceForm.opening_hours=obj.opening_hours;
        serviceForm.subservices = obj.subservices;
        previewImage.value=obj.main_image;
        subServices.value=obj.subservices;

        if(Object.keys(serviceForm.opening_hours).length > 0){
            availability.value=serviceForm.opening_hours;
            Object.keys(availability.value).forEach((key:string) =>{
                availability.value[key]={
                    start_time: availability.value[key]['start_time'] === null ? null:convertToTime(availability.value[key]['start_time']),
                    end_time: availability.value[key]['end_time'] === null ? null:convertToTime(availability.value[key]['end_time']),
                };
            });
        }else{
            availability.value= daysOfWeek.reduce((acc:GenericObject, day) => {
                acc[day.value] = { start_time: null, end_time: null };
                return acc;
            }, {});
        }
        const params = new URLSearchParams();
        params.append('service_id', currentId.value.toString());
        images.value=await fetchWrapper.get('/services/images?' + params);

        formTitle.value='Editar Servicio';
        showEditModal.value=true;
    };

    const confirmDelete = (id:number) => {
        const index = filteredServiceData.value.findIndex(obj => obj.id ===id);
        const obj = filteredServiceData.value[index];

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
                params.append('service_ids', JSON.stringify([id]));
                await fetchWrapper.delete('/services/delete?'+ params).then((msg)=>{
                    filteredServiceData.value=filteredServiceData.value.filter(item => item.id !== id);
                    serviceData.value=serviceData.value.filter(item => item.id !== id);

                    toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
                }).catch((e)=>{
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Error al eliminar: '+JSON.stringify(e), life: 6000 });
                });
            }
        });
    };

    const confirmEdit = async()=>{
        serviceForm.images=images.value.map(e=>e.image);
        serviceForm.opening_hours=availability.value;
        serviceForm.subservices=subServices.value;

        if(currentId.value === -1){
            await fetchWrapper.post('/services/service', serviceForm).then((resp)=>{
                filteredServiceData.value.push(resp['data']);

                toast.add({ severity: 'success', summary: 'Confirmación', detail: resp['msg'], life: 5000 });
                showEditModal.value = false;
            }).catch((e)=>{
                toast.add({ severity: 'error', summary: 'Error', detail: 'Error al guardar: '+JSON.stringify(e), life: 7000 });
            });
        }else{
            const params = new URLSearchParams();
            params.append('service_id', currentId.value.toString());

            await fetchWrapper.put('/services/service?'+params, serviceForm).then((resp)=>{
                const index = filteredServiceData.value.findIndex(obj => obj.id === currentId.value);
                filteredServiceData.value[index]=resp['data'];

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
        filteredServiceData.value=serviceData.value.filter(entry=>{
            return (
                entry.title.toLowerCase().includes(search) ||
                entry.header_tag.toLowerCase().includes(search) ||
                entry.subcategory__title.toLowerCase().includes(search)
            );
        });
    });

    onMounted(async()=>{
        serviceData.value=await fetchWrapper.get('/services/services');
        filteredServiceData.value=cloneDeep(serviceData.value);

        subcategoryOptions.value=await fetchWrapper.get('/subcategories/options');
    });
</script>