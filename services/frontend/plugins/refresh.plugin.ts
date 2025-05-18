import {useAuthStore} from '~/stores/auth.store';

export default defineNuxtPlugin({
    name: 'refresh-plugin',
    enforce: 'post',
    hooks: {
        // You can directly register Nuxt app runtime hooks here
        'app:created': async()=>{
            const store=useAuthStore();
            await store.startRefreshTokenTimer();
        }
    },
    env: {
        // Set this value to `false` if you don't want the plugin to run when rendering server-only or island components.
        islands: true
    }
});