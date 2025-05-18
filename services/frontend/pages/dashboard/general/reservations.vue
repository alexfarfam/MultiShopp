<template>
    <div>
        <div class="m-4 flex items-center gap-2">
            <Checkbox @change="getEvents" input-id="showActives" v-model="showActives" binary/>
            <label for="showActives">Reservaciones por atender</label>
        </div>

        <ClientOnly>
            <ScheduleXCalendar :calendar-app="calendarApp">
                <template #eventModal="{ calendarEvent }">
                    <div class="sx__interactive-event-modal">
                        <span class="font-medium text-lg">{{ calendarEvent.title }}</span>
                        <div class="flex flex-col gap-2 p-2 mt-3">
                            <div class="flex flex-row gap-2">
                                <i class="pi pi-clock"></i> <span class="text-sm">{{`${new Date(calendarEvent.start).toLocaleDateString('es-ES', dateOptions)} ⋅ ${new Date(calendarEvent.start).toLocaleTimeString('es-ES', timeOptions)} – ${new Date(calendarEvent.end).toLocaleTimeString('es-ES', timeOptions)}`}}</span>
                            </div>

                            <div class="flex flex-row gap-2">
                                <i class="pi pi-user"></i> <span class="text-sm">{{calendarEvent.people[0]}}</span>
                            </div>

                            <div class="flex flex-row gap-2">
                                <i class="pi pi-pen-to-square"></i> <span class="text-sm">{{ calendarEvent.description }}</span>
                            </div>

                            <div class="flex flex-row gap-2">
                                <i class="pi pi-calendar-plus"></i> <span class="text-sm">{{ calendarEvent.subservices  }}</span>
                            </div>

                            <div v-if="calendarEvent.active" class="mt-4 flex flex-row gap-2">
                                <label for="telephone" class="w-18 font-medium">Notas:</label>
                                <div class="flex-1 flex flex-col">
                                    <Textarea
                                    v-model:model-value="notes"
                                    placeholder="Alguna nota para el cliente"
                                    fluid
                                    size="small"
                                    />
                                </div>
                            </div>
                            <div v-if="calendarEvent.active" class="mt-2 flex flex-row gap-2">
                                <Button @click="doAction('Confirmar', calendarEvent)" class="!bg-green-500 !border-green-500 !text-white flex-1" icon="pi pi-check" size="small" label="Confirmar" />
                                <Button @click="doAction('Rechazar', calendarEvent)" class="!bg-red-500 !border-red-500 !text-white flex-1" icon="pi pi-times" size="small" label="Rechazar" />
                                <!--<Button v-show="false" @click="doAction('Reprogramar', calendarEvent)" class="!bg-blue-500 !border-blue-500 !text-white" icon="pi pi-clock" size="small" label="Reprogramar" /> -->
                            </div>

                        </div>
                    </div>
                </template>
            </ScheduleXCalendar>
        </ClientOnly>
    </div>

    <ConfirmDialog></ConfirmDialog>
</template>

<script lang="ts" setup>
    import {ScheduleXCalendar} from "@schedule-x/vue";
    import {
        createCalendar,
        viewDay,
        viewWeek,
        viewMonthGrid,
        viewMonthAgenda,
        type CalendarEvent,
    } from '@schedule-x/calendar';
    import '@schedule-x/theme-default/dist/index.css';
    import {createResizePlugin} from "@schedule-x/resize";
    import { createDragAndDropPlugin } from '@schedule-x/drag-and-drop';
    import { createEventModalPlugin } from '@schedule-x/event-modal';
    import {createScrollControllerPlugin} from "@schedule-x/scroll-controller";
    import { fetchWrapper } from "~/helpers/fetch-wrapper";
    import { useMediaQuery } from "@vueuse/core";

    // Meta configuration
    const confirm = useConfirm();
    const toast = useToast();
    const isMobile = useMediaQuery('(max-width: 600px)');

    const authStore = useAuthStore();
    const {user} = storeToRefs(authStore);

    const dateOptions:Intl.DateTimeFormatOptions = { year: 'numeric', month: 'short', day: '2-digit' };
    const timeOptions:Intl.DateTimeFormatOptions = { hour: 'numeric', minute: 'numeric', hour12: true };

    const eventModal = createEventModalPlugin();
    const dragAndDropEvent = createDragAndDropPlugin();

    const calendarApp = shallowRef(createCalendar({
        locale: 'es-ES',
        views: [viewDay, viewWeek, viewMonthGrid, viewMonthAgenda],
        defaultView: viewWeek.name,
        isResponsive: true,
        plugins: [
            createResizePlugin(),
            createScrollControllerPlugin({
                initialScroll: '07:00'
            }),
            dragAndDropEvent,
            eventModal
        ],
        events: [],
        calendars: {
            work: {
                colorName: 'work',
                lightColors: {
                    container: '#fff',
                    onContainer: '#000',
                    main: '#fff',
                },
                darkColors: {
                    container: '#000',
                    onContainer: '#fff',
                    main: '#000',
                },
            }
        },
        weekOptions: {
            timeAxisFormatOptions: { hour: '2-digit', minute: '2-digit', hour12: true },
        },
    }));

    function convertUTCToLocal(dateString:string) {
        const utcDate = new Date(`${dateString}Z`);

        const localYear = utcDate.getFullYear();
        const localMonth = (utcDate.getMonth() + 1).toString().padStart(2, '0'); 
        const localDay = utcDate.getDate().toString().padStart(2, '0');
        const localHours = utcDate.getHours().toString().padStart(2, '0');
        const localMinutes = utcDate.getMinutes().toString().padStart(2, '0');

        const localDateString = `${localYear}-${localMonth}-${localDay} ${localHours}:${localMinutes}`;
        
        return localDateString;
    }
    /********************* 
    | DATA
    **********************/
    const showActives = ref<boolean>(true);
    const notes=ref<string>();

    /********************* 
    | METHODS
    **********************/
    const getEvents= async()=> {
        const params = new URLSearchParams();
        params.append('active', showActives.value?'1':'0');
        const data = await fetchWrapper.get('/reservations/all?'+params);
        data.forEach((item:any) => {
            item.start = convertUTCToLocal(item.start);
            item.end = convertUTCToLocal(item.end);
        });

        calendarApp.value.events.set(data);
    };

    const doAction=(action:string, calendarEvent:CalendarEvent)=>{
        confirm.require({
            message: "¿Seguro(a) que quieres "+action+" esta reservación?",
                header: action,
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
                accept: async()=>{
                    const params = new URLSearchParams();
                    params.append('reservation_id', calendarEvent.id.toString());
                    params.append('action', action.toLocaleLowerCase());

                    await fetchWrapper.put('/reservations/update?'+params).then(async (response)=>{
                        toast.add({ severity: 'success', summary: 'Éxito', detail: response, life: 5000 });
                        await getEvents();

                        const telephone:string = calendarEvent.telephone.replaceAll(/\s/g,'');
                        const prefix = (!telephone.startsWith('51') && telephone.length === 9) ? '51':(!telephone.startsWith('54') ? '54':'');
                        const phoneNumber=prefix+telephone;

                        var message='Hola! '+ new String(calendarEvent.people && calendarEvent.people [0]).toString()+', le saluda *'+user.value?.company+'*!🤗\nPara informarle que su *'+calendarEvent.title+ '* a sido ';
                        if (action === 'Confirmar'){
                            message+=' ✅*aceptado*! Por favor acudir a la hora programada.';
                        }else if (action === 'Rechazar'){
                            message+=' 🚫*rechazado*! Disculpe las molestias.';
                        }else if (action === 'Reprogramar'){
                            message+=' 📆*reprogramado*!.';
                        }  

                        if (notes.value?.trim() !== ''){
                            message+='\nNotas: '+notes.value; 
                        }
                        
                        const encodedMessage = encodeURIComponent(message);
                        const whatsappUrl = isMobile.value? `https://wa.me/${phoneNumber}/?text=${encodedMessage}`:`https://web.whatsapp.com/send/?phone=${phoneNumber}&text=${encodedMessage}&type=phone_number&app_absent=0`;
                        window.open(whatsappUrl);
                    }).catch((e)=>{
                        toast.add({ severity: 'error', summary: 'Error', detail: JSON.stringify(e), life: 7000 });
                    });
                }
        });
    };

    /********************* 
    | MOUNT
    **********************/
    onMounted(async() => {
        await getEvents();
    })

</script>


<style>
.sx-vue-calendar-wrapper {
    height: 700px;
    max-height: 90vh;
    width: 100%;
}

.sx__interactive-event-modal {
    padding: var(--sx-spacing-padding6);
    background-color: var(--sx-color-background);
    box-shadow: 0 24px 38px 3px rgba(0,0,0,.14),0 9px 46px 8px rgba(0,0,0,.12),0 11px 15px -7px rgba(0,0,0,.2);
    border-radius: var(--sx-rounding-small);
}
</style>
