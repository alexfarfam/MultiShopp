<template>
    <div class="flex flex-nowrap flex-row h-screen">
        <Drawer 
        v-model:visible="navbarVisible"
        :modal="!isLargeScreen" 
        position="left" 
        :dismissable="!isLargeScreen"
        class="!bg-slate-950/[0.9] !w-auto !border-transparent fixed top-0 right-0 h-full"
        :pt="{
            mask: {
                class: 'lg:!w-fit lg:!basis-1/6'
            }
        }"
        >
            <template #container>
                <div class="flex flex-col h-full">
                    <div class="flex items-center justify-between px-6 pt-4 shrink-0">
                        <span class="inline-flex items-center gap-2">
                            <Avatar :image="companyLogo" size="large" shape="circle" />
                            <span class="ml-2 mt-2 font-semibold text-2xl text-white">{{ companyName }}</span>
                        </span>
                    </div>

                    <div class="mt-8 pl-3 overflow-y-auto">
                        <li class="px-4 m-0" @click="doToogleNavbar">
                            <nuxt-link 
                            to="/dashboard" 
                            v-ripple 
                            class="flex items-center cursor-pointer px-4 py-3 rounded text-[#dee4ee] focus:bg-slate-300/[0.1] hover:bg-slate-300/[0.1] dark:text-surface-0 dark:hover:bg-surface-800 duration-150 transition-colors p-ripple"
                            >
                                <i class="pi mr-2 text-lg pi-home"></i>
                                <span class="font-medium">Inicio</span>
                            </nuxt-link>
                        </li>

                        <ul v-for="(item, index) in menu" class="list-none p-4 m-0">
                            <li>
                                <div
                                    v-ripple
                                    v-styleclass="{
                                        selector: '@next',
                                        enterFromClass: 'hidden',
                                        enterActiveClass: 'animate-slidedown',
                                        leaveToClass: 'hidden',
                                        leaveActiveClass: 'animate-slideup'
                                    }"
                                    class="px-4 py-2 flex items-center justify-between text-surface-500 dark:text-surface-400 cursor-pointer p-ripple"
                                    >
                                    <span class="uppercase">{{ item.title }}</span>
                                    <i class="pi pi-chevron-down"></i>
                                </div>

                                <ul class="list-none p-0 m-0 overflow-hidden">
                                    <li @click="doToogleNavbar" v-for="(child, index2) in item.childrens">
                                        <nuxt-link 
                                        :to="child.url" 
                                        v-ripple 
                                        class="flex items-center cursor-pointer px-4 py-3 rounded text-[#dee4ee] focus:bg-slate-300/[0.1] hover:bg-slate-300/[0.1] dark:text-surface-0 dark:hover:bg-surface-800 duration-150 transition-colors p-ripple"
                                        >
                                            <i :class="'pi mr-2 text-lg ' + child.icon"></i>
                                            <span class="font-medium">{{ child.text }}</span>
                                        </nuxt-link>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                        
                    <div class="mt-auto">
                        <hr class="mb-4 mx-4 border-t border-0 border-surface-200 dark:border-surface-700" />
                        <a v-ripple class="m-4 flex items-center cursor-pointer p-4 gap-2 rounded text-surface-700 hover:bg-slate-300/[0.1] dark:text-surface-0 dark:hover:bg-surface-800 duration-150 transition-colors p-ripple">
                            <Avatar :image="userAvatar" size="large" shape="circle" />
                            <span class="font-bold text-white">
                                {{ user?.username }}
                            </span>
                        </a>
                    </div>
                </div>
            </template>
        </Drawer>

        <div :class="mainContainerClass">
            <Toolbar 
            class="!py-1 shadow-lg top-0 w-full" 
            >
                <template #start>
                    <Button @click="navbarVisible = !navbarVisible" icon="pi pi-bars" class="ml-6" severity="contrast" text />
                    <p class="ml-6 tracking-wider text-lg text-gray-900">
                        {{companyName}} Dashboard
                    </p>
                </template>

                <template #end> 
                    <IconField>
                        <InputIcon>
                            <i class="pi pi-search" />
                        </InputIcon>
                        <InputText class="w-28 md:w-full" v-model:model-value="searchForm.search" @keyup="doGlobalSearch" size="small" placeholder="Buscar" />
                    </IconField>

                    <OverlayBadge severity="danger" class="mx-5" :value="notifications.length">
                        <i ref="triggerButton" @click="toggleNotifications" class="cursor-pointer pi pi-bell mt-1 text-2xl/[5px]"/>
                    </OverlayBadge>
                    <Popover class="shadow" ref="notificationsContainerRef" append-to="self">
                        <div class="flex flex-col gap-4 w-[22rem]">
                            <div>
                                <span class="block p-1 pb-2 mb-4 border-b border-b-slate-200/[0.6]">Notificaciones</span>
                                <ul v-if="notifications.length > 0" class="list-none p-0 m-0 flex flex-col gap-4">
                                    <li v-for="notification in notifications" :key="notification.id" class="flex items-center gap-2">
                                        <Avatar class="mr-2" icon="pi pi-info" size="normal" shape="circle" />

                                        <div>
                                            <span>{{ notification.title }}</span>
                                            <div class="text-sm text-surface-500 dark:text-surface-400">{{ notification.content }}</div>
                                        </div>
                                        <div class="flex items-center gap-2 text-surface-500 dark:text-surface-400 ml-auto text-sm">
                                            <Button @click="notification.actionEvent" severity="secondary" outlined size="small" :label="notification.actionText" />
                                        </div>
                                    </li>
                                </ul>

                                <div class="text-center py-10 text-lg text-zinc-400/[0.6]" v-else>
                                    Sin notificaciones que mostrar.
                                </div>
                            </div>
                        </div>
                    </Popover>

                    <Divider class="!hidden md:block h-16" layout="vertical" />
                    <SplitButton
                    :model="toolbarMenu" 
                    text
                    @click="showMenu"
                    ref="splitButton"
                    >
                        <span class="flex items-center">
                            <span class="flex flex-col text-right">
                                <span class="text-base/[20px] text-gray-700 capitalize">{{ user?.username }}</span>
                                <span class="text-sm font-thin text-gray-600">{{ user?.profile__name }}</span>
                            </span>
                            <Avatar :image="userAvatar" class="ml-4" size="large" shape="circle" />
                        </span>
                    </SplitButton>
                </template>
            </Toolbar>

            <div 
            class="w-full !overflow-y-scroll bg-gradient-to-r from-slate-100 to-slate-200 px-0 py-4 md:px-12 md:py-8 rounded-lg shadow-md" 
            style="height: 90vh;"
            >
                <div class="w-full flex flex-row mb-10">
                    <span class="flex-auto mx-10 font-medium text-slate-900 text-2xl tracking-wide">{{ getCurrentPage(route.path) }}</span>
                    <Button @click="doAddNew" v-if="excludePaths.indexOf(route.path) === -1" class="!bg-[#10B981] !border-[#10B981] flex-none w-36 mr-4 md:mr-0" icon="pi pi-plus" label="Agregar"/>
                </div>

                <div class="mt-5">
                    <slot/>
                </div>
            </div>
        </div>
    </div>

</template>

<script lang="ts" setup>
    import { ref, type UnwrapRef} from 'vue';

    import { sendEvent } from '~/composables/useMitt';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import type { CompanyForm } from '~/types/dashboard/profile/company-data';
    import { useAuthStore } from '~/stores/auth.store';
    import type { MenuSection, NotificationItem, SearchForm } from '~/types';
    import { useMediaQuery } from '@vueuse/core';

    /********************* 
    | Setup Configuration
    **********************/
    const excludePaths =[
        '/dashboard', '/dashboard/general/payments', '/dashboard/general/clients', '/dashboard/general/reservations',
        '/dashboard/general/comments', '/dashboard/general/providers', '/dashboard/profile/my-payments', 
        '/dashboard/general/orders', '/dashboard/profile/company-data',
        '/dashboard/profile/user-data', '/dashboard/profile/contact-data', '/dashboard/general/extras'
    ];

    const mainContainerClass = computed(() =>
        navbarVisible.value ? 'w-full md:basis-5/6 ml-0 md:ml-auto transition-all duration-300' : 'w-full transition-all duration-300'
    );

    const route = useRoute();
    const router = useRouter();
    const authStore=useAuthStore();
    const {user} = storeToRefs(authStore);
    const isMobile = useMediaQuery('(max-width: 600px)');

    /********************* 
    | Data
    **********************/
    const triggerButton = ref();
    const splitButton = ref();
    const navbarVisible = ref<boolean>(false);
    const isLargeScreen = ref<boolean>(false);
    const toolbarMenu = ref([
        {
            label: 'Perfil',
            icon: 'pi pi-user',
            command: () => {
                router.push('/dashboard/profile/user-data');
            }
        },
        {
            label: 'Salir',
            icon: 'pi pi-power-off',
            command: async()=>{
                await authStore.logout();
                router.push('/dashboard/login');
            }
        }
    ]);

    //
    const companyName = ref<string>('');
    const companyLogo=ref<string>('');
    const companyPhoneNumber=ref<string>('');
    const userAvatar=ref<string>('');
    userAvatar.value=user.value?.logo?user.value.logo:'/avatar.png';

    const menu = ref<MenuSection[]>([
        {
            title: 'GENERAL',
            childrens: []
        },
        {
            title: 'PERFIL',
            childrens: []
        }
    ]);

    const searchForm:UnwrapRef<SearchForm>={
        search: ''
    };

    //
    const notificationsContainerRef = ref();
    const notifications = ref<NotificationItem[]>([ ]);

    /********************* 
    | Actions
    **********************/
    const doAddNew = ()=>{
        sendEvent('application:add-new', {severity: 'normal', message: ''});
    };

    const showMenu = () => {
        splitButton.value.onDropdownButtonClick();
    };

    //
    const checkScreenSize = () => {
        isLargeScreen.value = window.innerWidth >= 1024; 
        if(isLargeScreen.value){
            navbarVisible.value=true;
        }
    };
    const doToogleNavbar = ()=>{
        if (isMobile.value){
            navbarVisible.value=false;
        }
    };

    const toggleNotifications = (event:any) => {
        notificationsContainerRef.value.toggle(event);
    }

    const getCurrentPage = (path:string)=>{
        const options = menu.value[0].childrens.concat(menu.value[1].childrens);
        
        const option=options.filter(({text, url})=>{
            if(url === path){
                return text;
            }
        })[0];

        return option? option.text:'';
    };

    const doGlobalSearch = ()=>{
        sendEvent('application:search', {severity: 'normal', message: searchForm.search});
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(() => {
        checkScreenSize();
        window.addEventListener('resize', checkScreenSize);

        if(user.value?.is_provider && (user.value.is_first_register || user.value?.expiration_days > -1 || user.value?.expire)){
            const title = user.value?.is_first_register ? 'Activación de Cuenta' : (user.value.expiration_days > -1 ? 'Pago Próximo a Vencer':'Pago Vencido');
            const content = user.value?.is_first_register ? 'Primer pago sin realizar.':(user.value.expiration_days > -1 ? 'El pago vence en '+user.value?.expiration_days+' día(s).':'Su cuenta està restringida.');
            notifications.value.push({ 
                id: '0', 
                title: title, 
                content: content, 
                actionText: 'Pagar Ahora', 
                actionEvent:(event:any)=>{
                    const phoneNumber = companyPhoneNumber.value;
                    const message = `¡Hola! Necesito realizar *el pago mensual del servicio*.\nMi correo electrónico es: ${user.value?.email}.\nGracias!`; 
                    const encodedMessage = encodeURIComponent(message);
                    const whatsappUrl = isLargeScreen? `https://web.whatsapp.com/send/?phone=${phoneNumber}&text=${encodedMessage}&type=phone_number&app_absent=0`:`https://wa.me/${phoneNumber}/?text=${encodedMessage}`;
                    window.open(whatsappUrl);
                }
            });

            notificationsContainerRef.value.show({currentTarget: triggerButton.value});
        }

        //
        if (user.value?.is_superuser){
            const data={
                label: 'Configuración',
                icon: 'pi pi-cog',
                command: ()=>{
                    router.push('/dashboard/profile/company-data')
                }
            };
            toolbarMenu.value.splice(1, 0, data);
        }

        //
        var generalOptions=[
            {
                text: 'Productos',
                icon: 'pi-barcode',
                url: '/dashboard/general/products'
            },
            {
                text: 'Servicios',
                icon: 'pi-thumbs-up',
                url: '/dashboard/general/services'
            },
            {
                text: 'Pedidos',
                icon: 'pi-shopping-cart',
                url: '/dashboard/general/orders'
            },
            {
                text: 'Comentarios',
                icon: 'pi-comments',
                url: '/dashboard/general/comments'
            },
            {
                text: 'Reservaciones',
                icon: 'pi-calendar-clock',
                url: '/dashboard/general/reservations'
            }
        ];

        var profileOptions=[
            {
                text: 'Datos Contacto',
                icon: 'pi-address-book',
                url: '/dashboard/profile/contact-data'
            },
            {
                text: 'Datos Usuario',
                icon: 'pi-user',
                url: '/dashboard/profile/user-data'
            },
            {
                text: 'Mis Pagos',
                icon: 'pi-credit-card',
                url: '/dashboard/profile/my-payments'
            }
        ];

        if (user.value?.is_superuser){
            generalOptions=[
                {
                    text: 'Categorías',
                    icon: 'pi-tag',
                    url: '/dashboard/general/categories'
                },
                {
                    text: 'SubCategorías',
                    icon: 'pi-tags',
                    url: '/dashboard/general/subcategories'
                },
                {
                    text: 'Clientes',
                    icon: 'pi-users',
                    url: '/dashboard/general/clients'
                },
                {
                    text: 'Proveedores',
                    icon: 'pi-truck',
                    url: '/dashboard/general/providers'
                },
                {
                    text: 'Pagos',
                    icon: 'pi-credit-card',
                    url: '/dashboard/general/payments'
                },
                {
                    text: 'Extras',
                    icon: 'pi-question-circle',
                    url: '/dashboard/general/extras'
                }
            ];

            profileOptions=[
                {
                    text: 'Datos Empresa',
                    icon: 'pi-briefcase',
                    url: '/dashboard/profile/company-data'
                },
                {
                    text: 'Cuentas',
                    icon: 'pi-users',
                    url: '/dashboard/profile/accounts'
                }
            ];
        }

        menu.value[0].childrens=generalOptions;
        menu.value[1].childrens=profileOptions;
    });

    onMounted(async()=>{
        const resp:CompanyForm = await fetchWrapper.get('/company-data/info');
        companyLogo.value=resp.logo;
        companyName.value=resp.company_name;
        companyPhoneNumber.value=resp.customer_service_telephone;
    });
    onUnmounted(() => {
        window.removeEventListener('resize', checkScreenSize);
    });

</script>

<style scoped>
    ::-webkit-scrollbar {
        width: 5px;
        height: 5px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #2c3e508e;
        border-radius: 15px;
    }

    *:not(".pi"){
        font-family: 'Satoshi-Medium'!important;
    }
    .p-overlaypanel.my-panel:before {
        right: 10px !important;
    }

    .p-overlaypanel.my-panel:after {
        right: 10px !important;
    }
</style>