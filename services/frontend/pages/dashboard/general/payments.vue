<template>
    <div>
        <Tabs v-model:value="currentTab" class="!shadow-lg" scrollable>
            <TabList>
                <Tab @click="updatePayments(tab.value)" class="flex items-center gap-2 text-inherit !font-normal" v-for="tab in tabs" :key="tab.title" :value="tab.value">
                    <svg-icon class="icon" size="24" type="mdi" :path="tab.icon"></svg-icon>
                    <span class="hidden md:block">Pagos</span> {{ tab.title }}
                    <Badge v-show="(paymentStatus && paymentStatus.hasOwnProperty(tab.value))" size="small" severity="primary" :value="(paymentStatus && paymentStatus.hasOwnProperty(tab.value)) ? paymentStatus[tab.value]:''" />
                </Tab>
            </TabList>

            <TabPanels class="!px-2">
                <TabPanel v-for="tab in tabs" :key="tab.value" :value="tab.value">
                    <form class="p-4 mt-2 flex flex-col md:flex-row gap-4" v-show="currentTab === 'pending'">
                        <div class="flex items-center gap-1">
                            <label for="provider" class="font-semibold w-24">Proveedor:</label>
                            <InputText v-model:model-value="currentPaymentSelection.provider__email" :disabled="true" id="provider" class="flex-auto"/>
                        </div>
                        <div class="flex items-center gap-1">
                            <label for="expiration_date" class="font-semibold w-24">Expiración:</label>
                            <InputText v-model:model-value="currentPaymentSelection.expiration_date" :disabled="true" id="expiration_date" class="flex-auto"/>
                        </div>
                        <div class="flex items-center gap-1">
                            <label for="amount" class="font-semibold w-24">Monto:</label>
                            <InputNumber v-model:model-value="currentPaymentSelection.amount" :disabled="true" inputId="amount" mode="currency" currency="ARS" locale="es-AR" class="flex-auto"/>
                        </div>
                        <div class="flex justify-end gap-2">
                            <Button @click="confirmPayment" :disabled="currentPaymentSelection.provider__email === ''" type="button" label="Pagado"></Button>
                            <Button @click="clearForm" type="button" label="Limpiar" severity="secondary"></Button>
                        </div>
                    </form>                   

                    <DataTable 
                    v-model:selection="selectedPayment" 
                    v-model:filters="filters"
                    data-key="id"
                    selectionMode="single" 
                    class="mt-5" 
                    filter-display="menu"
                    tableStyle="min-width: 50rem"
                    scrollHeight="300px" 

                    :value="paymentData" 
                    :meta-key-selection="false" 
                    :virtualScrollerOptions="{ itemSize: 40 }"
                    :global-filter-fields="['provider__email', 'expiration_date', 'payment_date', 'creation_date', 'amount']"
                    
                    @row-select="doPaymentSelection"
                    @row-unselect="doPaymentUnSelection"

                    scrollable 
                    removableSort
                    >
                    <template #header>
                        <div class="flex justify-between">
                            <Button class="!hidden md:block" type="button" icon="pi pi-filter-slash" label="Limpiar Filtros" outlined @click="clearFilter()" />
                            <IconField>
                                <InputIcon>
                                    <i class="pi pi-search" />
                                </InputIcon>
                                <InputText v-model="filters['global'].value" placeholder="Realizar una búsqueda" />
                            </IconField>
                        </div>
                    </template>
                   
                        <Column field="provider__email" filterField="provider__email" :showFilterMatchModes="false" :filterMenuStyle="{ width: '16rem' }" header="Proveedor" :headerClass="'!bg-[#2D3040] !text-white !rounded-tl-lg'" sortable frozen>                           
                            <template #filter="{ filterModel, filterCallback }">
                                <MultiSelect filter-placeholder="Buscar" v-model="filterModel.value" @change="filterCallback()" :options="uniquesEmails" placeholder="Seleccionar" style="min-width: 14rem" filter>
                                    <template #option="slotProps">
                                        <div class="flex items-center gap-2">
                                            <Avatar icon="pi pi-envelope" />
                                            <span>{{slotProps.option, false}}</span>
                                        </div>
                                    </template>

                                    <template #emptyfilter>
                                        <div class="text-center py-4 text-gray-500/[0.8]">
                                            Sin resultados
                                        </div>
                                    </template>

                                    <template #empty>
                                        <div class="text-center py-4 text-gray-500/[0.8]">
                                            Sin datos
                                        </div>
                                    </template>
                                </MultiSelect>
                            </template>

                            <template #body="slotProps">
                                <Tag v-if="currentTab === 'pending'" :value="slotProps.data.days_difference < 5? 'Vence en '+(slotProps.data.days_difference-1)+' día(s)':'Pagado'" :severity="(slotProps.data.days_difference-1) < 5 ? 'danger':'success'" />
                                {{ slotProps.data.provider__email }}
                            </template>

                            <template #footer>
                                <div class="text-left font-bold">
                                   Total:
                                </div>
                            </template>
                        </Column>  

                        <Column field="expiration_date" filterField="expiration_date" header="Fecha Expiración" :showFilterMatchModes="false" :filterMenuStyle="{ width: '16rem' }" :headerClass="'!bg-[#2D3040] !text-white'" sortable>
                            <template #filter="{ filterModel, filterCallback }">
                                <MultiSelect filter-placeholder="Buscar" v-model="filterModel.value" @change="filterCallback()" :options="uniquesExpirationDates" placeholder="Seleccionar" style="min-width: 14rem" filter>
                                    <template #option="slotProps">
                                        <div class="flex items-center gap-2">
                                            <Avatar icon="pi pi-calendar-clock" />
                                            <span>{{ Globalization.dateFormat2(slotProps.option, false)}}</span>
                                        </div>
                                    </template>

                                    <template #emptyfilter>
                                        <div class="text-center py-4 text-gray-500/[0.8]">
                                            Sin resultados
                                        </div>
                                    </template>

                                    <template #empty>
                                        <div class="text-center py-4 text-gray-500/[0.8]">
                                            Sin datos
                                        </div>
                                    </template>

                                </MultiSelect>
                            </template>

                            <template #body="slotProps">
                                {{ Globalization.dateFormat2(slotProps.data.expiration_date, false) }}
                            </template>
                        </Column>

                        <Column v-if="currentTab === 'paid'" field="payment_date" filterField="payment_date" header="Fecha Pago" :showFilterMatchModes="false" :filterMenuStyle="{ width: '16rem' }" :headerClass="'!bg-[#2D3040] !text-white'" sortable>
                            <template #filter="{ filterModel, filterCallback }">
                                <MultiSelect filter-placeholder="Buscar" v-model="filterModel.value" @change="filterCallback()" :options="uniquesPaymentDates" placeholder="Seleccionar" style="min-width: 14rem" filter>
                                    <template #option="slotProps">
                                        <div class="flex items-center gap-2">
                                            <Avatar icon="pi pi-calendar-clock" />
                                            <span>{{ Globalization.dateFormat2(slotProps.option, false)}}</span>
                                        </div>
                                    </template>

                                    <template #emptyfilter>
                                        <div class="text-center py-4 text-gray-500/[0.8]">
                                            Sin resultados
                                        </div>
                                    </template>

                                    <template #empty>
                                        <div class="text-center py-4 text-gray-500/[0.8]">
                                            Sin datos
                                        </div>
                                    </template>

                                </MultiSelect>
                            </template>

                            <template #body="slotProps">
                                {{ Globalization.dateFormat2(slotProps.data.payment_date, false) }}
                            </template>
                        </Column>

                        <Column field="creation_date" filter-field="creation_date" header="Fecha Creación" :showFilterMatchModes="false" :filterMenuStyle="{ width: '16rem' }" :headerClass="'!bg-[#2D3040] !text-white'" sortable>
                            <template #filter="{ filterModel, filterCallback }">
                                <MultiSelect filter-placeholder="Buscar" v-model="filterModel.value" @change="filterCallback()" :options="uniquesCreationDates" placeholder="Seleccionar" style="min-width: 14rem" filter>
                                    <template #option="slotProps">
                                        <div class="flex items-center gap-2">
                                            <Avatar icon="pi pi-calendar-clock" />
                                            <span>{{ Globalization.dateFormat2(slotProps.option, false)}}</span>
                                        </div>
                                    </template>

                                    <template #emptyfilter>
                                        <div class="text-center py-4 text-gray-500/[0.8]">
                                            Sin resultados
                                        </div>
                                    </template>

                                    <template #empty>
                                        <div class="text-center py-4 text-gray-500/[0.8]">
                                            Sin datos
                                        </div>
                                    </template>

                                </MultiSelect>
                            </template>

                            <template #body="slotProps">
                                {{ Globalization.dateFormat2(slotProps.data.creation_date, false) }}
                            </template>
                        </Column>

                        <Column field="amount" filter-field="amount" header="Monto" :showFilterMatchModes="false" :filterMenuStyle="{ width: '16rem' }" :headerClass="'!bg-[#2D3040] !text-white !rounded-tr-lg'" sortable>
                            <template #filter="{ filterModel, filterCallback }">
                                <MultiSelect filter-placeholder="Buscar" v-model="filterModel.value" @change="filterCallback()" :options="uniquesAmounts" placeholder="Seleccionar" style="min-width: 14rem" filter>
                                    <template #option="slotProps">
                                        <div class="flex items-center gap-2">
                                            <Avatar icon="pi pi-dollar" />
                                            <span>{{ Globalization.currencyFormat.format(slotProps.option)}}</span>
                                        </div>
                                    </template>

                                    <template #emptyfilter>
                                        <div class="text-center py-4 text-gray-500/[0.8]">
                                            Sin resultados
                                        </div>
                                    </template>

                                    <template #empty>
                                        <div class="text-center py-4 text-gray-500/[0.8]">
                                            Sin datos
                                        </div>
                                    </template>

                                </MultiSelect>
                            </template>

                            <template #body="slotProps">
                                {{ Globalization.currencyFormat.format(slotProps.data.amount) }}
                            </template>

                            <template #footer>
                                <div class="text-left font-bold">
                                   {{ Globalization.currencyFormat.format(totalAmount) }}
                                </div>
                            </template>
                        </Column>

                        <template #empty>
                            <div class="text-lg text-center py-20 text-gray-500/[0.8]">
                                No hay pagos para mostrar.
                            </div>
                        </template>
                    </DataTable>
                </TabPanel>
            </TabPanels>
        </Tabs>
    </div>

    <Toast />
    <ConfirmDialog></ConfirmDialog>
</template>

<script lang="ts" setup>
    import { ref, type UnwrapRef } from 'vue';
    import { FilterMatchMode } from '@primevue/core/api';

    import { useConfirm } from "primevue/useconfirm";
    import { useToast } from "primevue/usetoast";

    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import { mdiCreditCardCheck, mdiCreditCardClock, mdiCreditCardRemove } from '@mdi/js';
    import type { PaymentForm, PaymentItem } from '~/types/dashboard/payments';
    import { Globalization } from '~/helpers/globalization';
    
    // Meta configuration
    const totalAmount = computed(() => {
        return paymentData.value.reduce((sum, payment) => sum + payment.amount, 0);
    });

    function getUniqueValuesByProperty<T, K extends keyof T>(
        array: T[],
        property: K,
        formatter?: (value: T[K]) => any
    ): any[] {
        const uniqueValues = array
            .map(item => item[property])
            .filter((value, index, self) => self.indexOf(value) === index)
            .map(value => (formatter ? formatter(value) : value));

        return uniqueValues;
    }
    const confirm = useConfirm();
    const toast = useToast();

    /********************* 
    | DATA
    **********************/
    const tabs = ref([
        { title: 'Pendientes', value: 'pending', icon:  mdiCreditCardClock},
        { title: 'Realizados', value: 'paid', icon:  mdiCreditCardCheck},
        { title: 'Vencidos', value: 'payment_due', icon:  mdiCreditCardRemove}
    ]);
    const filters = ref();
    const selectedPayment = ref();
    const currentTab = ref<string>('pending');
    const currentPaymentSelection:UnwrapRef<PaymentForm> = reactive({
        id: -1,
        provider__email: '',
        expiration_date: '',
        amount: 0
    });

    const paymentStatus = ref();
    const paymentData = ref<PaymentItem[]>([]);
    const uniquesEmails = ref<string[]>([]);
    const uniquesExpirationDates = ref<string[]>([]);
    const uniquesCreationDates = ref<string[]>([]);
    const uniquesPaymentDates = ref<string[]>([]);
    const uniquesAmounts = ref<number[]>([]);
    
    /********************* 
    | METHODS
    **********************/
    const initFilters = () => {
        filters.value = {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
            amount: { value: null, matchMode: FilterMatchMode.IN },
            payment_date: { value: null, matchMode: FilterMatchMode.IN },
            expiration_date: { value: null, matchMode: FilterMatchMode.IN },
            provider__email: { value: null, matchMode: FilterMatchMode.IN },
            creation_date: { value: null, matchMode: FilterMatchMode.IN }
        };
    };
    const clearFilter = () => {
        initFilters();
    };

    const updatePayments = async(status:string)=>{
        const params=new URLSearchParams();
        params.append('_filter', status);

        const resp=await fetchWrapper.get('/payments/all?'+params);
        paymentStatus.value=resp['status'];
        paymentData.value=resp['data'];

        uniquesEmails.value=getUniqueValuesByProperty(paymentData.value, 'provider__email');
        uniquesExpirationDates.value=getUniqueValuesByProperty(paymentData.value, 'expiration_date');
        uniquesCreationDates.value=getUniqueValuesByProperty(paymentData.value, 'creation_date');
        uniquesPaymentDates.value=getUniqueValuesByProperty(paymentData.value, 'payment_date');
        uniquesAmounts.value=getUniqueValuesByProperty(paymentData.value, 'amount');
    };

    const doPaymentSelection=()=>{
        currentPaymentSelection.id=selectedPayment.value.id;
        currentPaymentSelection.provider__email=selectedPayment.value.provider__email;
        currentPaymentSelection.expiration_date=Globalization.dateFormat2(selectedPayment.value.expiration_date, false);
        currentPaymentSelection.amount = selectedPayment.value.amount;
    };
    const doPaymentUnSelection=()=>{
        currentPaymentSelection.id=-1;
        currentPaymentSelection.provider__email='';
        currentPaymentSelection.expiration_date='';
        currentPaymentSelection.amount=0;
    };

    const clearForm = ()=>{
        selectedPayment.value=null;
        doPaymentUnSelection();
    };
    const confirmPayment = () => {
        confirm.require({
            message: 'Seguro(a) que quieres realizar este pago?',
            header: 'Confirmar pago',
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
                params.append('payment_id', currentPaymentSelection.id.toString());

                await fetchWrapper.put('/payments/update?'+params).then((resp)=>{
                    const index = paymentData.value.findIndex(obj => obj.id === currentPaymentSelection.id);

                    paymentStatus.value['paid']=paymentStatus.value.hasOwnProperty('paid') ? (parseInt(paymentStatus.value['paid']) + 1):0;
                    paymentData.value[index]=resp['data'];
                    clearForm();

                    toast.add({ severity: 'success', summary: 'Confirmación', detail: resp['msg'], life: 4000 });
                }).catch((e)=>{
                    toast.add({ severity: 'error', summary: 'Error', detail: JSON.stringify(e), life: 8000 });
                });
                
            }
        });
    };

    initFilters();
    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        const params=new URLSearchParams();
        params.append('_filter', 'pending');

        const resp=await fetchWrapper.get('/payments/all?'+params);
        paymentStatus.value=resp['status'];
        paymentData.value=resp['data'];

        uniquesEmails.value=getUniqueValuesByProperty(paymentData.value, 'provider__email');
        uniquesExpirationDates.value=getUniqueValuesByProperty(paymentData.value, 'expiration_date');
        uniquesCreationDates.value=getUniqueValuesByProperty(paymentData.value, 'creation_date');
        uniquesPaymentDates.value=getUniqueValuesByProperty(paymentData.value, 'payment_date');
        uniquesAmounts.value=getUniqueValuesByProperty(paymentData.value, 'amount');
    });

</script>
