<template>
    <Dialog class="w-[96%] md:w-[38rem]" :draggable="false" v-model:visible="showPaymentForm" modal :closable="false" :dismissable-mask="true">
        <span class="text-slate-700 font-semibold text-[20px] m-0 md:m-2">Nueva Compra</span>
        <div class="flex flex-col">
            <div v-for="(item, index) in products" :key="index">
                <div class="flex flex-row p-5 border-t border-surface-200 gap-4 my-2 h-36 cursor-pointer" :class="item.selected?'selected-item':''" @click="selectMainProduct(index)">
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

                        <div v-if="item.price" class="flex-1 flex flex-row items-end gap-2">
                            <div class="flex flex-col md:flex-row gap-1 md:gap-5">
                                <span class="text-slate-900 flex-auto text-2xl font-semibold">{{Globalization.currencyFormat.format(item.price)}}</span>
                                <span class="text-right flex-auto pt-[0.2rem] text-lg font-normal text-slate-500 line-through">{{ Globalization.currencyFormat.format(item.reference_price) }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="productOffers.length > 0" class="flex flex-col mt-8">
            <span class="text-slate-700 font-semibold text-lg m-2">Tal vez te pueda interesar:</span>
            <div v-for="(item, index) in productOffers" :key="index">
                <div class="flex flex-row p-5 gap-4 border-t border-surface-200 my-4 h-36 cursor-pointer" @click="selectOfferProduct(index)" :class="item.selected?'selected-item':''">
                    <div class="w-[6.3rem]">
                        <img class="block mx-auto rounded w-full h-full" :src="item.image" :alt="item.title" />
                        <span v-if="item.discount > 0" class="block relative top-[-6.5rem] left-0 rounded-md px-2 py-1 bg-[#D4AF37] text-white text-xs">
                            {{item.discount}}% de dsct
                        </span>
                    </div>

                    <div class="flex-1 flex flex-row justify-between items-center gap-2">
                        <div class="basis-3/5">
                            <span class="inline-block text-[18px] font-medium text-slate-900">{{ item.title}}</span>
                            <span v-if="item.header_tag" class="inline-block rounded-md px-2 py-1 bg-[#D4AF37] text-white text-xs ml-2">
                                {{ item.header_tag }}
                            </span>
                        </div>

                        <div class="flex-1 flex flex-row items-end gap-2">
                            <div class="flex flex-col md:flex-row gap-1 md:gap-5">
                                <span class="text-slate-900 flex-auto text-lg font-semibold">{{Globalization.currencyFormat.format(item.price)}}</span>
                                <span class="text-right flex-auto pt-[0.2rem] text-base font-normal text-slate-500 line-through">{{ Globalization.currencyFormat.format(item.reference_price) }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="totals.totalAmount" class="pb-8 bg-[#EBEBEB] rounded-2xl mb-4 p-4 flex flex-col">
            <div class="flex flex-row">
                <span class="basis-[80%] mx-2 my-1 font-medium text-slate-900 text-[16px]">Subtotal:</span>
                <span class="mx-2 my-1 text-right font-medium text-slate-900 text-[16px]">{{ Globalization.currencyFormat.format(totals.totalAmount) }}</span>
            </div>

            <div v-if="totals.totalDiscount > 0" class="flex flex-row">
                <span class="basis-[80%] mx-2 my-1 font-medium text-slate-900 text-[16px]">Descuentos:</span>
                <span class="mx-2 my-1 text-right  font-medium text-slate-900 text-[16px]">-{{ Globalization.currencyFormat.format(totals.totalDiscount) }}</span>
            </div>

            <span class="h-[0.5px] bg-gray-600 w-full my-2"></span>

            <div class="flex flex-row bg-[#FFCE4B] h-11 text-[15px] m-3 rounded-2xl">
                <span class="basis-[85%] mt-3 mx-2 font-medium text-slate-900 text-[16px]">Total:</span>
                <span class="mt-3 mx-2 text-right  font-medium text-slate-900 text-[16px]">{{ Globalization.currencyFormat.format(totals.total) }}</span>
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

        <form @submit.prevent="doOrder" class="flex flex-col mt-8">
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
</template>

<script lang="ts" setup>
    import {ref, type UnwrapRef} from 'vue';

    import { minLength, required, email } from '@vuelidate/validators';
    import { useListen } from '~/composables/useMitt';
    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import type { OrderForm } from '~/types/payment';

    import { useMediaQuery } from '@vueuse/core';
    import type { CartItem, SelectOption, SmallItem } from '~/types';
    import type { ProductOfferForm } from '~/types/dashboard/products';
    import { Globalization } from '~/helpers/globalization';
    import useVuelidate from '@vuelidate/core';
    import type { ContactForm2 } from '~/types/dashboard/profile/contact-data';

    // Meta configuration
    useListen('modal:payment-form', async(message:any) => {
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
        productOffers.value=[];
        showPaymentForm.value=true;
        const params=new URLSearchParams();
        params.append('item_id', message['item_id']);

        productOffers.value=await fetchWrapper.get('/products/public-offers?'+params);
        productOffers.value.forEach((offer)=>{
            offer.selected=false;
        });

        orderForm.provider_id=parseInt(message['provider_id']);
        const params2 = new URLSearchParams();
        params2.append('provider_id', orderForm.provider_id.toString());
        providerInfo.value = await fetchWrapper.get('/globals/provider-info?'+params2);
        
        provinciesData.value=await fetchWrapper.get('/globals/provinces');
    });

    const telRegex = /^\+54\s?9\s?\d{2,4}\s?\d{2,4}[-\s]?\d{3,4}$/
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

    const props=defineProps<{ readonly items: CartItem[] }>();
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
    /********************* 
    | DATA
    **********************/
    const isMobile = useMediaQuery('(max-width: 600px)');
    const lastIndex=ref<number>(0);
    const loadingOrder=ref<boolean>(false);
    const showModalEndOrder = ref<boolean>(false);
    const order_number = ref<string>('');

    const showPaymentForm = ref<boolean>(false);
    const products=ref<CartItem[]>([]);
    const productOffers=ref<ProductOfferForm[]>([]);
    const providerInfo = ref<ContactForm2>();
    const provinciesData=ref<SelectOption[]>([]);
    const localitiesData=ref<SelectOption[]>([]);

    const totals = computed(() => {
        let totalAmount = 0;
        let totalDiscount=0;
        
        if((products.value[0] && products.value[0].selected)){
            products.value.forEach(({ amount, reference_price, price }) => {
                totalAmount+=(amount * reference_price);
                totalDiscount+=((amount * reference_price) - (amount * price));
            });
        }else{
            productOffers.value.forEach(({ price, reference_price, selected}) => {
                if(selected){
                    totalAmount+=(reference_price);
                    totalDiscount+=((reference_price) - (price));
                }
            });
        }
        
        let total=totalAmount - totalDiscount;
        return { totalAmount, totalDiscount, total };
    });

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

    /********************* 
    | METHODS
    **********************/
    //
    const selectMainProduct=(index:number)=>{
        products.value[index].selected=true;
        productOffers.value.forEach((offer) => {
            offer.selected=false;
        });
    };

    const selectOfferProduct=(index:number)=>{
        for (var x = 0; x < products.value.length; x++){
            products.value[x].selected=false;
        }

        for (var x = 0; x < productOffers.value.length; x++){
            if(x === index){
                productOffers.value[x].selected=true;
                continue;
            }
            productOffers.value[x].selected=false;
        }
    
        if(lastIndex.value !== index){
            lastIndex.value=index;
        }
    };

    const filterLocalities = async() => {
        const params=new URLSearchParams();
        params.append('province_id', orderForm.province);

        localitiesData.value=await fetchWrapper.get('/globals/localities?'+params);
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
        if((products.value[0] && products.value[0].selected)){
            products.value.forEach(({title, price, amount}) => {
                data.push({
                    title: title, 
                    amount: amount,
                    price: price
                });
            });
        }else{
            productOffers.value.forEach(({title, price, amount, selected}) => {
                if(selected){
                    data.push({
                        title: title, 
                        amount: amount,
                        price: price
                    });
                }
            });
        }

        for(let x=0; x<data.length;x++){
            var product=data[x];
            message+=`
✅ *${product.title}* 
Cantidad: ${product.amount}
${product.price ?  "Precio:"+Globalization.currencyFormat.format(product.price):'' }
------------------------------------>
`;
        };

            if (products.value[0].price){
            message+=`
*Sub-Total: ${Globalization.currencyFormat.format(totals.value.totalAmount)}*
*Descuentos: ${Globalization.currencyFormat.format(totals.value.totalDiscount)}*
*Total: ${Globalization.currencyFormat.format(totals.value.total)}*
`;
        }

        
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

            if((products.value[0] && products.value[0].selected)){
                products.value.forEach(({id, amount}) => {
                    orderForm.details.push({
                        id: id,
                        amount: amount,
                        options: []
                    });
                });
                orderForm.source_detail='products';
            }else{
                productOffers.value.forEach(({id, amount, selected}) => {
                    if(selected){
                        orderForm.details.push({
                            id: id,
                            amount: amount
                        });
                    }
                });
                orderForm.source_detail='offers';
            }
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
        products.value=props.items;
    });

</script>

<style>
.selected-item{
    border: 4px solid #0074BF!important;
    background-color: #D9EBF6;
    border-radius: 10px;
}
</style>