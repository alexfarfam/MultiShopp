import { defineNuxtPlugin } from '#app';
import VImageMagnifier from 'v-image-magnifier';

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.vueApp.use(VImageMagnifier, {
        zoomSize: 200,
        zoomFactor: 5,
        magnifiedBorderRadius:100
    })
})
