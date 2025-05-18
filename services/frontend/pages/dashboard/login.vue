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
                    <span class="mb-1 text-zinc-800 hidden md:block">{{ slogan }}</span>
                    <h2 class="mb-4 text-2xl font-bold text-black dark:text-white sm:text-title-xl2">
                        {{ title }}
                    </h2>

                    <p class="text-zinc-800 text-sm pb-6 2xl:px-20 block md:hidden">
                        Estimado usuario, tenga en cuenta que necesita realizar un pago mensual para poder usar este servicio.
                    </p>

                    <form @submit.prevent="submitLogin" v-show="showLogin" autocomplete="new-password">
                        <div class="mb-4">
                            <label class="mb-2.5 block font-medium text-black dark:text-white" for="email">Correo Electrónico:</label>
                            <InputText 
                            v-model:model-value="loginState.email"
                            type="email"  
                            autocomplete="new-password" 
                            class="w-full h-14" 
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
                            class="h-14" 
                            fluid 
                            placeholder="Ingresa tu contraseña" 
                            id="login-password" 
                            :class="{'!border !border-red-500': $loginValidator.password.$invalid && $loginValidator.password.$dirty}"
                            @input="$loginValidator.password.$touch()" 
                            aria-describedby="login-password-help"
                            />
                            <small id="login-password-help" v-if="$loginValidator.password.required.$invalid && $loginValidator.password.$dirty" class="text-red-600">Contraseña requerida.</small>
                        </div>

                        <div class="mb-5">
                            <Button :disabled="loginLoading || $loginValidator.email.$invalid || $loginValidator.password.$invalid" :loading="loginLoading" type="submit" class="h-14 font-medium text-white transition hover:bg-opacity-90" fluid label="Ingresar" />
                        </div>

                        <div class="mt-6 text-center">
                            <p class="font-medium">
                                A&uacute;n no tienes una cuenta?
                                <span @click="toggleForm" class="text-blue-500 cursor-pointer">Crear una</span>
                            </p>

                            <p class="font-medium text-blue-500 cursor-pointer mt-10">
                                <nuxt-link to='/auth/reset-password'>¿Olvidaste tu contraseña?</nuxt-link>
                            </p>
                        </div>
                    </form>

                    <form @submit.prevent="submitRegister" v-show="!showLogin" autocomplete="new-password">
                        <div class="mb-4">
                            <label class="mb-2.5 block font-medium text-black dark:text-white" for="username">Nombre de Usuario:</label>
                            <InputText 
                            v-model:model-value="registerState.username"
                            autocomplete="new-password" 
                            class="h-14" 
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
                            class="h-14" 
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
                                class="h-14" 
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
                                <small id="register-password-help" v-if="$registerValidator.password.required.$invalid && $registerValidator.password.$dirty" class="text-red-600">Contraseña Requerida</small>
                            </div>
                        </div>

                        <div class="mb-5">
                            <Button :disabled="registerLogin || $registerValidator.username.$invalid || $registerValidator.email.$invalid || $registerValidator.password.$invalid" :loading="registerLogin" type="submit" class="h-14 font-medium text-white transition hover:bg-opacity-90" fluid label="Crear Cuenta" />
                        </div>

                        <div class="mt-6 text-center">
                            <p class="font-medium">
                            Ya tienes una cuenta?
                            <span @click="toggleForm" class="text-blue-500 cursor-pointer">Ingresar</span>
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
    import { required, minLength, email, alphaNum } from '@vuelidate/validators'
    import { useToast } from "primevue/usetoast";

    import type { UserLoginForm, UserRegisterForm } from '~/types/auth';
    import {useAuthStore} from '~/stores/auth.store';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';

    // Meta configuration
    definePageMeta({
        'layout': 'empty'
    });

    const toast = useToast();
    const route = useRoute();
    const router=useRouter();
    const authStore = useAuthStore();
    const {user} = storeToRefs(authStore);

    const registerRules = computed(() => ({
        username: {
            required,
            alphaNum,
            minLength: minLength(5),
        },
        email: {
            required,
            email,
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

    // Redirect to home if already logged in
    if (user.value?.username && user.value?.is_superuser) {
        router.push('/dashboard');
    }
    /********************* 
    | DATA
    **********************/
    const showLogin = ref<boolean>(true);
    const slogan = ref<string>('¡Empieza ahora!');
    const title = ref<string>('Inicia Sesión');

    //
    const loginLoading=ref<boolean>(false);
    const registerLogin=ref<boolean>(false);

    // Body
    const loginState:UnwrapRef<UserLoginForm> = reactive({
        email: '',
        password: ''
    });
    const registerState:UnwrapRef<UserRegisterForm> = reactive({
        username: '',
        email: '',
        password: '',
        is_provider: true
    });
    const $registerValidator = useVuelidate(registerRules, registerState );
    const $loginValidator=useVuelidate(loginRules, loginState);

    /********************* 
    | METHODS
    **********************/
    const toggleForm = ()=>{
        showLogin.value = !showLogin.value;
        slogan.value=showLogin.value? '¡Empieza ahora!':'¡Todo empieza con un click!';
        title.value=showLogin.value?'Inicia Sesión':'Crea una cuenta';
    };

    //
    const submitLogin = async()=>{
        const isValid = await $loginValidator.value.$validate();
        if(isValid){
            loginLoading.value=true;
            await authStore.login(loginState).then(() => {
                loginLoading.value=false;
                toast.add({ severity: 'success', summary: 'Éxito', detail: 'Iniciando Sesión!', life:1500 });
                
                // Redirect to previous url or default to home page
                setTimeout(()=>{
                    const returnUrl=route.query.returnUrl === undefined ? '/dashboard' : new String(route.query.returnUrl).valueOf();
                    router.push(returnUrl);
                }, 1600);
            }).catch(error =>{
                if (error.detail){
                    error=error.detail;
                }
                toast.add({ severity: 'error', summary: 'Error', detail: JSON.stringify(error), life: 6000 });
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
                toast.add({ severity: 'success', summary: 'Éxito', detail: '¡Registro exitoso! Por favor revise su correo electrónico para ver el enlace de activación.', life:6000 });
                
                setTimeout(() => {
                    registerState.email='';
                    registerState.password='';
                    registerState.username='';

                    $registerValidator.value.$reset();
                }, 2000);
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

                toast.add({ severity: 'error', summary: 'Error', detail: JSON.stringify(error), life:6000 });
                registerLogin.value=false;
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