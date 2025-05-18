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

                    <form @submit.prevent="submitConfirmRecover" autocomplete="new-password">
                        <div class="mb-4">
                            <label class="mb-2.5 block font-medium text-black dark:text-white" for="new-password">Contraseña:</label>
                            <Password 
                            fluid
                            toggle-mask 
                            v-model:model-value="confirmRecoverState.new_password"
                            autocomplete="new-password" 
                            class="w-full h-14" 
                            placeholder="Ingresa Contraseña" 
                            id="new-password" 
                            
                            promptLabel="Ingrese una contraseña"
                            weakLabel="Contraseña débil"
                            mediumLabel="Contraseña aceptable"
                            strongLabel="Contraseña robusta"

                            :class="{'!border !border-red-500': $confirmRecoverValidator.new_password.$invalid && $confirmRecoverValidator.new_password.$dirty}"
                            @input="$confirmRecoverValidator.new_password.$touch()" 
                            aria-describedby="new-password-help"
                            />
                            <small id="new-password-help" v-if="$confirmRecoverValidator.new_password.required.$invalid && $confirmRecoverValidator.new_password.$dirty" class="text-red-600">Contraseña Requerida.</small>
                        </div>
                       
                        <div class="mb-4">
                            <label class="mb-2.5 block font-medium text-black dark:text-white" for="re-new-password">Confirmar Contraseña:</label>
                            <Password 
                            fluid
                            toggle-mask 
                            :feedback="false"
                            v-model:model-value="confirmRecoverState.re_new_password"
                            autocomplete="re-new-password" 
                            class="w-full h-14" 
                            placeholder="Confirmar Contraseña" 
                            id="re-new-password" 
                            
                            :class="{'!border !border-red-500': $confirmRecoverValidator.re_new_password.$invalid && $confirmRecoverValidator.re_new_password.$dirty}"
                            @input="$confirmRecoverValidator.re_new_password.$touch()" 
                            aria-describedby="re-new-password-help"
                            />
                            <small id="re-new-password-help" v-if="$confirmRecoverValidator.re_new_password.sameAsPassword.$invalid && $confirmRecoverValidator.re_new_password.$dirty" class="text-red-600">Contraseñas no coinciden.</small>
                        </div>

                        <div class="mb-5">
                            <Button :disabled="confirmRecoverLoading || $confirmRecoverValidator.new_password.$invalid || $confirmRecoverValidator.re_new_password.$invalid " :loading="confirmRecoverLoading" type="submit" class="h-14 font-medium text-white transition hover:bg-opacity-90" fluid label="Resetear" />
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
    import { required, sameAs } from '@vuelidate/validators'
    import { useToast } from "primevue/usetoast";

    import type { UserConfirmRecoverForm } from '~/types/auth';
    import {useAuthStore} from '~/stores/auth.store';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';

    // Meta configuration
    definePageMeta({
        'layout': 'empty'
    });

    const toast = useToast();
    const router=useRouter();
    const route=useRoute();
    const authStore = useAuthStore();
    const {user} = storeToRefs(authStore);

    const confirmRecoverRules = computed(() => ({
        new_password: {
            required
        },
        re_new_password: {
            sameAsPassword:sameAs(confirmRecoverState.new_password)
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
    const confirmRecoverLoading=ref<boolean>(false);
    const confirmRecoverState:UnwrapRef<UserConfirmRecoverForm> = reactive({
        new_password: '',
        re_new_password: '',
        uid: '',
        token: ''
    });

    const $confirmRecoverValidator=useVuelidate(confirmRecoverRules, confirmRecoverState);

    /********************* 
    | METHODS
    **********************/
    //
    const submitConfirmRecover = async()=>{
        const isValid = await $confirmRecoverValidator.value.$validate();
        if(isValid){
            confirmRecoverLoading.value=true;
            const { _uid, _token } = route.query;

            await fetchWrapper.post('/auth2/users/reset_password_confirm/', confirmRecoverState).then(() => {
                confirmRecoverLoading.value=false;
                toast.add({ severity: 'success', summary: 'Éxito', detail: 'Contraseña recuperada con éxito!', life:1500 });

                setTimeout(()=>{
                    router.push('/dashboard/login');
                }, 1600);
            }).catch(error =>{
                toast.add({ severity: 'error', summary: 'Error', detail: JSON.stringify(error), life: 8000 });;
                confirmRecoverLoading.value=false;
            });
        }
    };
    /********************* 
    | MOUNT
    **********************/
    onMounted(async () => {
        const { uid, token } = route.query;
        if (!uid || !token){
            router.push('/');
        }else{
            confirmRecoverState.uid=new String(uid).toString();
            confirmRecoverState.token=new String(token).toString();
        }
    });
</script>

<style scoped>
    *:not(".pi"){
        font-family: 'Satoshi-Normal'!important;
    }
</style>