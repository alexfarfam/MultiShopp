<template>
    <div class="w-screen flex h-screen bg-gradient-to-r from-slate-100 to-slate-200" >
        
        <div class="m-auto rounded-sm border bg-white shadow w-10/12">
            <div class="flex flex-wrap items-center">
                <div class="hidden w-full xl:block xl:w-1/2">
                  <div class="px-24 py-16 text-center">
                    <nuxt-link class="mb-4 m-auto inline-block" to="/">
                        <img class="!w-12 !h-12 hidden dark:inline-block" src="/logo.png" alt="Logo">
                        <img class="inline-block !w-12 !h-12 dark:hidden" src="/logo.png" alt="Logo">
                        <span class="inline-block font-bold top-2 relative ml-2 text-2xl">EmprenderRadix</span>
                    </nuxt-link>

                    <p class="text-zinc-800 2xl:px-20">
                      Estimado usuario, tenga en cuenta que necesita realizar un pago mensual para poder usar este servicio.
                    </p>

                    <span class="mt-14 inline-block">
                        <img src="/banner.svg" alt="illustration">
                    </span>
                  </div>
                </div>

                <div class="w-full xl:w-1/2 xl:border-l-2">
                  <div class="w-full p-4 sm:p-12.5 xl:p-17.5">
                    <span class="mb-1 text-zinc-800 hidden md:block">Recupera el control!</span>
                    <h2 class="mb-4 text-2xl font-bold text-black dark:text-white sm:text-title-xl2">
                        Recuperar Contraseña
                    </h2>

                    <p class="text-zinc-800 text-sm pb-6 2xl:px-20 block md:hidden">
                        Estimado usuario, tenga en cuenta que necesita realizar un pago mensual para poder usar este servicio.
                    </p>

                    <form @submit.prevent="submitRecover" autocomplete="new-password">
                        <div class="mb-4">
                            <label class="mb-2.5 block font-medium text-black dark:text-white" for="email">Correo Electrónico:</label>
                            <InputText 
                            v-model:model-value="recoverState.email"
                            type="email"  
                            autocomplete="new-password" 
                            class="w-full h-14" 
                            placeholder="Ingresa tu correo electrónico" 
                            id="email" 
                            :class="{'!border !border-red-500': $recoverValidator.email.$invalid && $recoverValidator.email.$dirty}"
                            @input="$recoverValidator.email.$touch()" 
                            aria-describedby="recover-email-help"
                            />
                            <small id="recover-email" v-if="$recoverValidator.email.required.$invalid && $recoverValidator.email.$dirty" class="text-red-600">Correo Electrónico requerido.</small>
                            <small id="recover-email" v-else-if="$recoverValidator.email.email.$invalid && $recoverValidator.email.$dirty" class="text-red-600">Correo Electrónico inválido.</small>
                        </div>
                       
                        <div class="mb-5">
                            <Button :disabled="recoverLoading || $recoverValidator.email.$invalid" :loading="recoverLoading" type="submit" class="h-14 font-medium text-white transition hover:bg-opacity-90" fluid label="Resetear" />
                        </div>

                        <div class="mt-6 text-center">
                            <p class="font-medium">
                                Ya tienes una cuenta?
                                <span class="text-blue-500 cursor-pointer">
                                    <nuxt-link to="/dashboard/login">Acceder</nuxt-link>
                                </span>
                            </p>
                        </div>
                    </form>
                  </div>
                </div>

            </div>
        </div>
    </div>

    <Toast />
</template>

<script lang="ts" setup>
    import {ref,  type UnwrapRef } from 'vue';

    import { useVuelidate } from '@vuelidate/core'
    import { required, email } from '@vuelidate/validators'
    import { useToast } from "primevue/usetoast";

    import type { UserRecoverForm } from '~/types/auth';
    import {useAuthStore} from '~/stores/auth.store';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';

    // Meta configuration
    definePageMeta({
        'layout': 'empty'
    });

    const toast = useToast();
    const router=useRouter();
    const authStore = useAuthStore();
    const {user} = storeToRefs(authStore);

    const recoverRules = computed(() => ({
        email: {
            required,
            email
        }
    }));

    // Redirect to home if already logged in
    if (user.value?.username && user.value?.is_superuser) {
        router.push('/dashboard');
    }
    /********************* 
    | DATA
    **********************/
    //
    const recoverLoading=ref<boolean>(false);
    const recoverState:UnwrapRef<UserRecoverForm> = reactive({
        email: ''
    });

    const $recoverValidator=useVuelidate(recoverRules, recoverState);

    /********************* 
    | METHODS
    **********************/
    //
    const submitRecover = async()=>{
        const isValid = await $recoverValidator.value.$validate();
        if(isValid){
            recoverLoading.value=true;
            await fetchWrapper.post('/auth2/users/reset_password/', {email: recoverState.email}).then(() => {
                recoverLoading.value=false;
                toast.add({ severity: 'success', summary: 'Éxito', detail: 'Se a enviado un correo con el enlace de recuperación a '+recoverState.email+'!', life:1500 });
            }).catch(error =>{
                toast.add({ severity: 'error', summary: 'Error', detail: JSON.stringify(error), life: 8000 });;
                recoverLoading.value=false;
            });
        }
    };
    /********************* 
    | MOUNT
    **********************/
</script>

<style scoped>
    *:not(".pi"){
        font-family: 'Satoshi-Normal'!important;
    }
</style>