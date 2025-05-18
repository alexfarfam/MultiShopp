<template>
    <div class="flex flex-col shadow-xl mx-0 md:mx-52 mt-8 py-5 bg-white">
        <div class="flex flex-wrap flex-row px-8">
                <div class="flex flex-col basis-full gap-2 mb-5 px-4">
                    <label for="username" class="text-zinc-900">Nombre Usuario:</label>
                    <InputText 
                    disabled
                    class="w-full rounded-lg border-[1.5px] bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:!border-blue-800 active:!border-blue-800 disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white" 
                    placeholder="Nombre Usuario" 
                    id="username" 
                    autocomplete="off" 
                    v-model:model-value="userDataForm.username" 
                    />
                </div>

                <div class="flex flex-col basis-full gap-2 mb-5 px-4">
                    <label for="email" class="text-zinc-900">Correo Electr&oacute;nico:</label>
                    <InputText 
                    disabled
                    class="w-full rounded-lg border-[1.5px] bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:!border-blue-800 active:!border-blue-800 disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white" 
                    placeholder="Correo Electrónico" 
                    id="email" 
                    autocomplete="off" 
                    v-model:model-value="userDataForm.email"
                    />
                </div>

                <div class="flex flex-row basis-full gap-2 mb-5 p-4">
                    <Checkbox disabled binary v-model:model-value="userDataForm.is_confirmed" inputId="confirmed" name="confirmed"/>
                    <label for="confirmed" class="text-zinc-900">Email Confirmado?</label>
                </div>

                <div class="flex flex-col basis-full gap-2 mb-5 px-4">
                    <label for="email" class="text-zinc-900">Fecha Registro:</label>
                    <DatePicker disabled v-model:model-value="userDataForm.joined_date" showIcon fluid/>
                </div>
        </div>
    </div>

    <Toast />
</template>

<script lang="ts" setup>
    import {type UnwrapRef} from 'vue';

    import type { UserDataItem } from '~/types/dashboard/profile/user-data';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';

    // Meta configuration
    /********************* 
    | DATA
    **********************/
    const userDataForm:UnwrapRef<UserDataItem> = reactive({
        username: '',
        email: '',
        is_confirmed: false,
        joined_date: new Date()
    });

    /********************* 
    | METHODS
    **********************/


    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        const resp:UserDataItem = await fetchWrapper.get('/contact-data/info');
        userDataForm.username=resp.username;
        userDataForm.email=resp.email;
        userDataForm.is_confirmed=resp.is_confirmed;
        userDataForm.joined_date=resp.joined_date;
    });
</script>