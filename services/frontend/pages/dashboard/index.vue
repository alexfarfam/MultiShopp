<template>
    <div class="top-[-2rem] relative flex flex-row gap-4 w-full">
        <span class="ml-6 md:ml-0 mt-4 md:mt-0 text-2xl font-medium">Resumen diario</span>
    </div>

    <div class="mt-4 flex flex-wrap flex-row gap-10" v-if="user?.is_provider">
        <nuxt-link to="/dashboard/general/reservations" class="mx-6 md:mx-0 cursor-pointer basis-full md:flex-1 flex flex-col gap-1 p-5 shadow-lg bg-white">
            <div class="flex flex-row gap-3 align-middle content-center">
                <i class="rounded-full text-indigo-700 bg-indigo-500/[0.2] p-4 pi pi-calendar-clock"></i>
                <span class="mt-1 text-4xl font-medium">{{ summary?.reservations_count }}</span>
            </div>
            <div class="w-full text-left px-2">
                <span class="w-full block text-lg text-center text-slate-400">Reservas pendientes</span>
            </div>
        </nuxt-link >

        <nuxt-link to="/dashboard/general/products" class="mx-6 md:mx-0 cursor-pointer basis-full md:flex-1 flex flex-col gap-1 p-5 shadow-lg bg-white">
            <div class="flex flex-row gap-3 align-middle content-center">
                <i class="rounded-full text-indigo-700 bg-indigo-500/[0.2] p-4 pi pi-barcode"></i>
                <span class="mt-1 text-4xl font-medium">{{ summary?.products_count }}</span>
            </div>
            <div class="w-full text-left px-2">
                <span class="w-full block text-lg text-center text-slate-400">Producto(s) en stock</span>
            </div>
        </nuxt-link>

        <nuxt-link to="/dashboard/general/services" class="mx-6 md:mx-0 cursor-pointer basis-full md:flex-1 flex flex-col gap-1 p-5 shadow-lg bg-white">
            <div class="flex flex-row gap-3 align-middle content-center">
                <i class="rounded-full text-indigo-700 bg-indigo-500/[0.2] p-4 pi pi-thumbs-up"></i>
                <span class="mt-1 text-4xl font-medium">{{ summary?.services_count }}</span>
            </div>
            <div class="w-full text-left px-2">
                <span class="w-full block text-lg text-center text-slate-400">Servicio(s) en stock</span>
            </div>
        </nuxt-link>

        <nuxt-link to="/dashboard/general/orders" class="mx-6 md:mx-0 cursor-pointer basis-full md:flex-1 flex flex-col gap-1 p-5 shadow-lg bg-white">
            <div class="flex flex-row gap-3 align-middle content-center">
                <i class="rounded-full text-indigo-700 bg-indigo-500/[0.2] p-4 pi pi-shopping-cart"></i>
                <span class="mt-1 text-4xl font-medium">{{ summary?.orders_count }}</span>
            </div>
            <div class="w-full text-left px-2">
                <span class="w-full block text-lg text-center text-slate-400">Pedidos realizados</span>
            </div>
        </nuxt-link >

        <nuxt-link to="/dashboard/general/comments" class="mx-6 md:mx-0 cursor-pointer basis-full md:flex-1 flex flex-col gap-1 p-5 shadow-lg bg-white">
            <div class="flex flex-row gap-3 align-middle content-center">
                <i class="rounded-full text-indigo-700 bg-indigo-500/[0.2] p-4 pi pi-comments"></i>
                <span class="mt-1 text-4xl font-medium">{{ summary?.comments_count }}</span>
            </div>
            <div class="w-full text-left px-2">
                <span class="w-full block text-lg text-center text-slate-400">Comentarios realizados </span>
            </div>
        </nuxt-link >

        <div class="mx-6 md:mx-0 shadow-lg bg-white basis-full mt-4 p-4">
            <span class="text-2xl font-medium">Pedidos Realizados</span>
            <Chart class="mt-2" type="bar" :data="chartData" :options="chartOptions" />
        </div>

        <!-- md:basis-[48%]-->
        <div class="mx-6 md:mx-0 shadow-lg bg-white basis-full mt-4 p-4">
            <span class="text-2xl font-medium">Top 10 productos</span>
            <Chart class="mt-2" type="pie" :data="chartData2" :options="chartOptions2" />
        </div>

        <!--<div class="mx-6 md:mx-0 shadow-lg bg-white basis-full md:basis-[48%] mt-4 p-4">
            <span class="text-2xl font-medium">Top 10 servicios</span>
            <Chart class="mt-2" type="pie" :data="chartData3" :options="chartOptions" />
        </div>-->
    </div>

    <div class="mt-4 flex flex-wrap flex-row gap-10" v-else>
        <nuxt-link to="/dashboard/general/clients" class="mx-6 md:mx-0 cursor-pointer basis-full md:flex-1 flex flex-col gap-1 p-5 shadow-lg bg-white">
            <div class="flex flex-row gap-3 align-middle content-center">
                <i class="rounded-full text-indigo-700 bg-indigo-500/[0.2] p-4 pi pi-users"></i>
                <span class="mt-1 text-4xl font-medium">{{ summary?.clients_count }}</span>
            </div>
            <div class="w-full text-left px-2">
                <span class="text-lg text-slate-400">Clientes</span>
            </div>
        </nuxt-link>

        <nuxt-link to="/dashboard/general/providers" class="mx-6 md:mx-0 cursor-pointer basis-full md:flex-1 flex flex-col gap-1 p-5 shadow-lg bg-white">
            <div class="flex flex-row gap-3 align-middle content-center">
                <i class="rounded-full text-indigo-700 bg-indigo-500/[0.2] p-4 pi pi-truck"></i>
                <span class="mt-1 text-4xl font-medium">{{ summary?.providers_count }}</span>
            </div>
            <div class="w-full text-left px-2">
                <span class="text-lg text-slate-400">Proveedores</span>
            </div>
        </nuxt-link>

        <nuxt-link to="/dashboard/general/payments" class="mx-6 md:mx-0 cursor-pointer basis-full md:flex-1 flex flex-col gap-1 p-5 shadow-lg bg-white">
            <div class="flex flex-row gap-3 align-middle content-center">
                <i class="rounded-full text-indigo-700 bg-indigo-500/[0.2] p-4 pi pi-credit-card"></i>
                <span class="mt-1 text-4xl font-medium">{{ summary?.payments_count }}</span>
            </div>
            <div class="w-full text-left px-2">
                <span class="text-lg text-slate-400">Pagos Realizados</span>
            </div>
        </nuxt-link>

        <div class="mx-6 md:mx-0 shadow-lg bg-white basis-full mt-4 p-4">
            <span class="text-2xl font-medium">Historial Pagos Mensual</span>
            <Chart class="mt-2" type="bar" :data="chartData4" :options="chartOptions3" />
        </div>

    </div>
</template>

<script lang="ts" setup>
    import {ref} from 'vue';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import { Globalization } from '~/helpers/globalization';
    
    // Meta configuration
    const authStore= useAuthStore();
    const {user}=storeToRefs(authStore);

    /********************* 
    | DATA
    **********************/
    const summary=ref(); 
    const chartData = ref();
    const chartOptions = ref();
    const chartOptions2 = ref();
    const chartOptions3 = ref();

    const chartData2 = ref();
    const chartData3 = ref();

    //ADMIN
    const chartData4 = ref();

    /********************* 
    | METHODS
    **********************/
    const setBarChartOptions = () => {
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--p-text-color');
        const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color');
        const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

        return {
            plugins: {
                legend: {
                    labels: {
                        color: textColor
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: textColorSecondary
                    },
                    grid: {
                        color: surfaceBorder
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: textColorSecondary
                    },
                    grid: {
                        color: surfaceBorder
                    }
                }
            }
        };
    };
    const setBarChartOptions2 = () => {
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--p-text-color');
        const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color');
        const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

        return {
            plugins: {
                legend: {
                    labels: {
                        color: textColor
                    }
                },
                tooltip:{
                    callbacks: {
                        label: function (tooltipItem:any, data:any) {
                            var v = tooltipItem.formattedValue.replaceAll(',', '');
                            return Globalization.currencyFormat.format(v);
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: textColorSecondary
                    },
                    grid: {
                        color: surfaceBorder
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: textColorSecondary,
                        callback: function (value:number) {
                            return Globalization.currencyFormat.format(value)
                        }
                    },
                    grid: {
                        color: surfaceBorder
                    }
                }
            }
        };
    };

    const setPieChartOptions = () => {
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--p-text-color');

        return {
            plugins: {
                legend: {
                    labels: {
                        usePointStyle: true,
                        color: textColor
                    }
                }
            }
        };
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(async() => {
        chartOptions.value = setBarChartOptions();
        chartOptions2.value=setPieChartOptions();
        chartOptions3.value=setBarChartOptions2();

        summary.value=await fetchWrapper.get('/summary/info');
        if (user.value?.is_provider){
            chartData.value = summary.value.summary_sales;
            chartData2.value = summary.value.summary_top_10_products;
            chartData3.value = summary.value.summary_top_10_services;
        }else{
            chartData4.value = summary.value.summary_payment_history;
        }
    });

</script>