<template>
    <div class="flex flex-col shadow-xl mx-0 md:mx-52 mt-8 py-5 bg-white">
        <form @submit.prevent="doSave">
            <div class="flex flex-wrap flex-row px-8">
                <div class="flex flex-col basis-full md:basis-1/2  gap-2 mb-5 px-4">
                    <label for="company_name" class="text-zinc-900">Nombre Empresa:</label>
                    <InputText 
                    placeholder="Nombre de la Empresa" 
                    id="company_name" 
                    autocomplete="off" 
                    
                    v-model:model-value="companyDataForm.company_name" 
                    :class="{'!border !border-red-500': $companyDataValidator.company_name.$invalid}"
                    @input="$companyDataValidator.company_name.$touch()" 
                    aria-describedby="company-data-name-help"
                    />
                    <small id="company-data-name-help" v-if="$companyDataValidator.company_name.required.$invalid && $companyDataValidator.company_name.$dirty" class="text-red-600">Nombre Empresa requerido.</small>
                    <small id="company-data-name-help" v-if="$companyDataValidator.company_name.minLength.$invalid && $companyDataValidator.company_name.$dirty" class="text-red-600">Nombre demasiado corto.</small>
                </div>

                <div class="flex flex-col basis-full md:basis-1/2 gap-2 mb-5 px-4">
                    <label for="email" class="text-zinc-900">Correo Electr&oacute;nico:</label>
                    <InputText 
                    placeholder="Correo Electronico de la Empresa" 
                    id="email" 
                    autocomplete="off" 
                    
                    v-model:model-value="companyDataForm.customer_service_email"
                    :class="{'!border !border-red-500': $companyDataValidator.customer_service_email.$invalid}"
                    @input="$companyDataValidator.customer_service_email.$touch()" 
                    aria-describedby="company-data-email-help"
                    />
                    <small id="company-data-email-help" v-if="$companyDataValidator.customer_service_email.required.$invalid && $companyDataValidator.customer_service_email.$dirty" class="text-red-600">Email requerido.</small>
                    <small id="company-data-email-help" v-if="$companyDataValidator.customer_service_email.email.$invalid && $companyDataValidator.customer_service_email.$dirty" class="text-red-600">Email inválido.</small>
                </div>

                <div class="flex flex-col basis-full md:basis-1/2 gap-2 mb-5 px-4">
                    <label for="telephone" class="text-zinc-900">N&uacute;mero T&eacute;lefono:</label>
                    <InputText 
                    placeholder="Número Télefono de la Empresa" 
                    id="telephone" 
                    autocomplete="off" 

                    v-model:model-value="companyDataForm.customer_service_telephone" 
                    :class="{'!border !border-red-500': $companyDataValidator.customer_service_telephone.$invalid}"
                    @input="$companyDataValidator.customer_service_telephone.$touch()" 
                    aria-describedby="company-data-telephone-help"
                    />
                    <small id="company-data-telephone-help" v-if="$companyDataValidator.customer_service_telephone.required.$invalid && $companyDataValidator.customer_service_telephone.$dirty" class="text-red-600">Teléfono requerido.</small>
                </div>

                <div class="flex flex-col basis-full md:basis-1/2 gap-2 mb-5 px-4">
                    <label for="whatsapp" class="text-zinc-900">Número de WhatsApp(pagos):</label>
                    <InputText 
                    placeholder="Número WhatsApp Pagos" 
                    id="whatsapp" 
                    autocomplete="off" 
                    
                    v-model:model-value="companyDataForm.whatsapp_telephone" 
                    :class="{'!border !border-red-500': $companyDataValidator.whatsapp_telephone.$invalid}"
                    @input="$companyDataValidator.whatsapp_telephone.$touch()" 
                    aria-describedby="company-data-whatsapp-help"
                    />
                    <small id="company-data-whatsapp-help" v-if="$companyDataValidator.whatsapp_telephone.required.$invalid && $companyDataValidator.whatsapp_telephone.$dirty" class="text-red-600">Número de WhatsApp requerido.</small>
                </div>

                <div class="flex flex-col basis-full md:basis-1/2 gap-2 mb-5 px-4">
                    <label for="facebook" class="text-zinc-900">Facebook:</label>
                    <InputText 
                    placeholder="Facebook de la Empresa" 
                    id="facebook" 
                    autocomplete="off" 
                    v-model:model-value="companyDataForm.url_facebook" 
                    />
                </div>

                <div class="flex flex-col basis-full md:basis-1/2 gap-2 mb-5 px-4">
                    <label for="instagram" class="text-zinc-900">Instagram:</label>
                    <InputText 
                    placeholder="Instagram de la Empresa" 
                    id="instagram" 
                    autocomplete="off" 
                    v-model:model-value="companyDataForm.url_instagram" 
                    />
                </div>
                <div class="flex flex-col basis-full md:basis-1/2 gap-2 mb-5 px-4">
                    <label for="amount" class="text-zinc-900">Monto:</label>
                    <InputNumber 
                    v-model:model-value="companyDataForm.service_price" 
                    inputId="amount" 
                    mode="currency"
                    currency="ARS" 
                    locale="es-AR" 
                    />
                </div>

                <div class="flex flex-col basis-full gap-2 mb-5 px-4">
                    <label for="logo" class="text-zinc-900">Logo:</label>

                    <FileUpload 
                    v-model="uploadedFiles"
                    :show-cancel-button="false" 
                    :show-upload-button="false" 
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

                <div class="flex basis-full flex-row-reverse gap-2 mb-2  px-4">
                    <div class="flex sm:w-full md:w-2/4 lg:w-1/4 gap-4 mt-1">
                        <Button label="Cancelar" severity="secondary" outlined class="w-full" />
                        <Button
                        :pt="{
                            label: '!font-medium !text-white'
                        }"
                        class="!bg-blue-700 !border-blue-700 hover:!bg-blue-800 w-full inline-flex rounded-md px-4 py-2" 
                        label="Guardar"
                        type="submit"
                        />
                    </div>
                </div>
            </div>
        </form>
    </div>

    <Toast />
</template>

<script lang="ts" setup>
    import {ref, type UnwrapRef} from 'vue';

    import { useToast } from "primevue/usetoast";
    import { required, minLength, email } from '@vuelidate/validators';
    import useVuelidate from '@vuelidate/core';

    import type { FileUploadSelectEvent } from 'primevue/fileupload';
    import type { CompanyForm } from '~/types/dashboard/profile/company-data';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';

    // Meta configuration
    const toast = useToast();

    function getBase64(file: File) {
        return new Promise<string>((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result as string);
            reader.onerror = error => reject(error);
        });
    };

    const companyDataRules = computed(() => ({
        company_name: {
            required,
            minLength: minLength(5),
        },
        customer_service_email:{
            required,
            email
        },
        customer_service_telephone:{
            required
        },
        whatsapp_telephone: {
            required
        }
    }));

    /********************* 
    | DATA
    **********************/
    const uploadedFiles = ref([]);
    const previewImage = ref();
    const fileUpload = ref(); 

    const companyDataForm:UnwrapRef<CompanyForm> = reactive({
        company_name: '',
        logo: '',
        url_facebook: '',
        url_instagram: '',
        customer_service_email: '',
        customer_service_telephone: '',
        whatsapp_telephone: '',
        service_price: 0
    });
    const $companyDataValidator=useVuelidate(companyDataRules, companyDataForm);

    /********************* 
    | METHODS
    **********************/
    const triggerFileSelect = () => {
        fileUpload.value.$refs.fileInput.click(); 
    };
    const onSelect = async(event:FileUploadSelectEvent) => {
        const file = event.files[0];
        previewImage.value = URL.createObjectURL(file);
        companyDataForm.logo=await getBase64(file);
    };

    const doSave = async()=>{
        await fetchWrapper.post('/company-data/save', companyDataForm).then((msg)=>{
            toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
        }).catch((e)=>{
            toast.add({ severity: 'error', summary: 'Error', detail: 'Error al guardar: '+JSON.stringify(e), life: 6000 });
        });
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        const resp:CompanyForm = await fetchWrapper.get('/company-data/info');

        companyDataForm.company_name=resp.company_name;
        companyDataForm.customer_service_telephone=resp.customer_service_telephone;
        companyDataForm.customer_service_email=resp.customer_service_email;
        companyDataForm.logo=resp.logo;
        previewImage.value=resp.logo;

        companyDataForm.url_facebook=resp.url_facebook;
        companyDataForm.url_instagram=resp.url_instagram;
        companyDataForm.whatsapp_telephone=resp.whatsapp_telephone;
        companyDataForm.service_price=resp.service_price;
    });
</script>