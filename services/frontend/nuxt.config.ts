// https://nuxt.com/docs/api/configuration/nuxt-config
if (!process.env.DEBUG){
    require('dotenv').config({path: __dirname+"/../../.env.dev"});
}

import Noir from './presets/Noir';
const config=process.env;

export default defineNuxtConfig({
    app: {
        head: {
            meta: [
                { name: 'viewport', content: 'width=device-width, initial-scale=1, user-scalable=no' },
            ],

            script: [
                { src: 'https://code.jquery.com/jquery-3.6.0.min.js', type: 'text/javascript' },
                { src: 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/3.20.0/codemirror.min.js', type: 'text/javascript' },
                { src: 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/3.20.0/mode/xml/xml.js', type: 'text/javascript' },
                { src: 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/2.36.0/formatting.min.js', type: 'text/javascript' },

                { src: 'https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js', type: 'text/javascript' },
                { src: 'https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/lang/summernote-es-ES.min.js', type: 'text/javascript' },
            ]
        }
    },
    css:[
        '@/assets/Satoshi/Fonts/WEB/css/satoshi.css'
    ],
    compatibilityDate: '2024-04-03',
    devtools: { enabled: false },
    modules: [
        '@primevue/nuxt-module',
        "@nuxtjs/tailwindcss",
        '@pinia/nuxt',
        '@pinia-plugin-persistedstate/nuxt'
    ],
    components: [
        {
            path: '~/components',
            pathPrefix: false,
        },
    ],
    pages: true,
    runtimeConfig: {
        public: {
            VITE_API_URL: process.env.VITE_API_URL
        }
    },
    ssr: false,
    imports: {
        dirs: ['store'],
    },
    //

    primevue: {
        options: {
            theme: {
                preset: Noir,
                options: {
                    prefix: 'p',
                    darkModeSelector: '.p-dark',
                    cssLayer: false,
                }
            },
            locale:{
                firstDayOfWeek: 1,
                dayNames: [
                  'domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'
                ],
                dayNamesShort: [
                  'dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb'
                ],
                dayNamesMin: [
                  'D', 'L', 'M', 'X', 'J', 'V', 'S'
                ],
                monthNames: [
                  'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                  'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
                ],
                monthNamesShort: [
                  'ene', 'feb', 'mar', 'abr', 'may', 'jun',
                  'jul', 'ago', 'sep', 'oct', 'nov', 'dic'
                ],
                today: 'Hoy',
                clear: 'Limpiar',
                weekHeader: 'Sem',
            }
        }
    }
})