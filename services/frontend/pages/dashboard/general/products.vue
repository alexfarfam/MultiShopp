<template>
    <div>
        <DataView class="!bg-transparent" :value="filteredProductData" data-key="id">
            <template #list="slotProps">
                <div class="flex flex-col gap-6">
                    <div v-for="(item, index) in slotProps.items" :key="index">
                        <div class="flex flex-row p-2 gap-2 border border-surface-200 bg-white shadow-md rounded-xl ">
                            <div class="w-18 md:w-20 relative">
                                <Image class="mt-2" :src="item.main_image" alt="Image" width="150" preview />
                            </div>
                            <div class="flex flex-col md:flex-row justify-between md:items-center flex-1 gap-6">
                                <div class="flex flex-row md:flex-col justify-between items-start gap-3">
                                    <div>
                                        <div class="flex flex-col md:flex-row gap-1 md:gap-2">
                                            <span class="text-base font-medium mt-2">{{ item.title }}</span>
                                            <span class="text-[12px] w-fit px-2 h-6 pt-1 mt-2 text-white rounded-md text-center bg-orange-500">{{ item.subcategory__title}}</span>
                                            <span v-if="item.header_tag" class="text-[12px] w-fit px-2 h-6 pt-1 mt-2 text-white rounded-md text-center bg-purple-500">{{ item.header_tag}}</span>
                                        </div>

                                        <div class="mt-4 md:mt-2 flex flex-col md:flex-row gap-1 md:gap-3">
                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Precio Ref: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ Globalization.currencyFormat.format(item.reference_price) }}</span>
                                            </div>

                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Precio Cliente: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ Globalization.currencyFormat.format(item.price) }}</span>
                                            </div>

                                            <div class="flex flex-row gap-2">
                                                <span class="font-medium text-surface-500 dark:text-surface-400 text-sm">Descuento: </span> <span class="font-normal text-surface-500 dark:text-surface-400 text-sm">{{ item.discount }}%</span>
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
                <span class="mt-4 block text-2xl text-gray-400/[0.8] w-full text-center">Sin productos para mostrar</span>
            </template>
        </DataView>
    </div>

    <Dialog dismissable-mask v-model:visible="showEditModal" modal :header="formTitle" :style="{ width: '90vw' }">
        <Accordion value="0">
            <AccordionPanel value="0">
                <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Información Principal</AccordionHeader>
                <AccordionContent>
                    <form class="p-1 md:p-6 w-full">
                        <div class="flex flex-wrap w-full flex-col md:flex-row gap-4">
                            <div class="flex w-full md:basis-[32%] flex-col gap-4 mb-4">
                                <label for="title" class="font-semibold">Título:</label>
                                <InputText 
                                v-model:model-value="productForm.title"
                                id="title" 
                                :class="{'!border !border-red-500': $productValidator.title.$invalid && $productValidator.title.$dirty}"
                                @input="$productValidator.title.$touch()" 
                                aria-describedby="product-title-help"

                                placeholder="Título" 
                                fluid
                                />
                                <small id="category-title-help" v-if="$productValidator.title.required.$invalid && $productValidator.title.$dirty" class="text-red-600">Título requerido.</small>
                                <small id="category-title-help" v-else-if="$productValidator.title.minLength.$invalid && $productValidator.title.$dirty" class="text-red-600">Título demasiado corto.</small>
                            </div>

                            <div class="flex basis-[32%] flex-col gap-4 mb-4">
                                <label for="header-tag" class="font-semibold">Tag Cabecera:</label>
                                <InputText v-model:model-value="productForm.header_tag" id="header-tag" placeholder="Tag Cabecera" />
                            </div>

                            <div class="flex basis-[32%] flex-col gap-4 mb-4">
                                <label for="subcategory" class="font-semibold">Sub Categoría:</label>
                                <Select 
                                :options="subcategoryOptions"
                                option-label="label"
                                option-value="value"

                                v-model:model-value="productForm.subcategory"
                                id="subcategory" 
                                :class="{'!border !border-red-500': $productValidator.subcategory.$invalid && $productValidator.subcategory.$dirty}"
                                @input="$productValidator.subcategory.$touch()" 
                                aria-describedby="product-subcategory-help"

                                placeholder="Sub Categoría"
                                empty-message="Sin Categorías para mostrar"
                                />
                                <small id="product-subcategory-help" v-if="$productValidator.subcategory.required.$invalid && $productValidator.subcategory.$dirty" class="text-red-600">Subcategoría requerida.</small>
                            </div>

                            <div class="flex basis-[32%] flex-col gap-4 mb-4">
                                <label for="ref-price" class="font-semibold">Precio Referencial:</label>
                                <InputNumber 
                                @update:model-value="calculatePorc"
                                v-model:model-value="productForm.reference_price"
                                inputId="ref-price" 
                                mode="currency" 
                                currency=ARS 
                                locale="es-AR"
                                placeholder="Precio Referencial"
                                />
                            </div>

                            <div class="flex basis-[32%] flex-col gap-4 mb-4">
                                <label for="client-price" class="font-semibold">Precio Cliente:</label>
                                <InputNumber 
                                v-model:model-value="productForm.price"
                                id="price" 
                                :class="{'!border !border-red-500': $productValidator.price.$invalid && $productValidator.price.$dirty}"
                                @input="$productValidator.price.$touch()" 
                                aria-describedby="product-price-help"
                                @update:model-value="calculatePorc"

                                inputId="client-price" 
                                mode="currency" 
                                currency=ARS 
                                locale="es-AR"
                                placeholder="Precio Cliente"
                                />
                                <small id="product-price-help" v-if="$productValidator.price.required.$invalid && $productValidator.price.$dirty" class="text-red-600">Precio requerido.</small>
                            </div>

                            <div class="flex basis-[32%] flex-col gap-4 mb-4">
                                <label for="discount" class="font-semibold">Descuento:</label>
                                <InputNumber 
                                v-model:model-value="productForm.discount"

                                disabled
                                inputId="discount" 
                                suffix="%"
                                placeholder="Descuento"
                                />
                            </div>

                            <div class="flex basis-full flex-col gap-4 mb-4">
                                <div class="w-full flex flex-col gap-2">
                                    <label for="description" class="flex-auto font-semibold">Descripción:</label>
                                
                                    <SummernoteEditor v-model="productForm.description"/>
                                </div>
                            </div>

                            <div class="flex basis-full flex-col gap-4 mb-4">
                                <label for="discount" class="font-semibold">Imagen Principal:</label>
                                <FileUpload 
                                id="main-upload"
                                v-model="uploadedFiles"
                                @select="onSelect"
                                :customUpload="true"
                                accept="image/*" 
                                :maxFileSize="1000000"
                                :auto="false"
                                :file-limit="1"
                                :multiple="false"
                                ref="fileUpload"
                                >
                                    <template #content>
                                        <div
                                        class="mt-4 flex flex-col justify-center items-center h-40 border-dashed border-2 border-gray-300 p-4 rounded-lg cursor-pointer"
                                        @click="triggerFileSelect"
                                        >
                                            <img v-if="previewImage" :src="previewImage" alt="Preview Image" class="max-w-full max-h-32 object-contain mb-2" />
                                            
                                            <div v-else class="flex flex-col justify-center items-center">
                                                <i class="pi pi-inbox !text-4xl text-gray-400"></i>
                                                <p class="text-gray-500 mt-2 text-center">Haz clic o arrastra un archivo aquí para cargarlo</p>
                                            </div>
                                        </div>
                                    </template>
                                </FileUpload>
                            </div>
                        </div>
                    </form>
                </AccordionContent>
            </AccordionPanel>

            <AccordionPanel value="1">
                <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Imágenes Extras</AccordionHeader>
                <AccordionContent>
                    <FileUpload 
                    :show-cancel-button="false" 
                    :show-upload-button="false" 
                    choose-label="Cargar"
                    class="normal"
                    accept="image/*" 
                    :maxFileSize="1000000"
                    :multiple="true"
                    @select="onSelectMultiple"
                    >
                        <template #content>
                            <div v-if="images.length > 0" class="flex !h-80 overflow-scroll flex-col gap-8 pt-4">
                                <div class="flex flex-wrap gap-4">
                                    <div v-for="(file, index) of images" :key="file.id" class="p-8 rounded-border flex flex-col border border-surface items-center gap-4">
                                        <div>
                                            <img role="presentation" :alt="file.name" :src="file.image" width="100" height="50" />
                                        </div>
                                        <span class="font-semibold text-ellipsis max-w-60 whitespace-nowrap overflow-hidden">{{ file.name }}</span>
                                        <Button @click="onRemoveMultiple(file.id, file.name, index)" icon="pi pi-times" outlined rounded severity="danger" />
                                    </div>
                                </div>
                            </div>
                        </template>

                        <template #empty>
                            <span v-if="images.length === 0" class="p-8 block text-center w-full text-2xl text-gray-400">
                                Arrastre y suelte archivos aquí para cargarlos.
                            </span>
                        </template>

                    </FileUpload>
                </AccordionContent>
            </AccordionPanel>

            <AccordionPanel value="2">
                <AccordionHeader class="!uppercase !bg-slate-400/[0.2]">Promociones</AccordionHeader>
                <AccordionContent>
                    <div class="w-full p-1 md:p-4">
                        <div class="my-4 flex items-center">
                            <Checkbox @change="toggleDefaultOfferts" v-model:model-value="productForm.show_offerts" inputId="show-offerts" name="pizza" :binary="true"/>
                            <label for="show-offerts" class="ml-2">Mostrar Ofertas</label>
                        </div>

                        <div class="flex flex-col p-1 md:p-4 m-0 md:mt-4">
                            <div 
                            v-for="(iproduct, index) in productForm.offers" 
                            class="my-4 md:my-8 grid grid-cols-1 md:grid-cols-6 w-full gap-4"
                            :key="iproduct.id"
                            >
                                <div class="flex items-center gap-3">
                                    <label for="ititle">Título:</label>
                                    <InputText fluid id="ititle" v-model:model-value="iproduct.title" placeholder="Título" />
                                </div>

                                <div class="flex items-center gap-3">
                                    <label for="itag">Tag:</label>
                                    <InputText fluid id="itag" v-model:model-value="iproduct.header_tag" placeholder="Tag" />
                                </div>

                                <div class="flex items-center gap-3">
                                    <label for="itag">Cantidad:</label>
                                    <InputNumber @blur="setValue(index)" fluid id="itag" v-model:model-value="iproduct.amount" placeholder="Cantidad" />
                                </div>

                                <div class="flex items-center gap-3">
                                    <label for="irefprice">Precio1:</label>
                                    <InputNumber fluid id="irefprice" v-model:model-value="iproduct.reference_price" mode="currency" currency=ARS locale="es-AR" placeholder="Precio Referencia" />
                                </div>

                                <div class="flex items-center gap-3">
                                    <label for="iprice">Precio2:</label>
                                    <InputNumber fluid id="iprice" v-model:model-value="iproduct.price" mode="currency" currency=ARS locale="es-AR" placeholder="Precio Cliente" />
                                </div>

                                <div class="flex items-center gap-3">
                                    <label for="iprice">Descuento:</label>
                                    <InputNumber fluid id="iprice" v-model:model-value="iproduct.discount" suffix="%" placeholder="Descuento" disabled />

                                   <i @click="removeProductOffer(iproduct)" class="cursor-pointer pi pi-minus-circle"></i>
                                </div>
                            </div>
                        </div>

                        <Button @click="addProductOffer" icon="pi pi-plus" class="mt-8 !border-dashed !border-1 !border-slate-500 !font-normal" severity="secondary" label="Agregar Ofertas" text fluid/>
                       
                    </div>
                </AccordionContent>
            </AccordionPanel>
        </Accordion>

        <template #footer>
            <div class="flex flex-row gap-4">
                <Button severity="secondary" label="Cancelar" @click="showEditModal = false" />
                <Button @click="confirmEdit" :disabled="loadingSubmit" :loading="loadingSubmit" label="Aceptar" />
            </div>
        </template>
    </Dialog>

    <Toast />
    <ConfirmDialog></ConfirmDialog>
</template>

<script lang="ts" setup>
    import {ref, type UnwrapRef} from 'vue';
    import { cloneDeep } from 'lodash-es';

    import { useConfirm } from "primevue/useconfirm";
    import { useToast } from "primevue/usetoast";
    import { required, minLength } from '@vuelidate/validators';
    import useVuelidate from '@vuelidate/core';
    import type { FileUploadSelectEvent } from 'primevue/fileupload';

    import { fetchWrapper } from '~/helpers/fetch-wrapper';
    import { useListen } from '~/composables/useMitt';
    import { Globalization } from '~/helpers/globalization';
    import type { ImageProduct, ProductForm, ProductItem, ProductOfferItem} from '~/types/dashboard/products';
    import type { SelectOption } from '~/types';

    // Meta configuration
    const confirm = useConfirm();
    const toast = useToast();

    function resetForm(){
        productForm.title='';
        productForm.header_tag='';
        productForm.description='';
        productForm.price=0;
        productForm.discount=0;
        productForm.reference_price=0;
        productForm.main_image='';
        productForm.subcategory='';
        productForm.images=[];
        productForm.offers=[];

        previewImage.value=false;
        $productValidator.value.$reset();
    };
    const productRules = computed(() => ({
        title: {
            required,
            minLength: minLength(4),
        },
        price: {
            required
        },
        subcategory: {
            required
        }
    }));
    function getBase64(file: File) {
        return new Promise<string>((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result as string);
            reader.onerror = error => reject(error);
        });
    }

    /********************* 
    | DATA
    **********************/
    const currentId = ref<number>(-1);
    const loadingSubmit=ref<boolean>(false);
    const formTitle=ref<string>('Nuevo Producto');

    const showEditModal=ref<boolean>(false);
    const productData=ref<ProductItem[]>([]);
    const filteredProductData=ref<ProductItem[]>([]);

    const productForm:UnwrapRef<ProductForm> = reactive({
        title: '',
        header_tag: '',
        description: '',
        price: 0,
        discount: 0,
        reference_price: 0,
        main_image: '',
        subcategory: '',
        images: [],
        offers: [],
        show_offerts: false
    });

    const $productValidator=useVuelidate(productRules, productForm);

    const subcategoryOptions=ref<SelectOption[]>([]);
    const uploadedFiles = ref([]);
    const previewImage = ref();
    const fileUpload = ref(); 
    const images = ref<ImageProduct[]>([]);

    /********************* 
    | METHODS
    **********************/
    //
    const calculatePorc = (value:number) => {
        const result =Math.trunc(((productForm.reference_price - productForm.price) / productForm.reference_price) * 100);
        productForm.discount = (isFinite(result) && result > -1) ? result:0;
    };
    const triggerFileSelect = () => {
        fileUpload.value.$refs.fileInput.click(); 
    };

    const setValue = (index:number) => {
        if(productForm.offers[index].amount === null || productForm.offers[index].amount.toString() === ''){
            productForm.offers[index].amount=1;
        };
    };
    const removeProductOffer = (item: ProductOfferItem) => {
        confirm.require({
            message: 'Seguro(a) que quieres borrar esta oferta?',
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
                params.append('offer_id', Math.round(item.id).toString());
                await fetchWrapper.delete('/products/offer?'+ params).then((msg)=>{
                    const index = productForm.offers.indexOf(item);
                    if (index !== -1) {
                        productForm.offers.splice(index, 1);
                    }
                    toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
                }).catch((e)=>{
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Error al eliminar: '+JSON.stringify(e), life: 6000 });
                });
            }
        });
    };
    const addProductOffer = () => {
        productForm.offers.push({
            id: Date.now(),
            title: '',
            price: 0,
            reference_price: 0,
            discount: 0,
            header_tag: '',
            amount: 0
        });
    };
    const toggleDefaultOfferts = ()=>{
        if(productForm.show_offerts && productForm.offers.length === 0){
            for (let x = 2; x <= 3;x++){
                productForm.offers.push({
                    id: Date.now(),
                    title: 'Compra '+(x)+' artículos y ahorra '+(x*10)+'%',
                    price: (productForm.reference_price * x) * (1 - ((x*10) / 100)),
                    reference_price: (productForm.reference_price * x),
                    discount: (x*10),
                    header_tag: 'Promoción',
                    amount: x
                });
            }
        }else{
            productForm.offers=[];
        }
    };

    const onSelect = async(event:FileUploadSelectEvent) => {
        const file = event.files[0];
        previewImage.value = URL.createObjectURL(file);
        productForm.main_image=await getBase64(file);
    };
    const onSelectMultiple = async(event:FileUploadSelectEvent) => {
        const file = event.files[images.value.filter(entry=> !entry.image.startsWith('http')).length];
        images.value.push({
            id: Math.random(),
            name: file.name === undefined ? '' : file.name,
            image: await getBase64(file)
        });
    };
    const onRemoveMultiple = async(id:number, name: string, index:number)=>{
        const params = new URLSearchParams();
        params.append('img_id', id.toString());

        confirm.require({
            message: 'Seguro(a) que quieres borrar "'+name+'"?',
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
                params.append('img_id', JSON.stringify(id));
                await fetchWrapper.delete('/products/image?'+params).then((msg)=>{
                    productForm.images.splice(index, 1);

                    toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
                }).catch((e)=>{
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Error al eliminar: '+JSON.stringify(e), life: 6000 });
                });
            }
        });
    };
    const doNew=()=>{
        resetForm();
        currentId.value=-1;
        formTitle.value='Nuevo Producto';
        showEditModal.value=true;
    };

    const doEdit = async (id:number)=>{
        currentId.value=id;
        const index = filteredProductData.value.findIndex(obj => obj.id === currentId.value);
        const obj = filteredProductData.value[index];
        productForm.title=obj.title;
        productForm.header_tag=obj.header_tag;
        productForm.description=obj.description;
        productForm.price=obj.price;
        productForm.discount=obj.discount;
        productForm.reference_price=obj.reference_price;
        productForm.main_image=obj.main_image;
        productForm.subcategory=obj.subcategory__id.toString();
        productForm.show_offerts=obj.show_offerts;
        previewImage.value=obj.main_image;

        const params = new URLSearchParams();
        params.append('product_id', currentId.value.toString());

        productForm.offers=await fetchWrapper.get('/products/offers?'+params);
        images.value=await fetchWrapper.get('/products/images?' + params);

        formTitle.value='Editar Producto';
        showEditModal.value=true;
    };

    const confirmDelete = (id:number) => {
        const index = filteredProductData.value.findIndex(obj => obj.id === id);
        const obj = filteredProductData.value[index];

        confirm.require({
            message: 'Seguro(a) que quieres borrar "'+obj.title+'"?',
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
                params.append('product_ids', JSON.stringify([id]));
                await fetchWrapper.delete('/products/delete?'+ params).then((msg)=>{
                    filteredProductData.value=filteredProductData.value.filter(item => item.id !== id);
                    productData.value=productData.value.filter(item => item.id !== id);

                    toast.add({ severity: 'success', summary: 'Confirmación', detail: msg, life: 4000 });
                }).catch((e)=>{
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Error al eliminar: '+JSON.stringify(e), life: 6000 });
                });
            }
        });
    };

    const confirmEdit = async()=>{
        productForm.images=images.value.map(e=>e.image);
        if(currentId.value === -1){
            await fetchWrapper.post('/products/product?', productForm).then((resp)=>{
                filteredProductData.value.push(resp['data']);

                toast.add({ severity: 'success', summary: 'Confirmación', detail: resp['msg'], life: 5000 });
                showEditModal.value = false;
            }).catch((e)=>{
                toast.add({ severity: 'error', summary: 'Error', detail: 'Error al guardar: '+JSON.stringify(e), life: 7000 });
            });
        }else{
            const params = new URLSearchParams();
            params.append('product_id', currentId.value.toString());

            await fetchWrapper.put('/products/product?'+params, productForm).then((resp)=>{
                const index = filteredProductData.value.findIndex(obj => obj.id === currentId.value);
                filteredProductData.value[index]=resp['data'];

                toast.add({ severity: 'success', summary: 'Confirmación', detail: resp['msg'], life: 5000 });
                showEditModal.value = false;
            }).catch((e)=>{
                toast.add({ severity: 'error', summary: 'Error', detail: 'Error al editar: '+JSON.stringify(e), life: 7000 });
            });      
        }
    };

    /********************* 
    | MOUNT
    **********************/
    useListen('application:add-new' , (message:any) => {
        doNew();
    });
    useListen('application:search' , (message:any) => {
        const search = (message.message as string).toLowerCase();
        filteredProductData.value=productData.value.filter(entry=>{
            return (
                entry.title.toLowerCase().includes(search) ||
                entry.header_tag.toLowerCase().includes(search) ||
                entry.subcategory__title.toLowerCase().includes(search) ||
                entry.price.toString().includes(search) ||
                entry.reference_price.toString().includes(search) ||
                entry.discount.toString().includes(search)
            );
        });
    });

    onMounted(async()=>{
        productData.value=await fetchWrapper.get('/products/products');
        filteredProductData.value=cloneDeep(productData.value);

        subcategoryOptions.value=await fetchWrapper.get('/subcategories/options');
    });
</script>