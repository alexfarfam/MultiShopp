<template>
    <div class="flex flex-col">
        <header id="header" class="bg-[#191919] pt-3 top-0 left-0 w-full">
            <div class="mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex flex-wrap lg:gap-8 md:gap-4 sm:gap-3 flex-row py-2">
                <i @click="showCategoryDrawer=true" class="block md:!hidden my-4 mx-2 cursor-pointer pi pi-bars text-white text-2xl font-medium"></i>
                <div class="relative top-[-0.1rem] basis-[24%] md:basis-1/12">
                    <NuxtLink to="/">
                        <img class="!h-12 md:!h-20 !w-60 md:!w-40" :src="companyDataForm?.logo" alt="Logo">
                    </NuxtLink>
                </div>

                <div class="flex flex-col order-last md:order-none basis-full md:basis-7/12 my-2">
                    <AutoComplete
                    v-model:model-value="globalFilterProduct"
                    @complete="globalSearchProduct"
                    option-label="title"
                    :suggestions="filteredProductOptions"
                    class="flex flex-row"
                    :pt="{
                        pcInput: { 
                            root: { 
                                class: 'flex-1 !w-full !rounded-3xl !p-4 h-8 md:!h-10 !text-sm !placeholder-gray-400 !tracking-wide' 
                            } 
                        } 
                    }"
                    placeholder="Buscar Producto/Servicio"
                    >
                        <template #dropdown>
                            <div class="absolute right-1 md:right-2 bg-[#191919] h-7 w-16 rounded-2xl text-center top-1 pt-1">
                                <i class="pi pi-search !text-lg text-slate-200"></i>
                            </div>
                        </template>
                        
                        <template #empty>
                            <span class="mt-4 block !text-2xl text-gray-400/[0.8] pi pi-folder-open w-full text-center"></span>
                            <span class="mt-2 mb-4 block text-lg text-gray-400/[0.8] w-full text-center">Sin productos para mostrar</span>
                        </template>

                        <template #option="slotProps">
                            <nuxt-link class="flex flex-col w-full" :to="(slotProps.option.price?'/store/products/':'/store/services/')+slotProps.option.id">
                                <div class="flex flex-row items-center p-2 md:p-6 gap-4 shadow-md bg-white my-2">
                                    <div class="w-24 md:w-28 relative">
                                        <img class="block mx-auto rounded w-full" :src="slotProps.option.main_image" :alt="slotProps.option.title" />
                                        <span v-if="slotProps.option.discount > 0" class="absolute top-0 left-0 rounded-md px-2 py-1 bg-[#D4AF37] text-white text-xs">
                                            {{slotProps.option.discount}}% descuento
                                        </span>
                                    </div>
                                    <div class="flex-1 flex flex-col md:flex-row justify-between items-center gap-6">
                                        <div class="basis-[80%] flex flex-col gap-2">
                                            <div class="hidden md:flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">{{ slotProps.option.subcategory__title }}</span>
                                                <div class="flex items-end gap-2 justify-end px-2">
                                                    <Rating v-model="slotProps.option.qualification" readonly/>
                                                    <span class="text-surface-900 top-[0.2rem] relative font-medium text-sm">{{ slotProps.option.qualification }}</span>
                                                </div>
                                            </div>

                                            <div>
                                                <div class="text-lg flex flex-col md:flex-row truncate w-[13rem] md:w-96 mt-1">
                                                    <span v-if="slotProps.option.header_tag" class="w-fit hidden md:block rounded-md px-2 py-1 bg-[#D4AF37] text-white text-xs mr-1">
                                                        {{ slotProps.option.header_tag }}
                                                    </span>
                                                    {{ slotProps.option.title}}
                                                </div>
                                            </div>
                                        </div>

                                        <div v-if="slotProps.option.price" class="flex-1 flex flex-col md:items-end gap-8">
                                            <div class="flex gap-5">
                                                <span class="text-[#D4AF37] flex-auto text-2xl font-semibold">{{Globalization.currencyFormat.format(slotProps.option.price)}}</span>
                                            <span class="flex-auto pt-[0.2rem] text-lg font-normal text-slate-500 line-through">{{ Globalization.currencyFormat.format(slotProps.option.reference_price) }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </nuxt-link>
                        </template>
                    </AutoComplete>
                </div>

                <div @click="showUserPopover" :class="isMobile ? (user?.username ? '':'ml-[6.3rem]'):''" class="cursor-pointer flex flex-row gap-1 basis-1/12 pt-2">
                    <span class="ml-5 text-white block md:hidden">{{ user?.username ? `Hola, ${user?.username}!` : '' }}</span>
                    <i :class="isMobile ? 'ml-5':''"  class="pi pi-user text-slate-200 !text-2xl md:!text-xl mx-2 md:mx-0"></i>
                    <Popover  ref="refUserPopover">
                        <div class="flex flex-col gap-1 w-60">
                            <Button @click="openLoginRegisterClientModal" class="w-full h-9">
                                {{user?.username ? 'Cerrar Sesión':'Logearse'}}
                            </Button>
                            <div class="hidden border-b pb-3 border-b-slate-300/[0.7] text-center text-zinc-600 tracking-wider text-sm/[12px]">
                                <span class="block mt-2" v-show="!user?.username">Registrarse</span>
                            </div>

                            <div v-show="!user?.username" class="text-zinc-500 text-sm text-justify">
                                Inicia sesión para tener un registro de pedidos y muchos beneficios más!
                            </div>

                            <div v-show="user?.username" class="pt-2">
                                <div @click="doSeeOrders" class="py-2 px-3 hover:cursor-pointer hover:bg-slate-200/[0.5]">
                                    <i class="text-lg pi pi-truck"></i>
                                    <span class="ml-2">Ver mis pedidos</span>
                                </div>

                                <div @click="doSetupAccount" class="py-2 px-3 hover:cursor-pointer hover:bg-slate-200/[0.5]">
                                    <i class="pi pi-cog"></i>
                                    <span class="ml-2">Configurar mi cuenta</span>
                                </div>
                            </div>
                        </div>
                    </Popover>

                    <span class="hidden md:!block text-slate-200 text-sm/[0.9]">
                        {{ user?.username ? `Hola, ${user?.username}! Bienvenido(a)` : 'Inicia Sesión/Registrate' }}
                    </span>
                </div>

                <div @click="showProviderPopover" class="cursor-pointer flex flex-row gap-1 basis-1/12 pt-2">
                   <i class="pi pi-truck text-slate-200 !text-2xl md:!text-xl pt-1 mx-2 md:mx-0"></i>
                    <span class="hidden md:!block text-slate-200 text-sm/[0.9]">Acceso a Proveedores</span>
                    <Popover ref="refProviderPopover">
                        <div class="flex flex-col gap-2 w-60">
                            <div>
                                <Button @click="openProviderLogin" class="w-full h-9">Portal de Proveedores</Button>
                            </div>

                            <div class="border-b pt-2 pb-3 border-b-slate-300/[0.7] text-center text-zinc-600 tracking-wider text-sm/[12px]">
                                <span>¿No tienes cuenta? Únete a nuestra red de proveedores.</span>
                            </div>

                            <div class="text-zinc-500 text-sm text-left">
                                Accede a tus órdenes, gestiona tus productos y colabora en nuestro marketplace.
                            </div>
                        </div>
                    </Popover>
                </div>
            </div>
            </div>
        </header>
        
        <header v-if="!isMobile" id="header2" class="bg-[#191919] top-0 left-0 w-full">
            <div class="mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex flex-wrap gap-1 flex-row py-3">
                    <div class="basis-4/12 md:basis-1/12"></div>

                    <div class="grow">
                        <nav class="hidden md:flex space-x-5 float-left gap-1">
                            <NuxtLink to="/store/collections/best-sellers" class="cursor-pointer px-3 py-1 rounded text-[#dee4ee] hover:bg-slate-300/[0.3] duration-150 transition-colors p-ripple" v-ripple>
                                Más Vendidos
                            </NuxtLink>

                            <NuxtLink to="/store/collections/discounts" class="cursor-pointer px-3 py-1 rounded text-[#dee4ee] hover:bg-slate-300/[0.3] duration-150 transition-colors p-ripple" v-ripple>
                                Descuentos
                            </NuxtLink>

                            <NuxtLink to="/store/collections/newcomers" class="cursor-pointer px-3 py-1 rounded text-[#dee4ee] hover:bg-slate-300/[0.3] duration-150 transition-colors p-ripple" v-ripple>
                                Reci&eacute;n Llegados
                            </NuxtLink>

                            <NuxtLink to="/store/collections/promotions" class="cursor-pointer px-3 py-1 rounded text-[#dee4ee] hover:bg-slate-300/[0.3] duration-150 transition-colors p-ripple" v-ripple>
                                Promociones
                            </NuxtLink>

                            <div @mouseenter="showMainCategoriesPopover" class="space-x-2 cursor-pointer px-3 py-1 rounded text-[#dee4ee] bg-slate-300/[0.3]">
                                <i style="position: relative;" class="pi pi-list"></i>
                                <span>Todas las categor&iacute;as</span>
                                <i style="position: relative;" class="top-1 pi pi-chevron-down"></i>
                            </div>

                            <Popover @mouseleave="hideMainCategoriesPopover" ref="refMainCategoriesPopover">
                                <div class="flex flex-row gap-2 !w-[720px] h-96">
                                    <div class="basis-[28%]">
                                        <Listbox 
                                        :options="categoriesData" 
                                        optionLabel="title" 
                                        class="!border-0 w-full h-full"
                                        :highlightOnSelect="false"
                                        >
                                            <template #empty>
                                                <span class="flex justify-center text-center mt-[90%] items-center text-sm text-slate-400">
                                                    Sin Categorias para mostrar
                                                </span>
                                            </template>
                                            <template #option="slotProps">
                                                <div @click="router.push('/store/collections/'+slotProps.option.id)" class="flex basis-full" @mouseenter="updateMainCategory(slotProps.index)">
                                                    <div class="basis-11/12 !capitalize">{{ slotProps.option.title }}</div>
                                                    <i class="basis-1/12 pi pi-angle-right"></i>
                                                </div>
                                            </template>
                                        </Listbox>
                                    </div>

                                    <div class="basis-[72%]">
                                        <div class="p-1 flex justify-start absolute bg-white w-[-webkit-fill-available]">
                                            Todos {{ currentMainCategorieName }}
                                        </div>
                                        <DataView class="mt-14 h-[-webkit-fill-available] overflow-y-auto" :value="subcategoriesData" layout="grid" data-key="id">
                                            <template #empty>
                                                <span class="mt-[15%] flex justify-center text-center items-center text-lg text-slate-400">
                                                    Sin Subcategorias para mostrar
                                                </span>
                                            </template>
                                            <template #grid="slotProps">
                                                <div class="grid grid-cols-5 gap-2">
                                                    <nuxt-link
                                                    v-for="(item, index) in slotProps.items" 
                                                    :to="'/store/collections/category/'+item.id"
                                                    :key="index" 
                                                    class="cursor-pointer col-span-1 m-3 flex flex-col align-middle"
                                                    >
                                                        <Avatar :image="item.image" class="mr-2 !w-20 !h-20" shape="circle" />
                                                        <div class="text-sm font-normal mt-2 text-center">{{ item.title }}</div>
                                                    </nuxt-link>
                                                </div>
                                            </template>
                                        </DataView>
                                    </div>
                                </div>
                            </Popover>

                        </nav>
                    </div>
                </div>
            </div>
        </header>
    </div>

    <div class="w-full bg-gradient-to-r from-slate-100 to-slate-200 p-2 md:p-10">
        <slot/>
    </div>

    <footer>
        <div class="bg-[#0B0B0B] text-white/[0.9] flex flex-col p-4 gap-2">
            <div class="flex flex-col md:flex-row gap-10 px-5 md:px-10 pt-10">
                <div class="md:m-auto basis-1/4">
                    <span class="uppercase ml-3 font-bold text-lg">{{companyDataForm?.company_name}}</span>

                    <div class="mt-4 ml-3 text-sm">
                        ¡Bienvenido a nuestra plataforma de ecommerce para emprendedores! Aquí, te ofrecemos la oportunidad de vender tus productos o servicios de manera sencilla y accesible. Publica tus artículos, conecta con más clientes y haz crecer tu negocio sin complicaciones. 
                    </div>

                    <div class="mt-4 ml-4 w-64 flex flex-row gap-8">
                        <a :href="companyDataForm?.url_facebook" class="w-9 h-8 text-center bg-[#2e7eed] rounded-full text-sm">
                            <i class="pi pi-facebook !text-xl mt-0"></i> 
                        </a>
                        <a :href="companyDataForm?.url_instagram" class="w-9 h-8 text-center bg-[#2e7eed] rounded-full text-sm">
                            <i class="pi pi-instagram !text-xl mt-0"></i> 
                        </a>
                        <a :href="'mailto:'+companyDataForm?.customer_service_email" class="w-9 h-8 text-center bg-[#2e7eed] rounded-full text-sm">
                            <i class="pi pi-envelope !text-lg mt-0"></i>
                        </a>
                        <a :href="'tel:' + companyDataForm?.customer_service_telephone" class="w-9 h-8 text-center bg-[#2e7eed] rounded-full text-sm">
                            <i class="pi pi-phone !text-lg mt-0"></i>
                        </a>
                    </div>
                </div>

                <div class="md:m-auto basis-1/4">
                    <span class="uppercase text-sm ml-3 font-bold">Información</span>
                    <ul class="mt-2">
                        <li class="p-2">
                            <nuxt-link to="/about" class="text-sm">
                                Acerca de
                            </nuxt-link> 
                        </li>
                        <li class="p-2">
                            <nuxt-link to="/company" class=" text-sm">
                                Nuestra compañia
                            </nuxt-link> 
                        </li>
                        <li class="p-2">
                            <nuxt-link to="/history" class="text-sm">
                                Nuestra historia
                            </nuxt-link> 
                        </li>
                    </ul>
                </div>

                <div class="md:m-auto basis-1/4">
                    <span class="uppercase text-sm ml-3 font-bold">¿Cómo podemos ayudarte?</span>
                    <ul class="mt-2">
                        <li class="p-2">
                            <nuxt-link to="/workflow" class="text-sm">
                                ¿Cómo trabajamos?
                            </nuxt-link> 
                        </li>
                        <li class="p-2">
                            <nuxt-link to="/faqs" class="text-sm">
                                FAQ
                            </nuxt-link> 
                        </li>
                        <li class="p-2">
                            <nuxt-link to="/support" class="text-sm">
                                Soporte
                            </nuxt-link> 
                        </li>
                    </ul>
                </div>

                <div class="md:m-auto basis-1/4">
                    <span class="uppercase text-sm ml-3 font-bold">Suscríbete</span>
                   <form @submit.prevent="doSub">
                        <ul class="mt-2">
                            <li class="p-2">
                                <InputText 
                                size="small"
                                v-model:model-value="subState.email"
                                type="email"  
                                autocomplete="new-password" 
                                class="w-full" 
                                placeholder="Ingresa tu correo electrónico" 
                                id="sub-email" 
                                :class="{'!border !border-red-500': $subValidator.email.$invalid && $subValidator.email.$dirty}"
                                @input="$subValidator.email.$touch()" 
                                aria-describedby="sub-email-help"
                                />
                                <small id="sub-email-help" v-if="$subValidator.email.email.$invalid && $subValidator.email.$dirty" class="text-red-600">Correo Electrónico inválido.</small>
                            </li>
                            <li class="p-2">
                                <Button type="submit" :disabled="subLoading || $subValidator.email$invalid || subState.email.trim() === '' " :loading="subLoading" class="!bg-[#2e7eed] w-full" size="small">Suscribirse</Button>
                            </li>
                        </ul>
                   </form>
                </div>
            </div>

            <span class="text-xs text-center pt-7 pb-1">
                Precios y condiciones de pago exclusivos para compras en esta web oficial, que pueden variar con el tiempo de la oferta. En caso de que compre los mismos productos en otras tiendas, no nos hacemos responsables de ningún problema.
            </span>
        </div>

        <div class="bg-black text-white/[0.8] p-4 flex flex-col md:flex-row sm:flex-row gap-2">
            <span class="flex-auto text-sm text-center sm:text-left md:text-left">
                &copy;{{ new Date().getFullYear() }} {{companyDataForm?.company_name}} - Todos los derechos reservados. Powered by 
                <a class="!text-slate-300" href="bussinessInfo.developer_url" target="_blank" rel="noopener noreferrer">
                    Al3x D3v
                </a>
            </span>

            <div class="flex flex-col sm:flex-row lg:flex-row flex-auto gap-2">
                <span class="md:flex-auto text-sm text-center sm:text-right md:text-right">
                    <nuxt-link to="/privacy-policy">Políticas de privacidad y uso de datos</nuxt-link>
                </span>

                <span class="md:flex-auto text-sm text-center sm:text-right md:text-right mr-10">
                    <nuxt-link to="/terms-condition">Términos y Condiciones</nuxt-link>
                </span>
            </div>
        </div>
    </footer>

    <LoginRegisterClientModal/>
    <Toast />

    <Drawer id="category-drawer" v-if="isMobile" v-model:visible="showCategoryDrawer" header="Todas las Categorías" position="full">
        <div class="flex flex-row gap-1 w-full h-full">
            <div class="basis-[28%]">
                <Listbox 
                :options="categoriesData" 
                optionLabel="title" 
                class="!border-0 w-full h-full"
                :highlightOnSelect="false"
                >
                    <template #empty>
                        <span class="flex justify-center text-center mt-[90%] items-center text-sm text-slate-400">
                            Sin Categorias para mostrar
                        </span>
                    </template>
                    
                    <template #option="slotProps">
                        <div @click="router.push('/store/collections/'+slotProps.option.id)" class="flex basis-full" @mouseenter="updateMainCategory(slotProps.index)">
                            <div class="basis-11/12 !text-xs">{{ slotProps.option.title }}</div>
                            <i class="basis-1/12 pi pi-angle-right"></i>
                        </div>
                    </template>
                </Listbox>
            </div>

            <div class="basis-[72%]">
                <div class="p-1 flex justify-start absolute bg-white w-[-webkit-fill-available]">
                    Todos {{ currentMainCategorieName }}
                </div>
                
                <DataView class="mt-14 h-[-webkit-fill-available] overflow-y-auto" :value="subcategoriesData" layout="grid" data-key="id">
                    <template #empty>
                        <span class="mt-[15%] flex justify-center text-center items-center text-lg text-slate-400">
                            Sin Subcategorias para mostrar
                        </span>
                    </template>
                    
                    <template #grid="slotProps">
                        <div class="grid grid-cols-2 gap-1">
                            <nuxt-link
                            v-for="(item, index) in slotProps.items" 
                            :to="'/store/collections/category/'+item.id"
                            :key="index" 
                            class="cursor-pointer col-span-1 m-2 flex flex-col align-middle"
                            >
                                <Avatar :image="item.image" class="!w-20 !h-20" shape="circle" />
                                <div class="text-sm font-normal mt-2 text-center">{{ item.title }}</div>
                            </nuxt-link>
                        </div>
                    </template>
                </DataView>
            </div>
        </div>
    </Drawer>

    <ScrollTop />

    <!-- Overlay -->
    <div @click="hiddenOverlay" v-show="showOverlay" class="bg-black/[0.5] fixed z-[999] top-0 left-0 w-screen h-screen" >
    </div>
</template>

<script lang="ts" setup>
    import {ref, type UnwrapRef} from 'vue';
    import { useMediaQuery } from '@vueuse/core';

    import { useToast } from "primevue/usetoast";
    import useVuelidate from '@vuelidate/core';
    import { Globalization } from '~/helpers/globalization';
    import type { ItemListbox } from '~/types';
    import type { CompanyForm } from '~/types/dashboard/profile/company-data';
    import type{UserSubForm} from '~/types/auth';
    import type { ProductItem } from '~/types/dashboard/products';
    import {useAuthStore} from '~/stores/auth.store';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import { email } from '@vuelidate/validators';

    // Meta configuration
    const router=useRouter();
    const authStore = useAuthStore();
    const {user} = storeToRefs(authStore);
    
    const subRules = computed(() => ({
        email: {
            email
        }
    }));

    const toast = useToast();

    /********************* 
    | DATA
    **********************/
    const refUserPopover = ref();
    const refProviderPopover = ref();
    const refMainCategoriesPopover = ref();
    const showOverlay = ref<boolean>(false);

    //
    const isMobile = useMediaQuery('(max-width: 600px)');
    const categoriesData = ref<Array<ItemListbox>>([]);
    const subcategoriesData = ref<any[]>([]);
    const currentMainCategorieIndex=ref<number>(-1);
    const currentMainCategorieName=ref<string>('');
    const companyDataForm=ref<CompanyForm>();

    const globalFilterProduct=ref<string>('');
    const filteredProductOptions = ref<ProductItem[]>([]);
    const productOptions = ref<ProductItem[]>([]);

    //
    const subState:UnwrapRef<UserSubForm> = reactive({
        email: ''
    });
    const $subValidator=useVuelidate(subRules, subState);
    const subLoading=ref<boolean>(false);
    const showCategoryDrawer = ref<boolean>(false);

    /********************* 
    | METHODS
    **********************/
    const hiddenOverlay = ()=>{
        showOverlay.value=false;
    };
    const globalSearchProduct = () => {
        filteredProductOptions.value=productOptions.value.filter(entry=>{
            const value=globalFilterProduct.value.toLowerCase();
            return (
                entry.title.toLowerCase().includes(value) || entry.header_tag.toLowerCase().includes(value) ||
                (entry.discount?entry.discount.toString().includes(value):false) || (entry.price?(Globalization.currencyFormat.format(entry.price)).toString().includes(value):false) ||
                (entry.reference_price?(Globalization.currencyFormat.format(entry.reference_price)).toString().includes(value):false)
            );
        });
        showOverlay.value=true;
    };

    const showUserPopover = (event:MouseEvent) => {
        refUserPopover.value.toggle(event);
        showOverlay.value=true;
    }
    const hideUserPopover = (event:MouseEvent) => {
        showOverlay.value=false;
        refUserPopover.value.toggle(event);
    }

    const showProviderPopover = (event:MouseEvent) => {
        refProviderPopover.value.toggle(event);
        showOverlay.value=true;
    }

    const showMainCategoriesPopover = (event:MouseEvent) => {
        refUserPopover.value.hide(event);
        refProviderPopover.value.hide(event);
        if (refMainCategoriesPopover.value)
            refMainCategoriesPopover.value.show(event);
        showOverlay.value=true;
    }
    const hideMainCategoriesPopover = (event:MouseEvent) => {
        if (refMainCategoriesPopover.value)
            refMainCategoriesPopover.value.hide(event);
        showOverlay.value=false;
    }

    //
    const doSeeOrders = ()=>{
        router.push('/store/orders/');
    };
    const doSetupAccount = ()=>{
        router.push('/store/config/');
    };
    
    //
    const updateMainCategory = async(index:number)=>{
        const item = categoriesData.value[index];
        currentMainCategorieIndex.value=index;
        currentMainCategorieName.value=item.title;
        const params=new URLSearchParams();
        params.append('category_id', item.id.toString());
        subcategoriesData.value = await fetchWrapper.get('/subcategories/public?'+params);
    };

    //
    const openProviderLogin = ()=>{
        router.push('/dashboard/login');
    };
    const openLoginRegisterClientModal= async(event:any)=>{
        hideUserPopover(event);
        if (user.value?.username){
            await authStore.logout();
        }else{
            sendEvent('modal:login-register-client', {severity: 'normal', message: ''});
        }
    };

    const doSub=async()=>{
        const isValid = true; //await $subValidator.value.$validate();
        if(isValid){
            subLoading.value=true;
            await fetchWrapper.post('/globals/sub', subState).then((msg) => {
                subLoading.value=false;
                toast.add({ severity: 'success', summary: 'Éxito', detail: msg, life:1500 });
                subState.email='';
                $subValidator.value.$reset();
            }).catch(error =>{
                if (error.detail){
                    error=error.detail;
                }
                toast.add({ severity: 'error', summary: 'Error', detail: JSON.stringify(error), life: 6000 });;
                subLoading.value=false;
            });
        }
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(async() => {
        companyDataForm.value = await fetchWrapper.get('/company-data/info');
        categoriesData.value = await fetchWrapper.get('/categories/public');
        productOptions.value=await fetchWrapper.get('/services/public');
        //productOptions.value=productOptions.value.concat(await fetchWrapper.get('/services/public'));
        filteredProductOptions.value=productOptions.value;
    });
</script>

<style>
    #header input{
        width: 100%!important;
    }
    #category-drawer .p-drawer-content{
        padding: 0px;
    }
    .p-autocomplete-overlay {
        max-height: 40rem!important;
    }
</style>