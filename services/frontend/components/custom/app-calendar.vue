

<template>
    <div>
      <ClientOnly>
        <ScheduleXCalendar :calendar-app="calendarApp">
  <!--        <template #timeGridEvent="{ calendarEvent }">-->
  <!--          <div class="event">-->
  <!--            {{ calendarEvent.title }}-->
  <!--          </div>-->
  <!--        </template>-->
        </ScheduleXCalendar>
      </ClientOnly>
    </div>
</template>

<script setup>
    import {ScheduleXCalendar} from "@schedule-x/vue";
    import {
        createCalendar,
        viewDay,
        viewWeek,
        viewMonthGrid,
        viewMonthAgenda,
    } from '@schedule-x/calendar'
    import '@schedule-x/theme-default/dist/index.css'
    import {createResizePlugin} from "@schedule-x/resize";
    import {createScrollControllerPlugin} from "@schedule-x/scroll-controller";

    const calendarApp = createCalendar({
        locale: 'es-AR',
        views: [viewDay, viewWeek, viewMonthGrid, viewMonthAgenda],
        defaultView: viewWeek.name,
        isResponsive: true,
        plugins: [
            createResizePlugin(),
            createScrollControllerPlugin({
                initialScroll: '08:00'
            })
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
        }
    });

    onMounted(() => {

            calendarApp.events.set([
            {
                id: 1,
                title: 'Event 1',
                description: 'PRUEBA PRUEBAAA',
                start: '2024-11-01 11:00',
                end: '2024-11-01 12:00',
            },
            {
                id: 2,
                title: 'Event 2',
                description: 'PRUEBA PRUEBAAA',
                start: '2024-11-01 12:00',
                end: '2024-11-01 13:00',
            },
            ])
        
    })

</script>


<style>
.sx-vue-calendar-wrapper {
  height: 700px;
  max-height: 90vh;
  width: 100%;
}
</style>