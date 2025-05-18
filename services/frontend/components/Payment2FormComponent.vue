<template>
    <Dialog class="w-[96%] md:w-[38rem]" :draggable="false" v-model:visible="showPaymentForm" modal :closable="false" :dismissable-mask="true">
        <div class="flex flex-col">
            <div v-for="(item, index) in services" :key="index">
                <div class="flex flex-row p-5 border-t border-surface-200 gap-4 my-2 h-36 cursor-pointer selected-item">
                    <div class="hidden md:block w-28">
                        <img class="mx-auto rounded w-full h-full" :src="item.img" :alt="item.title" />
                        <span v-if="item.discount > 0" class="block relative top-[-6.5rem] left-0 rounded-md px-2 py-1 bg-[#D4AF37] text-white text-xs">
                            {{item.discount}}% descuento
                        </span>
                    </div>

                    <div class="flex-1 flex flex-row justify-between items-center gap-0 md:gap-3">
                        <div class="basis-3/5">
                            <span class="inline-block text-[18px] font-medium text-slate-900">{{ item.title}}</span>
                            <span v-if="item.header_tag" class="inline-block rounded-md px-2 py-1 bg-[#D4AF37] text-white text-xs ml-0 md:ml-2">
                                {{ item.header_tag }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="flex flex-col mt-8">
            <span class="text-slate-700 font-semibold text-lg m-2">Datos del Proveedor:</span>
            <div class="p-2 flex flex-row gap-4">
                <span class="basis-5/12 font-medium"><i class="pi pi-facebook"></i> Facebook:</span>
                <a class="text-blue-800 flex-1 text-right" :href="providerInfo?.url_facebook">{{ providerInfo?.user__username }}</a>
            </div>
            <div class="p-2 flex flex-row gap-4">
                <span class="basis-5/12 font-medium"><i class="pi pi-instagram"></i> Instagram:</span>
                <a class="text-blue-800 flex-1 text-right" :href="providerInfo?.url_instagram">{{ providerInfo?.user__username }}</a>
            </div>
            <div class="p-2 flex flex-row gap-4">
                <span class="basis-5/12 font-medium"><i class="pi pi-envelope"></i> Correo:</span>
                <a class="text-blue-800 flex-1 text-right" :href="'mailto:'+providerInfo?.email">{{ providerInfo?.email }}</a>
            </div>
            <div v-if="providerInfo?.whatsapp_telephone" class="p-2 flex flex-row gap-4">
                <span class="basis-5/12 font-medium"><i class="pi pi-whatsapp"></i> WhatsApp:</span>
                <a class="text-blue-800 flex-1 text-right" :href="isMobile? `https://api.whatsapp.com/send/?phone=${providerInfo?.whatsapp_telephone}&type=phone_number&text=HOLA!&app_absent=0`:`https://web.whatsapp.com/send/?phone=${providerInfo?.whatsapp_telephone}&&text=HOLA!`">{{ providerInfo?.whatsapp_telephone }}</a>
            </div>
            <div class="p-2 flex flex-row gap-4">
                <span class="basis-5/12 font-medium"><i class="pi pi-phone"></i> Teléfono:</span>
                <a class="text-blue-800 flex-1 text-right" :href="'tel:'+providerInfo?.telephone">{{ providerInfo?.telephone }}</a>
            </div>

            <div class="p-2 flex flex-row gap-4">
                <span class="basis-5/12 font-medium"><i class="pi pi-map-marker"></i> Dirección:</span>
                <span class="text-blue-800 flex-1 text-right">{{ providerInfo?.address }}</span>
            </div>
        </div>

        <form v-if="!extraInfo?.with_reservation" @submit.prevent="doOrder" class="flex flex-col mt-8">
            <span class="text-slate-700 font-semibold text-lg m-2">Ingrese sus datos para generar el pedido:</span>
            
            <div class="p-2 flex flex-row gap-1">
                <label for="fullname" class="w-24 font-medium">Nombres y Apellidos:</label>
                
                <div class="flex-1 flex flex-col">
                    <IconField>
                        <InputIcon class="pi pi-user" />
                        <InputText 
                        v-model:model-value="orderForm.fullname"
                        id="fullname" 
                        :class="{'!border !border-red-500': $orderValidator.fullname.$invalid && $orderValidator.fullname.$dirty}"
                        @input="$orderValidator.fullname.$touch()" 
                        aria-describedby="fullname-help"
                        
                        placeholder="Nombres y Apellidos" 
                        fluid
                        />
                    </IconField>
                    
                    <small id="fullname-help" v-if="$orderValidator.fullname.required.$invalid && $orderValidator.fullname.$dirty" class="text-red-600">Nombres requeridos.</small>
                    <small id="fullname-help" v-else-if="$orderValidator.fullname.minLength.$invalid && $orderValidator.fullname.$dirty" class="text-red-600">Nombre demasiado corto.</small>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="telephone" class="w-24 font-medium">Teléfono:</label>
                <div class="flex-1 flex flex-col">
                    <IconField>
                        <InputIcon class="pi pi-phone" />
                 
                        <InputText
                        v-model:model-value="orderForm.telephone"
                        id="telephone" 
                        :class="{'!border !border-red-500': $orderValidator.telephone.$invalid && $orderValidator.telephone.$dirty}"
                        @input="$orderValidator.telephone.$touch()" 
                        aria-describedby="telephone-help"

                        placeholder="Teléfono"
                        fluid
                        />
                    </IconField>
                    <small id="telephone-help" v-if="$orderValidator.telephone.required.$invalid && $orderValidator.telephone.$dirty" class="text-red-600">Teléfono requerido.</small>
                    <small id="telephone-help" v-else-if="$orderValidator.telephone.isTel.$invalid && $orderValidator.telephone.$dirty" class="text-red-600">Teléfono inválido.</small>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="email" class="w-24 font-medium">Email:</label>
                <div class="flex-1 flex flex-col">
                    <IconField>
                        <InputIcon class="pi pi-envelope" />
                 
                        <InputText
                        v-model:model-value="orderForm.email"
                        id="email" 
                        :class="{'!border !border-red-500': $orderValidator.email.$invalid && $orderValidator.email.$dirty}"
                        @input="$orderValidator.email.$touch()" 
                        aria-describedby="email-help"

                        placeholder="Email"
                        fluid
                        />
                    </IconField>
                    
                    <small id="email-help" v-if="$orderValidator.email.email.$invalid && $orderValidator.email.$dirty" class="text-red-600">Email inválido.</small>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="province" class="w-24 font-medium">Provincia:</label>
                
                <div class="flex-1 flex flex-col">
                    <Select 
                    @change="filterLocalities"
                    option-value="value"
                    option-label="label"
                    :options="provinciesData"
                    v-model:model-value="orderForm.province"
                    id="province" 
                    :class="{'!border !border-red-500': $orderValidator.province.$invalid && $orderValidator.province.$dirty}"
                    @input="$orderValidator.province.$touch()" 
                    aria-describedby="province-help"
                        
                    placeholder="Provincia" 
                    fluid
                    >
                        <template #empty>
                            <span class="mt-4 block !text-4xl text-gray-500/[0.7] pi pi-folder-open w-full text-center"></span>
                            <span class="mb-4 block text-lg text-gray-400/[0.8] w-full text-center">No hay provincias para mostrar</span>
                        </template>
                    </Select>
                    
                    <small id="province-help" v-if="$orderValidator.province.required.$invalid && $orderValidator.province.$dirty" class="text-red-600">Provincia Requerida.</small>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="locality" class="w-24 font-medium">Localidad:</label>
                
                <div class="flex-1 flex flex-col">
                    <Select 
                    option-value="value"
                    option-label="label"
                    :options="localitiesData"
                    v-model:model-value="orderForm.locality"
                    id="locality" 
                    :class="{'!border !border-red-500': $orderValidator.locality.$invalid && $orderValidator.locality.$dirty}"
                    @input="$orderValidator.locality.$touch()" 
                    aria-describedby="locality-help"
                        
                    placeholder="Localidad" 
                    fluid
                    >
                        <template #empty>
                            <span class="mt-4 block !text-4xl text-gray-500/[0.7] pi pi-folder-open w-full text-center"></span>
                            <span class="mb-4 block text-lg text-gray-400/[0.8] w-full text-center">No hay localidades para mostrar</span>
                        </template>
                    </Select>
                    
                    <small id="locality-help" v-if="$orderValidator.locality.required.$invalid && $orderValidator.locality.$dirty" class="text-red-600">Localidad Requerida.</small>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="city" class="w-24 font-medium break-words">Ciudad/Pueblo:</label>
                
                <div class="flex-1 flex flex-col">
                    <IconField>
                        <InputIcon class="pi pi-map-marker" />
                        <InputText 
                        v-model:model-value="orderForm.city"
                        id="city" 
                        :class="{'!border !border-red-500': $orderValidator.city.$invalid && $orderValidator.city.$dirty}"
                        @input="$orderValidator.city.$touch()" 
                        aria-describedby="city-help"
                        
                        placeholder="Ciudad/Pueblo" 
                        fluid
                        />
                    </IconField>
                    
                    <small id="city-help" v-if="$orderValidator.city.required.$invalid && $orderValidator.city.$dirty" class="text-red-600">Ciudad requerida.</small>
                    <small id="city-help" v-else-if="$orderValidator.city.minLength.$invalid && $orderValidator.city.$dirty" class="text-red-600">Dirección demasiada corta.</small>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="address" class="w-24 font-medium">Dirección:</label>
                
                <div class="flex-1 flex flex-col">
                    <IconField>
                        <InputIcon class="pi pi-map-marker" />
                        <InputText 
                        v-model:model-value="orderForm.address"
                        id="address" 
                        :class="{'!border !border-red-500': $orderValidator.address.$invalid && $orderValidator.address.$dirty}"
                        @input="$orderValidator.address.$touch()" 
                        aria-describedby="address-help"
                        
                        placeholder="Dirección" 
                        fluid
                        />
                    </IconField>
                    
                    <small id="address-help" v-if="$orderValidator.address.required.$invalid && $orderValidator.address.$dirty" class="text-red-600">Dirección requerida.</small>
                    <small id="address-help" v-else-if="$orderValidator.address.minLength.$invalid && $orderValidator.address.$dirty" class="text-red-600">Dirección demasiada corta.</small>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="reference" class="w-24 font-medium">Referencia:</label>
                
                <div class="flex-1 flex flex-col">
                    <IconField>
                        <InputIcon class="pi pi-map-marker" />
                        <InputText 
                        v-model:model-value="orderForm.reference"
                        id="reference" 
                        :class="{'!border !border-red-500': $orderValidator.reference.$invalid && $orderValidator.reference.$dirty}"
                        @input="$orderValidator.reference.$touch()" 
                        aria-describedby="reference-help"

                        placeholder="Referencia" 
                        fluid
                        />
                    </IconField>
                    
                    <small id="reference-help" v-if="$orderValidator.reference.required.$invalid && $orderValidator.reference.$dirty" class="text-red-600">Referencia requerida.</small>
                    <small id="reference-help" v-else-if="$orderValidator.reference.minLength.$invalid && $orderValidator.reference.$dirty" class="text-red-600">Referencia demasiada corta.</small>
                </div>
            </div>

            <Button :loading="loadingOrder" :disabled="loadingOrder || $orderValidator.fullname.$invalid || $orderValidator.telephone.$invalid || $orderValidator.province.$invalid || $orderValidator.locality.$invalid || $orderValidator.city.$invalid || $orderValidator.address.$invalid || $orderValidator.reference.$invalid" type="submit" icon="pi pi-whatsapp" size="large" class="mt-10" label="Realizar Pedido" fluid />
        </form>

        <div v-else class="flex flex-col mt-8">
            <span class="text-slate-700 font-semibold text-lg m-2">Horarios de Atención:</span>
            <div class="flex flex-col" v-for="(item, index) in extraInfo.opening_hours">
                <div v-if="item.start_time !== null && item.end_time !== null" class="p-2 flex flex-row gap-4">
                    <span class="basis-5/12 md:basis-[70%] font-medium">{{ daysOfWeek2[item.day]}}: </span>
                    <span class="text-slate-700 flex-1 text-left">{{formatTo12Hour(item.start_time)}} - {{formatTo12Hour(item.end_time)}}</span>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-4">
                <span class="basis-9/12 font-medium">Duración Aprox Sesión:</span>
                <span class="text-slate-700 flex-1 text-right">{{ extraInfo.approximate_duration}} min</span>
            </div>
        </div>

        <form v-if="extraInfo?.with_reservation" @submit.prevent="doReservation" class="flex flex-col mt-8">
            <span class="text-slate-700 font-semibold text-lg m-2 mt-8">Realizar Reservación:</span>

            <div class="p-2 flex flex-row gap-1">
                <label for="fullname" class="w-24 font-medium">Nombres y Apellidos:</label>
                
                <div class="flex-1 flex flex-col">
                    <IconField>
                        <InputIcon class="pi pi-user" />
                        <InputText 
                        v-model:model-value="reservationForm.fullname"
                        id="fullname" 
                        :class="{'!border !border-red-500': $reservationValidator.fullname.$invalid && $reservationValidator.fullname.$dirty}"
                        @input="$reservationValidator.fullname.$touch()" 
                        aria-describedby="fullname-help"
                        
                        placeholder="Nombres y Apellidos" 
                        fluid
                        />
                    </IconField>
                    
                    <small id="fullname-help" v-if="$reservationValidator.fullname.required.$invalid && $reservationValidator.fullname.$dirty" class="text-red-600">Nombres requeridos.</small>
                    <small id="fullname-help" v-else-if="$reservationValidator.fullname.minLength.$invalid && $reservationValidator.fullname.$dirty" class="text-red-600">Nombre demasiado corto.</small>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="telephone" class="w-24 font-medium">Teléfono:</label>
                <div class="flex-1 flex flex-col">
                    <IconField>
                        <InputIcon class="pi pi-phone" />
                 
                        <InputText
                        v-model:model-value="reservationForm.telephone"
                        id="telephone" 
                        :class="{'!border !border-red-500': $reservationValidator.telephone.$invalid && $reservationValidator.telephone.$dirty}"
                        @input="$reservationValidator.telephone.$touch()" 
                        aria-describedby="telephone-help"

                        placeholder="Teléfono"
                        fluid
                        />
                    </IconField>
                    <small id="telephone-help" v-if="$reservationValidator.telephone.required.$invalid && $reservationValidator.telephone.$dirty" class="text-red-600">Teléfono requerido.</small>
                    <small id="telephone-help" v-else-if="$reservationValidator.telephone.isTel.$invalid && $reservationValidator.telephone.$dirty" class="text-red-600">Teléfono inválido.</small>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="email" class="w-24 font-medium">Email:</label>
                <div class="flex-1 flex flex-col">
                    <IconField>
                        <InputIcon class="pi pi-envelope" />
                 
                        <InputText
                        v-model:model-value="reservationForm.email"
                        id="email" 
                        :class="{'!border !border-red-500': $reservationValidator.email.$invalid && $reservationValidator.email.$dirty}"
                        @input="$reservationValidator.email.$touch()" 
                        aria-describedby="email-help"

                        placeholder="Email"
                        fluid
                        />
                    </IconField>
                    
                    <small id="email-help" v-if="$reservationValidator.email.email.$invalid && $reservationValidator.email.$dirty" class="text-red-600">Email inválido.</small>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="subservices" class="w-24 font-medium">Servicios:</label>
                
                <div class="flex-1 flex flex-col">
                    <MultiSelect 
                    v-model:model-value="reservationForm.subservices"
                    id="subservices" 
                    :class="{'!border !border-red-500': $reservationValidator.subservices.$invalid && $reservationValidator.subservices.$dirty}"
                    @blur="$reservationValidator.subservices.$touch()" 
                    aria-describedby="subservices-help"
                    display="chip"
                    :options="subservices"
                    option-label="description"
                    option-value="description"
                    
                    :max-selected-labels="3"
                    placeholder="Sub Servicios" 
                    fluid
                    >
                        <template #empty>
                            <span class="block w-full text-lg text-center py-4 text-gray-500/[0.5]">No hay servicios para mostrar</span>
                        </template>
                    </MultiSelect>
                    
                    <small id="subservices-help" v-if="$reservationValidator.subservices.required.$invalid && $reservationValidator.subservices.$dirty" class="text-red-600">Sub Servicios requeridos.</small>
                </div>
            </div>
            
            <div class="p-2 flex flex-row gap-1">
                <label for="telephone" class="w-24 font-medium">Comentario:</label>
                <div class="flex-1 flex flex-col">
                    <IconField>
                        <InputIcon class="pi pi-pencil" />
                        <InputText
                        v-model:model-value="reservationForm.notes"
                        placeholder="Comentario"
                        fluid
                        />
                    </IconField>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="date" class="w-24 font-medium">Fecha:</label>
                    
                <div class="flex-1 flex flex-col">
                    <DatePicker  
                    show-icon
                    @date-select="setTimeRange"
                    :disabled-days="disabledDays"
                    :min-date="minDate" 
                    date-format="dd/mm/yy"  
                    v-model:model-value="reservationForm.date"
                    id="date" 
                    :class="{'!border !border-red-500': $reservationValidator.date.$invalid && $reservationValidator.date.$dirty}"
                    @input="$reservationValidator.date.$touch()" 
                    aria-describedby="date-help"
                    placeholder="Seleccionar Fecha" 
                    />
                    <small id="date-help" v-if="$reservationValidator.date.required.$invalid && $reservationValidator.date.$dirty" class="text-red-600">Fecha de Reserva Requerido.</small>
                </div>
            </div>

            <div class="p-2 flex flex-row gap-1">
                <label for="time" class="w-24 font-medium">Hora:</label>
                    
                <div class="flex-1 flex flex-col">
                    <DatePicker  
                    :disabled="reservationForm.date === null"
                    show-icon
                    @blur="validateTime"
                    :step-minute="extraInfo.approximate_duration"
                    :min-date="minTime"
                    :max-date="maxTime"
                    time-only
                    hour-format="12"         
                    v-model:model-value="reservationForm.time"
                    id="time" 
                    :class="{'!border !border-red-500': $reservationValidator.time.$invalid && $reservationValidator.time.$dirty}"
                    @input="$reservationValidator.time.$touch()" 
                    aria-describedby="time-help"
                    placeholder="Seleccionar Hora" 
                    />
                    <small id="time-help" v-if="$reservationValidator.time.required.$invalid && $reservationValidator.time.$dirty" class="text-red-600">Hora de Reserva Requerida.</small>
                </div>
            </div>

            <Button :loading="loadingReservation" :disabled="loadingReservation || $reservationValidator.date.$invalid || $reservationValidator.subservices.$invalid || $reservationValidator.time.$invalid || $reservationValidator.fullname.$invalid || $reservationValidator.telephone.$invalid || $reservationValidator.email.$invalid" type="submit" icon="pi pi-calendar-clock" size="large" class="mt-10" label="Reservar" fluid />

        </form>
    </Dialog>

    <Dialog class="w-[96%] md:w-[38rem]" v-model:visible="showModalEndOrder" :draggable="false" modal :closable="false" :dismissable-mask="true">
        <div class="flex flex-col" v-if="order_number.trim() !== ''">
            <i class="bg-green-500  p-6 rounded-full mx-auto text-center text-white text-5xl pi pi-check"></i>
            <span class="mt-4 w-full text-center text-2xl">¡¡Compra Exitosa!!</span>
            <span class="mt-4 w-full text-center text-lg">La compra generó el Nº Orden '{{order_number}}'.</span>

            <span class="mt-4 w-full text-center text-base">
                Puede consultar el estado de su orden en  <nuxt-link target="_blank" :to="'/store/orders/'+order_number">/store/orders/{{ order_number }}</nuxt-link>
            </span>

            <strong class="mt-4 w-full text-center text-base">
                Importante: Conservar el Nº de &Oacute;rden: {{ order_number }}
            </strong>

            <div class="flex gap-4 mt-10 mb-5 mx-0 md:mx-8">
                <Button severity="success" @click="doExport" icon="pi pi-download" :size="isMobile?'small':'large'" label="Descargar PDF" fluid />
                <Button severity="secondary" @click="doConfirmPayment" icon="pi pi-check" size="large" label="Confirmar" fluid />
            </div>
        </div>

        <div class="flex flex-col" v-else>
            <i class="bg-red-500  p-6 rounded-full mx-auto text-center text-white text-5xl pi pi-times"></i>
            <span class="mt-4 w-full text-center text-2xl">Compra Fallida</span>
            <span class="mt-4 w-full text-center text-lg">Por favor verifique y modifique la siguiente información antes de volver a enviarla.</span>

            <div class="mx-8 mt-7 flex flex-col gap-4">
                <span class="font-bold text-lg">Posibles Causas:</span>
                <span><i class="pi pi-times-circle !text-lg text-red-500"></i> La informaci&oacute;n es err&oacute;nea.</span>
                <span><i class="pi pi-times-circle !text-lg text-red-500"></i> Error Interno del servidor.</span>
            </div>

            <div class="flex gap-4 mt-10 mb-5 mx-8">
                <Button severity="danger" @click="()=>{showModalEndOrder = false;}" size="large" label="Cancelar" fluid />
            </div>
        </div>
    </Dialog>

    <Toast />
</template>

<script lang="ts" setup>
    import {ref, type UnwrapRef} from 'vue';
    import { useToast } from "primevue/usetoast";

    import { minLength, required, email } from '@vuelidate/validators';
    import { useListen } from '~/composables/useMitt';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import type { OrderForm } from '~/types/payment';

    import { useMediaQuery } from '@vueuse/core';
    import type { CartItem, SelectOption, SmallItem } from '~/types';
    import useVuelidate from '@vuelidate/core';
    import type { ContactForm2 } from '~/types/dashboard/profile/contact-data';
    import type { Availability2, ExtraInfo, ReservationForm } from '~/types/dashboard/services';
    import { daysOfWeek2 } from '~/helpers/constants';

    // Meta configuration
    const toast = useToast();

    useListen('modal:payment-form2', async(message:any) => {
        service_id.value=message['item_id'];

        providerInfo.value={
            company_name: '',
            logo: '',
            telephone: '',
            address: '',
            email: '',
            url_facebook: '',
            url_instagram: '',
            whatsapp_telephone: '',
            user__username: ''
        };
        showPaymentForm.value=true;
        const params=new URLSearchParams();
        params.append('service_id', message['item_id']);
        subservices.value=await fetchWrapper.get('/services/subservices?'+params);
        extraInfo.value=await fetchWrapper.get('/services/opening-hours?'+params);
        disabledDays.value=extraInfo.value?.opening_hours && extraInfo.value.opening_hours.
                filter((value: Availability2) => {return(value.start_time === null && value.end_time === null)}).
                map((value: Availability2) => getWeekNumber(value.day)) as number[];

        orderForm.provider_id=parseInt(message['provider_id']);
        const params2 = new URLSearchParams();
        params2.append('provider_id', orderForm.provider_id.toString());
        providerInfo.value = await fetchWrapper.get('/globals/provider-info?'+params2);
        
        provinciesData.value=await fetchWrapper.get('/globals/provinces');
    });
    function formatTo12Hour(time:string) {
        if (!time) return null;

        // Crear una fecha en UTC a partir de la hora dada
        const [hours, minutes, seconds] = time.split(":");
        const date = new Date(Date.UTC(
            new Date().getUTCFullYear(),
            new Date().getUTCMonth(),
            new Date().getUTCDate(),
            parseInt(hours, 10),
            parseInt(minutes, 10),
            parseInt(seconds, 10) || 0
        ));

        // Convertir a la hora local del cliente
        const localHours = date.getHours();
        const localMinutes = date.getMinutes();

        // Formatear en 12 horas
        const period = localHours >= 12 ? 'PM' : 'AM';
        const formattedHours = localHours % 12 || 12; // Asegura que 12 se mantenga como 12
        const formattedMinutes = localMinutes.toString().padStart(2, '0');

        return `${formattedHours}:${formattedMinutes} ${period}`;
    }
    function getWeekNumber(abbreviation: string): number|null {
        const weekMap: { [key: string]: number } = {
            'SUN': 0,  // Domingo
            'MON': 1,  // Lunes
            'TUE': 2,  // Martes
            'WED': 3,  // Miércoles
            'THU': 4,  // Jueves
            'FRI': 5,  // Viernes
            'SAT': 6   // Sábado
        };
        return weekMap[abbreviation] !== undefined ? weekMap[abbreviation] : null;
    }
    function getWeekAbbreviation(weekNumber: number): string | null {
        const weekMap: { [key: string]: number } = {
            'SUN': 0,  // Domingo
            'MON': 1,  // Lunes
            'TUE': 2,  // Martes
            'WED': 3,  // Miércoles
            'THU': 4,  // Jueves
            'FRI': 5,  // Viernes
            'SAT': 6   // Sábado
        };

        const invertedMap: { [key: number]: string } = Object.fromEntries(
            Object.entries(weekMap).map(([key, value]) => [value, key])
        );
        return invertedMap[weekNumber] || null;
    }

    //const telRegex = /^\+54\s?9\s?\d{2,4}\s?\d{2,4}[-\s]?\d{3,4}$/
    const customTelValidator = (value:string) => {
        return true; // telRegex.test(value);
    };

    const orderRules = computed(() => ({
        fullname: {
            required,
            minLength: minLength(5),
        },
        telephone: {
            required,
            isTel: customTelValidator
        },
        email:{
            email: email
        },
        province: {
            required
        },
        locality: {
            required
        },
        city: {
            required,
            minLength: minLength(5),
        },
        address: {
            required,
            minLength: minLength(5),
        },
        reference: {
            required,
            minLength: minLength(5),
        },
    }));
    const reservationRules = computed(() => ({
        fullname: {
            required,
            minLength: minLength(5),
        },
        telephone: {
            required,
            isTel: customTelValidator
        },
        email:{
            email: email
        },
        subservices: {
            required
        },
        date: {
            required
        },
        time: {
            required
        }
    }));

    function resetOrderFields(){
        orderForm.fullname='';
        orderForm.email='';
        orderForm.telephone='';
        orderForm.province='';
        orderForm.locality='';
        orderForm.city='';
        orderForm.address='';
        orderForm.reference='';
        
        orderForm.details=[];
        orderForm.provider_id=-1;
        
        $orderValidator.value.$reset();
    }
    function resetReservationFields(){
        reservationForm.notes='';
        reservationForm.fullname='';
        reservationForm.date=null;
        reservationForm.email='';
        reservationForm.telephone='';
        reservationForm.time=null;
        reservationForm.subservices=[];
        
        $reservationValidator.value.$reset();
    }
    const props=defineProps<{ readonly items: CartItem[] }>();

    /********************* 
    | DATA
    **********************/
    const service_id=ref<number>(-1);
    const isMobile = useMediaQuery('(max-width: 600px)');
    const loadingOrder=ref<boolean>(false);
    const loadingReservation=ref<boolean>(false);
    const showModalEndOrder = ref<boolean>(false);
    const order_number = ref<string>('');

    const showPaymentForm = ref<boolean>(false);
    const services=ref<CartItem[]>([]);
    const providerInfo = ref<ContactForm2>();
    const provinciesData=ref<SelectOption[]>([]);
    const localitiesData=ref<SelectOption[]>([]);
    const extraInfo=ref<ExtraInfo>();
    const subservices=ref<string[]>([]);

    const disabledDays = ref<number[]>();
    const minDate = ref<Date>(new Date());
    const minTime = ref<Date>(new Date());
    const maxTime = ref<Date>(new Date());

    const orderForm:UnwrapRef<OrderForm> = reactive({
        fullname: '',
        email: '',
        telephone: '',
        province: '',
        locality: '',
        city: '',
        address: '',
        reference: '',
        source_detail: '',
        provider_id: -1,

        details: []
    });
    const $orderValidator=useVuelidate(orderRules, orderForm);

    const reservationForm:UnwrapRef<ReservationForm> = reactive({
        fullname: '',
        notes: '',
        telephone: '',
        email: '',
        service: -1,
        subservices:[],

        date: null,
        time: null
    });
    const $reservationValidator=useVuelidate(reservationRules, reservationForm);

    /********************* 
    | METHODS
    **********************/
    //
    const validateTime = () => {
        if (reservationForm.time) {
            if (reservationForm.time < minTime.value) {
                reservationForm.time= minTime.value;
            } else if (reservationForm.time > maxTime.value) {
                reservationForm.time = maxTime.value;
            }
        }
    };

    const filterLocalities = async() => {
        const params=new URLSearchParams();
        params.append('province_id', orderForm.province);

        localitiesData.value=await fetchWrapper.get('/globals/localities?'+params);
    };
    const setTimeRange = async () => {
        const currentDay = extraInfo.value?.opening_hours.find((entry) => 
            entry.day === getWeekAbbreviation(reservationForm.date?.getDay() as number)
        );

        if (!currentDay) return;

        // Convertir start_time a UTC y ajustar a la hora local
        const [startHour, startMinute] = currentDay.start_time.split(':').map(Number);
        const minTimeUTC = new Date(Date.UTC(
            new Date().getUTCFullYear(),
            new Date().getUTCMonth(),
            new Date().getUTCDate(),
            startHour,
            startMinute,
            0
        ));
        minTime.value = new Date(minTimeUTC); // Ajuste automático a la hora local

        // Convertir end_time a UTC y ajustar a la hora local
        const [endHour, endMinute] = currentDay.end_time.split(':').map(Number);
        const adjustedEndMinute = endMinute - (extraInfo.value?.approximate_duration as number);
        const maxTimeUTC = new Date(Date.UTC(
            new Date().getUTCFullYear(),
            new Date().getUTCMonth(),
            new Date().getUTCDate(),
            endHour,
            adjustedEndMinute,
            0
        ));
        maxTime.value = new Date(maxTimeUTC); // Ajuste automático a la hora local

        // Establecer la hora de inicio en reservationForm.time
        reservationForm.time = minTime.value;
    };

    //
    const doConfirmPayment = ()=>{
        showModalEndOrder.value = false;

        const params=new URLSearchParams();
        params.append('_format', 'pdf');
        params.append('order_number', order_number.value);
        const meta= import.meta.env.VITE_API_URL === undefined?'https://emprender-radix.com/api' : import.meta.env.VITE_API_URL;
        const urlExport = `${meta}/orders/export?${params}`;

        const phoneNumber = providerInfo.value?.telephone;
        var message = '¡Hola! 🌟 Estoy interesado(a) en encargar:';

        const data:SmallItem[] = [];
        services.value.forEach(({title, price, amount}) => {
            data.push({
                title: title, 
                amount: amount,
                price: price
            });
        });

        for(let x=0; x<data.length;x++){
            var product=data[x];
            message+=`
✅ *${product.title}* 
Cantidad: ${product.amount}
------------------------------------>
`;
        };

        message+=`
Nota al vendedor:
Puede consultar el pedido en *${location.protocol + '//' + location.host}/store/orders/${order_number.value}*,
adicionalmente puede descargar la constancia de compra en *${urlExport}*
`; 
        const encodedMessage = encodeURIComponent(message);
        const whatsappUrl = isMobile.value? `https://wa.me/${phoneNumber}/?text=${encodedMessage}`:`https://web.whatsapp.com/send/?phone=${phoneNumber}&text=${encodedMessage}&type=phone_number&app_absent=0`;
        window.open(whatsappUrl);
    };

    const doOrder = async() =>{
        const $valid= await $orderValidator.value.$validate();
        if ($valid){
            loadingOrder.value=true;

            services.value.forEach(({id, amount}) => {
                orderForm.details.push({
                    id: id,
                    amount: amount,
                    options: []
                });
            });
            orderForm.source_detail='products';
            
            await fetchWrapper.post("/orders/save", orderForm).then((data) => {
                showPaymentForm.value=false;
                order_number.value=data["msg"];
                loadingOrder.value=false;
                showModalEndOrder.value=true;
                resetOrderFields();

            }).catch(error =>{
                if (error.detail){
                    error=error.detail;
                }
                loadingOrder.value=false;
                showModalEndOrder.value=true;
            });
        }
    };
    const doReservation = async()=>{
        const $valid= await $reservationValidator.value.$validate();
        if ($valid){
            loadingReservation.value=true;
            reservationForm.service=service_id.value;
            
            await fetchWrapper.post("/reservations/save", reservationForm).then((msg) => {
                showPaymentForm.value=false;
                loadingReservation.value=false;
                resetReservationFields();
                toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 6000 });
            }).catch(error =>{
                toast.add({ severity: 'error', summary: 'Error', detail: 'Error al Reservar: '+JSON.stringify(error), life: 6000 });
                loadingReservation.value=false;
            });
        }
    };
    const doExport = async () => {
        const params=new URLSearchParams();
        params.append('_format', 'pdf');
        params.append('order_number', order_number.value);
        
        const meta= import.meta.env.VITE_API_URL === undefined?'https://emprender-radix.com/api' : import.meta.env.VITE_API_URL;
        const url = `${meta}/orders/export?${params}`;
        fetch(url, {
            method: 'GET'
        }).then(response => {
            if (response.ok) {
                return response.blob();
            }
            throw new Error('Network response was not ok.');
        }).then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'Pedido-'+order_number.value+'.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        }).catch(error => alert('There was a problem with the fetch operation:'+ error));
    };
    /********************* 
    | MOUNT
    **********************/
    watch(() => props.items, (newProducts) => {
        services.value=props.items;
    });

</script>

<style>
.selected-item{
    border: 4px solid #0074BF!important;
    background-color: #D9EBF6;
    border-radius: 10px;
}
</style>