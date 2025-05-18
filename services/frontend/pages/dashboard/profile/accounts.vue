<template>
    <div>
        <DataView class="!bg-transparent" :value="filteredAccountData" data-key="id">
            <template #list="slotProps">
                <div class="flex flex-col gap-6">
                    <div v-for="(item, index) in slotProps.items" :key="index">
                        <div class="flex flex-row p-2 gap-2 border border-surface-200 bg-white shadow-md rounded-xl ">
                            <div class="w-18 md:w-20 relative">
                                <i class="bg-[#001529] text-white rounded-full px-5 py-[31px] m-2 text-center !text-xl/[0] pi pi-user"></i>
                            </div>
                            <div class="flex flex-col md:flex-row justify-between md:items-center flex-1 gap-6">
                                <div class="flex flex-row md:flex-col justify-between items-start gap-3">
                                    <div>
                                        <div class="flex flex-col md:flex-row gap-1 md:gap-2">
                                            <span class="text-base font-medium mt-2">{{ item.email }}</span>
                                            <span class="text-[12px] w-fit px-2 h-6 pt-1 mt-2 text-white rounded-md text-center" :class="item.is_active ? 'bg-green-500':'bg-red-500'">{{ item.is_active ? 'Activo':'Inactivo' }}</span>
                                            <span class="text-[12px] w-fit px-2 h-6 pt-1 mt-2 text-white rounded-md text-center" :class="item.is_superuser ? 'bg-orange-500':'bg-gray-500'">{{ item.is_superuser ? 'SuperUsuario':'Cuenta Normal' }}</span>
                                            <span v-if="item.id === user?.id" class="text-[12px] w-fit px-2 h-6 pt-1 mt-2 text-white rounded-md text-center bg-purple-500">Cuenta Logeada</span>
                                        </div>

                                        <div class="mt-4 md:mt-2 flex flex-col md:flex-row gap-1 md:gap-3">
                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Nombres: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ item.username }}</span>
                                            </div>
                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Fecha Creación: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ Globalization.dateFormat2(item.joined_date, false) }}</span>
                                            </div>
                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Último account: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm"> {{ item.last_account === null ? '':Globalization.dateFormat2(item.last_account, false) }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="flex mt-0 md:mt-4 flex-col md:items-end gap-3">
                                    <div class="flex flex-row-reverse md:flex-row gap-2">
                                        <Button class="!bg-[#4F61E3] !border-[#4F61E3]" @click="doEdit(item.id)" icon="pi pi-pencil" label="Editar"></Button>
                                        <Button v-if="item.id !== user?.id" @click="confirmDelete(item.id)" severity="danger" icon="pi pi-trash" label="Eliminar"></Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </template>

            <template #empty>
                <span class="mt-48 block !text-4xl text-gray-400/[0.8] pi pi-folder-open w-full text-center"></span>
                <span class="mt-4 block text-2xl text-gray-400/[0.8] w-full text-center">Sin Cuentas para mostrar</span>
            </template>
        </DataView>
    </div>

    <Toast />
    <ConfirmDialog></ConfirmDialog>

    <Dialog dismissable-mask v-model:visible="showEditModal" modal :header="formTitle" :style="{ width: '25rem' }">
        <form autocomplete="new-password2" @submit.prevent="confirmEdit">
            <div class="mb-4">
                <label class="mb-2.5 block font-medium text-black dark:text-white" for="username">Nombre de Usuario:</label>
                <InputText 
                v-model:model-value="accountForm.username"
                autocomplete="new-password2" 
                class="w-full" 
                placeholder="Nombre de Usuario" 
                id="username" 
                :class="{'!border !border-red-500': $accountValidator.username.$invalid && $accountValidator.username.$dirty}"
                @input="$accountValidator.username.$touch()" 
                aria-describedby="account-username-help"
                />
                <small id="account-username-help" v-if="$accountValidator.username.required.$invalid && $accountValidator.username.$dirty" class="text-red-600">Nombre de Usuario requerido.</small>
                <small id="account-username-help" v-else-if="$accountValidator.username.minLength.$invalid && $accountValidator.username.$dirty" class="text-red-600">Nombre de Usuario muy corto.</small>
            </div>

            <div class="mb-4">
                <label class="mb-2.5 block font-medium text-black dark:text-white" for="email">Correo Electrónico:</label>
                <InputText 
                v-model:model-value="accountForm.email"
                type="email"  
                autocomplete="new-password2" 
                class="w-full" 
                placeholder="Correo Electrónico" 
                id="email" 
                :class="{'!border !border-red-500': $accountValidator.email.$invalid && $accountValidator.email.$dirty}"
                @input="$accountValidator.email.$touch()" 
                aria-describedby="account-email-help"
                />
                <small id="account-email-help" v-if="$accountValidator.email.required.$invalid && $accountValidator.email.$dirty" class="text-red-600">Correo Electrónico requerido.</small>
                <small id="account-email-help" v-else-if="$accountValidator.email.email.$invalid && $accountValidator.email.$dirty" class="text-red-600">Correo Electrónico inválido.</small>
            </div>

            <div class="mb-4">
                <label class="mb-2.5 block font-medium text-black dark:text-white" for="password">Contraseña:</label>
                <Password 
                v-model:model-value="accountForm.password"
                autocomplete="new-password2" 
                :feedback="true" 
                toggle-mask 
                fluid 
                placeholder="Ingresa tu contraseña" 
                id="password" 
                promptLabel="Ingrese una contraseña"
                weakLabel="Contraseña débil"
                mediumLabel="Contraseña aceptable"
                strongLabel="Contraseña robusta"
                :class="{'!border !border-red-500': $accountValidator.password.$invalid && $accountValidator.password.$dirty}"
                @input="$accountValidator.password.$touch()" 
                aria-describedby="account-password-help"
                />
                <small id="account-password-help" v-if="$accountValidator.password.required.$invalid && $accountValidator.password.$dirty" class="text-red-600">Contraseña Requerida</small>
            </div>

            <div class="flex items-center gap-4 mb-8">
                <label for="email" class="font-semibold w-24">Activo?</label>
                <Checkbox v-model="accountForm.is_active" :binary="true" />
            </div>
            
            <div class="flex items-center gap-4 mb-8">
                <label for="email" class="font-semibold w-24">Admin?</label>
                <Checkbox v-model="accountForm.is_superuser" :binary="true" />
            </div>
   
            <div class="flex justify-end gap-2">
                <Button type="button" label="Cancelar" severity="secondary" @click="showEditModal = false"></Button>
                <Button type="submit" label="Guardar" :loading="loadingSubmit"></Button>
            </div>
        </form>
    </Dialog>
</template>

<script lang="ts" setup>
    import {ref, type UnwrapRef} from 'vue';
    import { cloneDeep } from 'lodash-es';

    import { storeToRefs } from 'pinia';
    import { useConfirm } from "primevue/useconfirm";
    import { useToast } from "primevue/usetoast";
    import { minLength, required, email } from '@vuelidate/validators';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import { Globalization } from '~/helpers/globalization';
    import useVuelidate from '@vuelidate/core';
    import { useListen } from '~/composables/useMitt';
    import type { AccountForm, AccountItem } from '~/types/dashboard/accounts';

    // Meta configuration
    const confirm = useConfirm();
    const toast = useToast();

    const authStore= useAuthStore();
    const {user} = storeToRefs(authStore);

    function resetForm(){
        accountForm.username='';
        accountForm.email='';
        accountForm.password='';
        accountForm.is_superuser = false;
        accountForm.is_active = false;

        $accountValidator.value.$reset();
    };
    const accountRules = computed(() => ({
        username: {
            required,
            minLength: minLength(4),
        },
        password: {
            required
        },
        email: {
            required,
            email
        }
    }));

    useListen('application:search' , (message:any) => {
        const search = (message.message as string).toLowerCase();
        filteredAccountData.value=accountData.value.filter(entry=>{
            return (
                entry.username.toLowerCase().includes(search) ||
                entry.email.toLowerCase().includes(search) ||
                Globalization.dateFormat2(entry.date_joined, false).includes(search) ||
                Globalization.dateFormat2((entry.date_joined === null?'':entry.date_joined), false).includes(search) ||
                (entry.is_active ? 'activo':'inactivo').includes(search)
            );
        });
    });
    useListen('application:add-new' , (message:any) => {
        doNew();
    });

    /********************* 
    | DATA
    **********************/
    const currentId = ref<number>(-1);
    const loadingSubmit=ref<boolean>(false);
    const formTitle = ref<string>('');

    const showEditModal=ref<boolean>(false);
    const accountData=ref<AccountItem[]>([]);
    const filteredAccountData=ref<AccountItem[]>([]);

    const accountForm:UnwrapRef<AccountForm> = reactive({
        username: '',
        password: '',
        email: '',
        is_superuser: false,
        is_active: false
    });
    const $accountValidator=useVuelidate(accountRules, accountForm);

    /********************* 
    | METHODS
    **********************/
    const doNew=()=>{
        resetForm();
        currentId.value=-1;
        formTitle.value='Nueva Cuenta';
        showEditModal.value=true;
    };

    const doEdit = (id:number)=>{
        currentId.value=id;
        const index = filteredAccountData.value.findIndex(obj => obj.id === currentId.value);
        const obj = filteredAccountData.value[index];
        accountForm.username=obj.username;
        accountForm.password=obj.password;
        accountForm.email=obj.email;
        accountForm.is_superuser = obj.is_superuser;
        accountForm.is_active = obj.is_active;

        formTitle.value='Editar Cuenta';
        showEditModal.value=true;
    };

    const confirmDelete = (id:number) => {
        const index = filteredAccountData.value.findIndex(obj => obj.id === currentId.value);
        const obj = filteredAccountData.value[index];

        confirm.require({
            message: 'Seguro(a) que quieres borrar la cuenta de "'+obj.email+'"?',
            header: 'Confirmar eliminación',
            icon: 'pi pi-info-circle',
            rejectLabel: 'Cancelar',
            rejectProps: {
                label: 'Cancelar',
                severity: 'secondary',
                outlined: true
            },
            acceptProps: {
                label: 'Confirmar',
                severity: 'danger'
            },
            accept: async() => {
                const params = new URLSearchParams();
                params.append('account_ids', JSON.stringify([id]));
                await fetchWrapper.delete('/accounts/delete?'+ params).then((msg)=>{
                    filteredAccountData.value=filteredAccountData.value.filter(item => item.id !== id);
                    accountData.value=accountData.value.filter(item => item.id !== id);

                    toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
                }).catch((e)=>{
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Error al eliminar: '+JSON.stringify(e), life: 6000 });
                });
            }
        });
    };

    const confirmEdit = async()=>{
        const params = new URLSearchParams();
        params.append('account_id', currentId.value.toString());

        loadingSubmit.value=true;
        if(currentId.value === -1){
            await fetchWrapper.post('/accounts/account', accountForm).then((resp)=>{
                const index = filteredAccountData.value.findIndex(obj => obj.id === currentId.value);
                filteredAccountData.value.push(resp['data']);

                toast.add({ severity: 'success', summary: 'Confirmación', detail: resp['msg'], life: 5000 });
                loadingSubmit.value=false;
                showEditModal.value=false;
            }).catch((e)=>{
                loadingSubmit.value=false;
                showEditModal.value=false;
                toast.add({ severity: 'error', summary: 'Error', detail: 'Error al guardar: '+JSON.stringify(e), life: 7000 });
            });
        }else{
            const params = new URLSearchParams();
            params.append('account_id', currentId.value.toString());

            await fetchWrapper.put('/accounts/account?'+params, accountForm).then((resp)=>{
                const index = filteredAccountData.value.findIndex(obj => obj.id === currentId.value);
                filteredAccountData.value[index]=resp['data'];

                toast.add({ severity: 'success', summary: 'Confirmación', detail: resp['msg'], life: 5000 });
                loadingSubmit.value=false;
                showEditModal.value=false;
            }).catch((e)=>{
                loadingSubmit.value=false;
                showEditModal.value=false;
                toast.add({ severity: 'error', summary: 'Error', detail: 'Error al editar: '+JSON.stringify(e), life: 7000 });
            });  
        }
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        accountData.value=await fetchWrapper.get('/accounts/accounts');
        filteredAccountData.value=cloneDeep(accountData.value);
    });

</script>