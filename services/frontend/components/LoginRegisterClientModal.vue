<template>

    <Dialog class="w-[34rem]" :draggable="false" v-model:visible="showClientLogin" modal :closable="false" :dismissable-mask="true">
        <div v-show="currentTab !== 0" @click="previusTab" class="w-full px-2">
            <Button icon="pi pi-arrow-left" label="Regresar" text/>
        </div>

        <div v-show="currentTab===0" class="flex flex-col px-7">
            <div class="flex flex-col">
                <span class="text-2xl font-bold text-zinc-900 text-center">Inicia Sesi&oacute;n/Reg&iacute;strate</span>
                <span class="text-center mt-2 text-[15px] text-green-800">
                    <i class="pi pi-lock !text-[15px] text-green-900"></i> Todos tus datos estar&aacute;n seguros
                </span>
            </div>

            <div class="mt-6 flex flex-row gap-8">
                <div class="text-zinc-900 flex flex-col gap-1 flex-auto items-center align-middle">
                    <svg-icon class="icon" size="30" type="mdi" :path="mdiTruckFastOutline"></svg-icon>
                    <span class="font-medium">Compras y Pedidos</span>
                    <span class="text-sm font-normal text-center">Has seguimiento de todos tus pedidos.</span>
                </div>

                <div class="text-zinc-900 flex flex-col gap-1 flex-auto items-center align-middle">
                    <svg-icon class="icon" size="30" type="mdi" :path="mdiTagSearch"></svg-icon>
                    <span class="font-medium">B&uacute;squedas y suguerencias</span>
                    <span class="text-sm font-normal text-center">Obt&eacute;n suguerencias de acuerdo a tus b&uacute;squedas.</span>
                </div>
            </div>
           
            <form class="mt-10 flex flex-col gap-5">
                <div class="flex flex-col gap-2">
                    <label class="text-zinc-900" for="client-register-email">Correo Electrónico:</label>
                    <InputText 
                    id="client-register-email" 
                    fluid 
                    placeholder="Ingrese Correo Electrónico"

                    v-model:model-value="registerState.email"
                    :class="{'!border !border-red-500': $registerValidator.email.$invalid && $registerValidator.email.$dirty}"
                    @input="$registerValidator.email.$touch()" 
                    aria-describedby="client-register-email-help"
                    />
                    <small id="client-register-email-help" v-if="$registerValidator.email.required.$invalid && $registerValidator.email.$dirty" class="text-red-600">Correo Electrónico Requerido</small>
                    <small id="client-register-email-help" v-else-if="$registerValidator.email.email.$invalid && $registerValidator.email.$dirty" class="text-red-600">Correo Electrónico inválido.</small>
                </div>

                <Button @click="nextTab" label="Continuar" :disabled="$registerValidator.email.$invalid" fluid class=""/>
            </form>
        </div>

        <div v-show="currentTab===1" class="px-2">
            <div class="w-full p-2">
                <span class="w-full block font-semibold text-center text-slate-900 text-2xl">Inicia Sesión</span>
                <span class="w-full block text-center text-green-700 text-base pt-2"><i class="pi pi-lock"></i> Todos tus datos estarán seguros.</span>
                
                <form class="pt-6" @submit.prevent="submitLogin" autocomplete="new-password">
                    <div class="mb-4">
                        <label class="mb-2.5 block font-medium text-black dark:text-white" for="email">Correo Electrónico:</label>
                        <InputText 
                        v-model:model-value="loginState.email"
                        type="email"  
                        autocomplete="new-password" 
                        class="w-full h-12" 
                        placeholder="Ingresa tu correo electrónico" 
                        id="email" 
                        :class="{'!border !border-red-500': $loginValidator.email.$invalid && $loginValidator.email.$dirty}"
                        @input="$loginValidator.email.$touch()" 
                        aria-describedby="login-email-help"
                        />
                        <small id="login-email-help" v-if="$loginValidator.email.required.$invalid && $loginValidator.email.$dirty" class="text-red-600">Correo Electrónico requerido.</small>
                        <small id="login-email-help" v-else-if="$loginValidator.email.email.$invalid && $loginValidator.email.$dirty" class="text-red-600">Correo Electrónico inválido.</small>
                    </div>

                    <div class="mb-6">
                        <label class="mb-2.5 block font-medium text-black dark:text-white" for="login-password">Contraseña:</label>
                        <Password 
                        v-model:model-value="loginState.password"
                        autocomplete="new-password" 
                        :feedback="false" 
                        toggle-mask 
                        class="h-12" 
                        fluid 
                        placeholder="Ingresa tu contraseña" 
                        id="login-password" 
                        :class="{'!border !border-red-500': $loginValidator.password.$invalid && $loginValidator.password.$dirty}"
                        @input="$loginValidator.password.$touch()" 
                        aria-describedby="login-password-help"
                        />
                        <small id="login-password-help" v-if="$loginValidator.password.required.$invalid && $loginValidator.password.$dirty" class="text-red-600">Contraseña requerida.</small>
                        <div class="text-right">
                            <p @click="currentTab = 3" class="pt-4 text-sm font-medium text-sky-800 cursor-pointer">
                                ¿Olvidaste tu contraseña?
                            </p>
                        </div>
                    </div>

                    <div class="mb-5">
                        <Button :disabled="loginLoading || $loginValidator.email.$invalid || $loginValidator.password.$invalid" :loading="loginLoading" type="submit" class="h-12 !bg-orange-500 !border-orange-500 font-medium text-white transition hover:bg-opacity-90" fluid label="Login" />
                    </div>

                    <div class="w-full">
                        <Divider layout="horizontal" class="flex md:hidden" align="center">O</Divider>
                    </div>

                    <div class="mb-5">
                        <Button @click="currentTab = 2" type="button" class="h-12 font-medium !bg-sky-700 !border-sky-700 text-white transition hover:bg-opacity-90" fluid label="Crear una Cuenta" />
                    </div>
                </form>
            </div>
        </div>

        <div v-show="currentTab===2" class="px-2">
            <div class="w-full p-2">
                <span class="w-full block font-semibold text-center text-slate-900 text-2xl">Regístrate</span>
                <span class="w-full block text-center text-green-700 text-base pt-2"><i class="pi pi-lock"></i> Todos tus datos estarán seguros.</span>
            
                <form class="pt-6" @submit.prevent="submitRegister" autocomplete="new-password">
                    <div class="mb-4">
                        <label class="mb-2.5 block font-medium text-black dark:text-white" for="username">Nombre de Usuario:</label>
                        <InputText 
                        v-model:model-value="registerState.username"
                        autocomplete="new-password" 
                        class="h-12" 
                        fluid 
                        placeholder="Ingresa tu nombre de usuario" 
                        id="username" 
                        :class="{'!border !border-red-500': $registerValidator.username.$invalid && $registerValidator.username.$dirty}"
                        @input="$registerValidator.username.$touch()" 
                        aria-describedby="username-help"
                        />
                        <small id="username-help" v-if="$registerValidator.username.required.$invalid && $registerValidator.username.$dirty" class="text-red-600">Nombre Requerido</small>
                        <small id="username-help" v-else-if="$registerValidator.username.minLength.$invalid && $registerValidator.username.$dirty" class="text-red-600">Nombre debe ser menor que 5.</small>
                        <small id="username-help" v-else-if="$registerValidator.username.alphaNum.$invalid && $registerValidator.username.$dirty" class="text-red-600">Nombre debe de ser alfanumérico</small>
                    </div>

                    <div class="mb-4">
                        <label class="mb-2.5 block font-medium text-black dark:text-white" for="register-email">Correo Electrónico:</label>
                        <InputText 
                        v-model:model-value="registerState.email"
                        autocomplete="new-password" 
                        class="h-12" 
                        fluid 
                        placeholder="Ingresa tu correo electrónico" 
                        id="register-email" 
                        :class="{'!border !border-red-500': $registerValidator.email.$invalid && $registerValidator.email.$dirty}"
                        @input="$registerValidator.email.$touch()" 
                        aria-describedby="email-help"
                        />
                        <small id="email-help" v-if="$registerValidator.email.required.$invalid && $registerValidator.email.$dirty" class="text-red-600">Correo Electrónico Requerido</small>
                        <small id="email-help" v-else-if="$registerValidator.email.email.$invalid && $registerValidator.email.$dirty" class="text-red-600">Correo Electrónico inválido.</small>
                    </div>

                    <div class="mb-6">
                        <label class="mb-2.5 block font-medium text-black dark:text-white" for="register-password">Contraseña:</label>
                        <div class="relative">
                            <Password 
                            v-model:model-value="registerState.password"
                            autocomplete="new-password" 
                            :feedback="true" 
                            toggle-mask 
                            class="h-12" 
                            fluid 
                            placeholder="Ingresa tu contraseña" 
                            id="register-password" 
                            promptLabel="Ingrese una contraseña"
                            weakLabel="Contraseña débil"
                            mediumLabel="Contraseña aceptable"
                            strongLabel="Contraseña robusta"
                            :class="{'!border !border-red-500': $registerValidator.password.$invalid && $registerValidator.password.$dirty}"
                            @input="$registerValidator.password.$touch()" 
                            aria-describedby="register-password-help"
                            />
                            <small id="register-email-help" v-if="$registerValidator.password.required.$invalid && $registerValidator.password.$dirty" class="text-red-600">Contraseña Requerida</small>
                        </div>
                    </div>

                    <div class="mb-5">
                        <Button :disabled="registerLogin || $registerValidator.username.$invalid || $registerValidator.email.$invalid || $registerValidator.password.$invalid" :loading="registerLogin" type="submit" class="h-12 !bg-sky-700 !border-sky-700 font-medium text-white transition hover:bg-opacity-90" fluid label="Registrarme" />
                    </div>
                </form>
            </div>
        </div>

        <div v-show="currentTab===3" class="px-2">
            <div class="w-full p-2">
                <span class="w-full block font-semibold text-center text-slate-900 text-2xl">Recuperar Acceso</span>
                <span class="w-full block text-center text-green-700 text-base pt-2"><i class="pi pi-lock"></i> Todos tus datos estarán seguros.</span>
                
                <form class="pt-6" @submit.prevent="submitRecover" autocomplete="new-password">
                    <div class="mb-4">
                        <label class="mb-2.5 block font-medium text-black dark:text-white" for="recover-email">Correo Electrónico:</label>
                        <InputText 
                        v-model:model-value="recoverState.email"
                        type="email"  
                        autocomplete="new-password" 
                        class="w-full h-12" 
                        placeholder="Ingresa tu correo electrónico" 
                        id="recover-email" 
                        :class="{'!border !border-red-500': $recoverValidator.email.$invalid && $recoverValidator.email.$dirty}"
                        @input="$recoverValidator.email.$touch()" 
                        aria-describedby="recover-email-help"
                        />
                        <small id="recover-email-help" v-if="$recoverValidator.email.required.$invalid && $recoverValidator.email.$dirty" class="text-red-600">Correo Electrónico requerido.</small>
                        <small id="recover-email-help" v-else-if="$recoverValidator.email.email.$invalid && $recoverValidator.email.$dirty" class="text-red-600">Correo Electrónico inválido.</small>
                    </div>
                        
                    <div class="mb-5">
                        <Button :disabled="recoverLoading || $recoverValidator.email.$invalid" :loading="recoverLoading" type="submit" class="h-12 font-medium text-white transition hover:bg-opacity-90" fluid label="Resetear" />
                    </div>

                    <div class="mt-6 text-center">
                        <p class="font-medium">
                            Ya tienes una cuenta?
                            <span @click="currentTab=1" class="text-sky-700 cursor-pointer">Acceder</span>
                        </p>
                    </div>
                </form>
            </div>
        </div>

        <div class="text-center text-base text-slate-700 px-2 pt-6">
            Al continuar, aceptas nuestros 
            <NuxtLink class="text-sky-500" :to="'/terms'" >Términos de uso</NuxtLink> y
            <NuxtLink class="text-sky-500" :to="'/privacy'" >Política de privacidad</NuxtLink>.
        </div>
    </Dialog>

    <Toast />
</template>


<script lang="ts" setup>
    import {ref, type UnwrapRef} from 'vue';

    import { minLength, required, alphaNum, email } from '@vuelidate/validators';
    import { useListen } from '~/composables/useMitt';
    import { useToast } from "primevue/usetoast";
    import { mdiTagSearch, mdiTruckFastOutline } from '@mdi/js';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import {useAuthStore} from '~/stores/auth.store';
    import type { UserLoginForm, UserRecoverForm, UserRegisterForm } from '~/types/auth';
    import useVuelidate from '@vuelidate/core';
    
    // Meta configuration
    useListen('modal:login-register-client', (message:any) => {
        currentTab.value=0;
        showClientLogin.value=true;
    });

    const toast = useToast();
    const authStore = useAuthStore();

    const registerRules = computed(() => ({
        username: {
            required,
            alphaNum,
            minLength: minLength(5),
        },
        email: {
            required,
            email
        },
        password:{
            required
        }
    }));
    const loginRules = computed(() => ({
        email: {
            required,
            email
        },
        password:{
            required
        }
    }));
    const recoverRules = computed(() => ({
        email: {
            required,
            email
        }
    }));
    /********************* 
    | DATA
    **********************/
    const showClientLogin = ref<boolean>(false);

    //
    const loginLoading=ref<boolean>(false);
    const registerLogin=ref<boolean>(false);
    const recoverLoading=ref<boolean>(false);
    const currentTab=ref<number>(0);

    // Body
    const loginState:UnwrapRef<UserLoginForm> = reactive({
        email: '',
        password: ''
    });
    const registerState:UnwrapRef<UserRegisterForm> = reactive({
        username: '',
        email: '',
        password: '',
        is_provider: false
    });

    const recoverState:UnwrapRef<UserRecoverForm> = reactive({
        email: ''
    });

    const $recoverValidator=useVuelidate(recoverRules, recoverState);
    const $registerValidator = useVuelidate(registerRules, registerState );
    const $loginValidator=useVuelidate(loginRules, loginState);

    /********************* 
    | METHODS
    **********************/
    const previusTab = ()=>{
        if (currentTab.value !== 0){
            currentTab.value-=1;
        }
    };
    const nextTab=()=>{
        currentTab.value=1;
        loginState.email=registerState.email;
        recoverState.email=registerState.email;
    };

    const submitLogin=async()=>{
        const isValid = await $loginValidator.value.$validate();
        if(isValid){
            loginLoading.value=true;
            await authStore.login(loginState).then(() => {
                loginLoading.value=false;
                toast.add({ severity: 'success', summary: 'Éxito', detail: 'Iniciando Sesión!', life:1500 });
                showClientLogin.value=false;

                loginState.email='';
                loginState.password='';
                registerState.email='';
                $loginValidator.value.$reset();
            }).catch(error =>{
                if (error.detail){
                    error=error.detail;
                }
                toast.add({ severity: 'error', summary: 'Error', detail: JSON.stringify(error), life: 6000 });;
                loginLoading.value=false;
            });
        }
    };
    const submitRegister = async()=>{
        const isValid = await $registerValidator.value.$validate();
        if(isValid){
            registerLogin.value=true;

            await fetchWrapper.post('/auth2/users/', registerState, {credentials: 'include'}).then(() => {
                registerLogin.value=false;
                toast.add({ severity: 'success', summary: 'Éxito', detail: '¡Registro exitoso! Por favor revise su correo electrónico para ver el enlace de activación. En caso no se muestre el mensaje, revisar la bandeja de SPAN.', life:8000 });
                
                registerState.email='';
                registerState.password='';
                registerState.username='';
                $registerValidator.value.$reset();
                
                showClientLogin.value=false;
            }).catch(error =>{
                if (error.detail){
                    error=error.detail;
                }else if (error.username){
                    error=error.username[0];
                }else if (error.password){
                    error=error.password[0];
                }else if (error.email){
                    error=error.email[0];
                }

                toast.add({ severity: 'error', summary: 'Error', detail: JSON.stringify(error), life:5000 });
                registerLogin.value=false;
            });
        }
    };
    const submitRecover = async()=>{
        const isValid = await $recoverValidator.value.$validate();
        if(isValid){
            recoverLoading.value=true;
            await fetchWrapper.post('/auth2/users/reset_password/', {email: recoverState.email}).then(() => {
                recoverLoading.value=false;
                toast.add({ severity: 'success', summary: 'Éxito', detail: 'Se a enviado un correo con el enlace de recuperación a '+recoverState.email+'!', life:5000 });
                
                recoverState.email='';
                $recoverValidator.value.$reset();
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
