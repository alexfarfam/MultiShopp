
<template>
    <div class="flex items-center justify-center !min-h-screen bg-gray-100">
        <div v-show="active" class="bg-white p-10 rounded-lg shadow-lg max-w-lg">
            <div class="text-center">
                <i class="pi pi-check-circle !text-green-500 !text-5xl mb-4"></i>
                <h2 class="text-2xl font-semibold text-gray-800 mb-2">¡Cuenta registrada con éxito!</h2>
                <p class="text-gray-600 mb-6">Gracias por registrarte. Ahora puedes iniciar sesión con tu nueva cuenta.</p>
                
                <nuxt-link :to="user?.is_provider? '/dashboard/login':'/'">
                    <Button label="Iniciar sesión" class="w-full p-button p-button-success" />
                </nuxt-link>
            </div>
        </div>

        <div v-show="!active" class="bg-white p-10 rounded-lg shadow-lg max-w-lg">
            <div class="text-center">
                <i class="pi pi pi-times-circle !text-red-500 !text-5xl mb-4"></i>
                <h2 class="text-2xl font-semibold text-gray-800 mb-2">¡Error!</h2>
                <p class="text-gray-600 mb-6">Ha ocurrido un problema al registrar tu cuenta. Por favor, inténtalo nuevamente más tarde.</p>
                
                <nuxt-link :to="user?.is_provider? '/dashboard/login':'/'">
                    <Button label="Volver a intentar" class="w-full p-button p-button-danger" />
                </nuxt-link>
            </div>
        </div>
    </div>

</template>

<script lang="ts" setup>
    import {ref} from 'vue';
    import { fetchWrapper } from '~/helpers/fetch-wrapper'
    import type { User } from '~/types/auth';
    
    // Meta configuration
    definePageMeta({
        'layout': 'empty'
    });

    /********************* 
    | DATA
    **********************/
    const router = useRouter();
    const route = useRoute();
    const active = ref<boolean>(false);
    const user = ref<User>();
    
    /********************* 
    | METHODS
    **********************/

    /********************* 
    | MOUNT
    **********************/
    onMounted(async () => {
        const { uid, token } = route.query;
        if (!uid || !token){
            router.push('/');
        };

        try {
            await fetchWrapper.post('/auth2/users/activation/', { uid, token });

            active.value = true;
        } catch (error) {
            active.value=false;
        }
    });

</script>