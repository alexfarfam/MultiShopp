<template>
    <div>
        <DataTable 
        v-model:selection="selectedPayment" 
        v-model:filters="filters" data-key="id" 
        selectionMode="single"
        class="mt-5" 
        filter-display="menu" 
        tableStyle="min-width: 50rem" 
        scrollHeight="300px" 
        :value="paymentData"
        :meta-key-selection="false" 
        :virtualScrollerOptions="{ itemSize: 40 }"
        :global-filter-fields="['provider__email', 'expiration_date', 'payment_date', 'creation_date', 'amount']"
        scrollable 
        removableSort
        >
            <template #header>
                <div class="justify-between">
                    <Button class="!hidden md:block" type="button" icon="pi pi-filter-slash" label="Limpiar Filtros" outlined @click="clearFilter()" />
                    <IconField>
                        <InputIcon>
                            <i class="pi pi-search" />
                        </InputIcon>
                        <InputText class="w-full" v-model="filters['global'].value" placeholder="Realizar una búsqueda" />
                    </IconField>
                </div>
            </template>

            <Column field="days_difference" header="Estado" :headerClass="'!bg-[#2D3040] !text-white !rounded-tl-lg'" sortable frozen>                           
                <template #body="slotProps">
                    <Tag 
                    :value="slotProps.data.days_difference < 5? ((slotProps.data.days_difference-1) >0 ? 'Vence en '+(slotProps.data.days_difference-1)+' día(s)'  : 'Vencido'):(slotProps.data.is_payment?'Pagado':'Por Pagar')" 
                    :severity="(slotProps.data.days_difference-1) < 5 ? 'danger':(slotProps.data.is_payment?'success':'info')" 
                    />
                    {{ slotProps.data.provider__email }}
                </template>

                <template #footer>
                    <div class="text-left font-bold">
                        Total:
                    </div>
                </template>
            </Column>  

            <Column field="expiration_date" filterField="expiration_date" header="Fecha Expiración"
                :showFilterMatchModes="false" :filterMenuStyle="{ width: '16rem' }"
                :headerClass="'!bg-[#2D3040] !text-white'" sortable>
                <template #filter="{ filterModel, filterCallback }">
                    <MultiSelect filter-placeholder="Buscar" v-model="filterModel.value" @change="filterCallback()"
                        :options="uniquesExpirationDates" placeholder="Seleccionar" style="min-width: 14rem" filter>
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

            <Column field="payment_date" filterField="payment_date" header="Fecha Pago" :showFilterMatchModes="false"
                :filterMenuStyle="{ width: '16rem' }" :headerClass="'!bg-[#2D3040] !text-white'" sortable>
                <template #filter="{ filterModel, filterCallback }">
                    <MultiSelect filter-placeholder="Buscar" v-model="filterModel.value" @change="filterCallback()"
                        :options="uniquesPaymentDates" placeholder="Seleccionar" style="min-width: 14rem" filter>
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

            <Column field="creation_date" filter-field="creation_date" header="Fecha Creación"
                :showFilterMatchModes="false" :filterMenuStyle="{ width: '16rem' }"
                :headerClass="'!bg-[#2D3040] !text-white'" sortable>
                <template #filter="{ filterModel, filterCallback }">
                    <MultiSelect filter-placeholder="Buscar" v-model="filterModel.value" @change="filterCallback()"
                        :options="uniquesCreationDates" placeholder="Seleccionar" style="min-width: 14rem" filter>
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

            <Column field="amount" filter-field="amount" header="Monto" :showFilterMatchModes="false"
                :filterMenuStyle="{ width: '16rem' }" :headerClass="'!bg-[#2D3040] !text-white !rounded-tr-lg'"
                sortable>
                <template #filter="{ filterModel, filterCallback }">
                    <MultiSelect filter-placeholder="Buscar" v-model="filterModel.value" @change="filterCallback()"
                        :options="uniquesAmounts" placeholder="Seleccionar" style="min-width: 14rem" filter>
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
    </div>
</template>

<script lang="ts" setup>
    import { ref} from 'vue';
    import { FilterMatchMode } from '@primevue/core/api';

    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import type {PaymentItem } from '~/types/dashboard/payments';
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
    const filters = ref();
    const selectedPayment = ref();

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

    initFilters();
    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        paymentData.value=await fetchWrapper.get('/payments/by_provider');

        uniquesEmails.value=getUniqueValuesByProperty(paymentData.value, 'provider__email');
        uniquesExpirationDates.value=getUniqueValuesByProperty(paymentData.value, 'expiration_date');
        uniquesCreationDates.value=getUniqueValuesByProperty(paymentData.value, 'creation_date');
        uniquesPaymentDates.value=getUniqueValuesByProperty(paymentData.value, 'payment_date');
        uniquesAmounts.value=getUniqueValuesByProperty(paymentData.value, 'amount');
    });

</script>