<template>
    <div>
        <DataView class="!bg-transparent" :value="filteredClientData" data-key="id">
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
                                            <span class="text-[12px] w-fit px-2 h-6 pt-1 mt-2 text-white rounded-md text-center" :class="item.is_confirmed ? 'bg-green-500':'bg-red-500'">{{ item.is_confirmed ? 'Email Confirmado':'Email sin confirmar' }}</span>
                                        </div>

                                        <div class="mt-4 md:mt-2 flex flex-col md:flex-row gap-1 md:gap-3">
                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Nombres: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ item.username }}</span>
                                            </div>
                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Fecha Creación: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ Globalization.dateFormat2(item.joined_date, false) }}</span>
                                            </div>
                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Último Login: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm"> {{ item.last_login === null ? '':Globalization.dateFormat2(item.last_login, false) }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="flex mt-0 md:mt-4 flex-col md:items-end gap-3">
                                    <div class="flex flex-row-reverse md:flex-row gap-2">
                                        <Button class="!bg-[#4F61E3] !border-[#4F61E3]" @click="doEdit(item.id)" icon="pi pi-pencil" label="Editar"></Button>
                                        <Button @click="confirmDelete(item.id)" severity="danger" icon="pi pi-trash" label="Eliminar"></Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </template>

            <template #empty>
                <span class="mt-48 block !text-4xl text-gray-400/[0.8] pi pi-folder-open w-full text-center"></span>
                <span class="mt-4 block text-2xl text-gray-400/[0.8] w-full text-center">Sin clientes para mostrar</span>
            </template>
        </DataView>
    </div>

    <Toast />
    <ConfirmDialog></ConfirmDialog>

    <Dialog dismissable-mask v-model:visible="showEditModal" modal header="Editar Proveedor" :style="{ width: '25rem' }">
        <form @submit.prevent="confirmEdit">
            <div class="flex items-center gap-4 mb-8">
                <label for="email" class="font-semibold w-24">Activo?</label>
                <Checkbox v-model="clientForm.is_active" :binary="true" />
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

    import { useConfirm } from "primevue/useconfirm";
    import { useToast } from "primevue/usetoast";

    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import { Globalization } from '~/helpers/globalization';
    import { useListen } from '~/composables/useMitt';
    import type { ClientItem, ClientForm } from '~/types/dashboard/clients';

    // Meta configuration
    const confirm = useConfirm();
    const toast = useToast();

    useListen('application:search' , (message:any) => {
        const search = (message.message as string).toLowerCase();
        filteredClientData.value=clientData.value.filter(entry=>{
            return (
                entry.username.toLowerCase().includes(search) ||
                entry.email.toLowerCase().includes(search) ||
                Globalization.dateFormat2(entry.date_joined, false).includes(search) ||
                Globalization.dateFormat2((entry.date_joined === null?'':entry.date_joined), false).includes(search) ||
                (entry.is_active ? 'email confirmado':'email sin confirmar').includes(search)
            );
        });
    });

    /********************* 
    | DATA
    **********************/
    const currentId = ref<number>(-1);
    const loadingSubmit=ref<boolean>(false);

    const showEditModal=ref<boolean>(false);
    const clientData=ref<ClientItem[]>([]);
    const filteredClientData=ref<ClientItem[]>([]);

    const clientForm:UnwrapRef<ClientForm> = reactive({
        is_active: false
    });

    /********************* 
    | METHODS
    **********************/
    const doEdit = (id:number)=>{
        currentId.value=id;
        const index = filteredClientData.value.findIndex(obj => obj.id === currentId.value);
        const obj = filteredClientData.value[index];
        clientForm.is_active=obj.is_active;

        showEditModal.value=true;
    };

    const confirmDelete = (id:number) => {
        const index = filteredClientData.value.findIndex(obj => obj.id === id);
        const obj = filteredClientData.value[index];

        confirm.require({
            message: 'Seguro(a) que quieres borrar al cliente "'+obj.email+'"?',
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
                params.append('client_ids', JSON.stringify([id]));
                await fetchWrapper.delete('/clients/delete?'+ params).then((msg)=>{
                    filteredClientData.value=filteredClientData.value.filter(item => item.id !== id);
                    clientData.value=clientData.value.filter(item => item.id !== id);

                    toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
                }).catch((e)=>{
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Error al eliminar: '+JSON.stringify(e), life: 6000 });
                });
            }
        });
    };

    const confirmEdit = async()=>{
        const params = new URLSearchParams();
        params.append('client_id', currentId.value.toString());

        loadingSubmit.value=true;
        await fetchWrapper.put('/clients/client?'+params, clientForm).then((resp)=>{
            const index = filteredClientData.value.findIndex(obj => obj.id === currentId.value);
            filteredClientData.value[index]=resp['data'];

            toast.add({ severity: 'success', summary: 'Confirmación', detail: resp['msg'], life: 5000 });
            loadingSubmit.value=false;
            showEditModal.value=false;
        }).catch((e)=>{
            loadingSubmit.value=false;
            showEditModal.value=false;
            toast.add({ severity: 'error', summary: 'Error', detail: 'Error al editar: '+JSON.stringify(e), life: 7000 });
        });
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        clientData.value=await fetchWrapper.get('/clients/clients');
        filteredClientData.value=cloneDeep(clientData.value);
    });

</script>