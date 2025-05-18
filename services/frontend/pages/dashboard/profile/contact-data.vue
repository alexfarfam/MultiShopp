<template>
    <div class="flex flex-col shadow-xl mx-0 md:mx-52 mt-8 py-5 bg-white">
        <form @submit.prevent="doSave">
            <div class="flex flex-wrap flex-row px-8">
                <div class="flex flex-col basis-full md:basis-1/2  gap-2 mb-5 px-4">
                    <label for="company_name" class="text-zinc-900">Nombre Empresa:</label>
                    <InputText 
                    class="w-full rounded-lg border-[1.5px] bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:!border-blue-800 active:!border-blue-800 disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white" 
                    placeholder="Nombre de la Empresa" 
                    id="company_name" 
                    autocomplete="off" 
                    
                    v-model:model-value="contactDataForm.company_name" 
                    :class="{'!border !border-red-500': $contactDataValidator.company_name.$invalid}"
                    @input="$contactDataValidator.company_name.$touch()" 
                    aria-describedby="company-data-name-help"
                    />
                    <small id="company-data-name-help" v-if="$contactDataValidator.company_name.required.$invalid && $contactDataValidator.company_name.$dirty" class="text-red-600">Nombre Empresa requerido.</small>
                    <small id="company-data-name-help" v-if="$contactDataValidator.company_name.minLength.$invalid && $contactDataValidator.company_name.$dirty" class="text-red-600">Nombre demasiado corto.</small>
                </div>

                <div class="flex flex-col basis-full md:basis-1/2  gap-2 mb-5 px-4">
                    <label for="url-instagram" class="text-zinc-900">Instagram:</label>
                    <InputText 
                    class="w-full rounded-lg border-[1.5px] bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:!border-blue-800 active:!border-blue-800 disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white" 
                    placeholder="Instagram" 
                    id="url-instagram" 
                    autocomplete="off" 
                    
                    v-model:model-value="contactDataForm.url_instagram" 
                    :class="{'!border !border-red-500': $contactDataValidator.url_instagram.$invalid && $contactDataValidator.url_instagram.$dirty}"
                    @input="$contactDataValidator.url_instagram.$touch()" 
                    aria-describedby="contact-data-url-instagram-help"
                    />
                    <small id="contact-data-url-instagram-help" v-if="$contactDataValidator.url_instagram.url.$invalid && $contactDataValidator.url_instagram.$dirty" class="text-red-600">URL Instagram inválida.</small>
                </div>

                <div class="flex flex-col basis-full md:basis-1/2 gap-2 mb-5 px-4">
                    <label for="url-facebook" class="text-zinc-900">Facebook:</label>
                    <InputText 
                    class="w-full rounded-lg border-[1.5px] bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:!border-blue-800 active:!border-blue-800 disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white" 
                    placeholder="Facebook" 
                    id="url-facebook" 
                    autocomplete="off" 
                    
                    v-model:model-value="contactDataForm.url_facebook" 
                    :class="{'!border !border-red-500': $contactDataValidator.url_facebook.$invalid && $contactDataValidator.url_facebook.$dirty}"
                    @input="$contactDataValidator.url_facebook.$touch()" 
                    aria-describedby="contact-data-url-facebook-help"
                    />
                    <small id="contact-data-url-facebook-help" v-if="$contactDataValidator.url_facebook.url.$invalid && $contactDataValidator.url_facebook.$dirty" class="text-red-600">URL Facebook inválida.</small>
                </div>

                <div class="flex flex-col basis-full md:basis-1/2 gap-2 mb-5 px-4">
                    <label for="email" class="text-zinc-900">Correo Electr&oacute;nico:</label>
                    <InputText 
                    class="w-full rounded-lg border-[1.5px] bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:!border-blue-800 active:!border-blue-800 disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white" 
                    placeholder="Correo Electrónico" 
                    id="email" 
                    autocomplete="off" 
                    
                    v-model:model-value="contactDataForm.email"
                    :class="{'!border !border-red-500': $contactDataValidator.email.$invalid && $contactDataValidator.email.$dirty}"
                    @input="$contactDataValidator.email.$touch()" 
                    aria-describedby="contact-data-email-help"
                    />
                    <small id="contact-data-email-help" v-if="$contactDataValidator.email.email.$invalid && $contactDataValidator.email.$dirty" class="text-red-600">Email inválido.</small>
                </div>

                <div class="flex flex-col basis-full md:basis-1/2 gap-2 mb-5 px-4">
                    <label for="telephone" class="text-zinc-900">N&uacute;mero T&eacute;lefono:</label>
                    <InputText 
                    class="w-full rounded-lg border-[1.5px] bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:!border-blue-800 active:!border-blue-800 disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white" 
                    placeholder="Número Télefono" 
                    id="telephone" 
                    autocomplete="off" 

                    v-model:model-value="contactDataForm.telephone" 
                    :class="{'!border !border-red-500': $contactDataValidator.telephone.$invalid && $contactDataValidator.telephone.$dirty}"
                    @input="$contactDataValidator.telephone.$touch()" 
                    aria-describedby="contact-data-telephone-help"
                    />
                    <small id="contact-data-telephone-help" v-if="$contactDataValidator.telephone.required.$invalid && $contactDataValidator.telephone.$dirty" class="text-red-600">Teléfono requerido.</small>
                </div>

                <div class="flex flex-col basis-full md:basis-1/2 gap-2 mb-5 px-4">
                    <label for="whatsapp-telephone" class="text-zinc-900">N&uacute;mero T&eacute;lefono(WhatsApp):</label>
                    <InputText 
                    class="w-full rounded-lg border-[1.5px] bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:!border-blue-800 active:!border-blue-800 disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white" 
                    placeholder="Número Télefono(WhatsApp)" 
                    id="whatsapp-telephone" 
                    autocomplete="off" 
                    v-model:model-value="contactDataForm.whatsapp_telephone" 
                    />
                </div>

                <div class="flex flex-col basis-full md:basis-1/2 gap-2 mb-5 px-4">
                    <label for="address" class="text-zinc-900">Dirección:</label>
                    <InputText 
                    class="w-full rounded-lg border-[1.5px] bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:!border-blue-800 active:!border-blue-800 disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white" 
                    placeholder="Dirección" 
                    id="address" 
                    autocomplete="off" 
                    
                    v-model:model-value="contactDataForm.address" 
                    aria-describedby="contact-data-address-help"
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
    import {type UnwrapRef} from 'vue';

    import { useToast } from "primevue/usetoast";
    import { required, url, email, minLength } from '@vuelidate/validators';
    import useVuelidate from '@vuelidate/core';
    import type { ContactForm } from '~/types/dashboard/profile/contact-data';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import type { FileUploadSelectEvent } from 'primevue/fileupload';

    // Meta configuration
    function getBase64(file: File) {
        return new Promise<string>((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result as string);
            reader.onerror = error => reject(error);
        });
    };
    
    const toast = useToast();

    const contactDataRules = computed(() => ({
        company_name: {
            required,
            minLength: minLength(5),
        },

        url_instagram: {
            url
        },
        url_facebook: {
            url
        },
        email:{
            email
        },
        telephone:{
            required
        }
    }));

    /********************* 
    | DATA
    **********************/
    const contactDataForm:UnwrapRef<ContactForm> = reactive({
        company_name: '',
        logo: '',
        whatsapp_telephone: '',
        url_instagram: '',
        url_facebook: '',
        email: '',
        telephone: '',
        address: ''
    });
    const $contactDataValidator=useVuelidate(contactDataRules, contactDataForm);
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
        contactDataForm.logo=await getBase64(file);
    };

    const doSave = async()=>{
        const $valid = await $contactDataValidator.value.$validate();
        if ($valid){
            await fetchWrapper.post('/contact-data/save', contactDataForm).then((msg)=>{
                toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
            }).catch((e)=>{
                toast.add({ severity: 'error', summary: 'Error', detail: 'Error al guardar: '+JSON.stringify(e), life: 6000 });
            });
        }
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        const resp:ContactForm = await fetchWrapper.get('/contact-data/contact');
        contactDataForm.company_name=resp.company_name;
        contactDataForm.url_instagram=resp.url_instagram;
        contactDataForm.url_facebook=resp.url_facebook;
        contactDataForm.email=resp.email;
        contactDataForm.telephone=resp.telephone;
        contactDataForm.whatsapp_telephone=resp.whatsapp_telephone;
        contactDataForm.address=resp.address;

        contactDataForm.logo=resp.logo;
        previewImage.value=resp.logo;
    });
</script>