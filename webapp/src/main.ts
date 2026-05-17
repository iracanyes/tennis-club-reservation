import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import { router }  from './router';
import PrimeVue from 'primevue/config';
import Aura from "@primeuix/themes/aura";
import {Ripple, ToastService} from "primevue";

const app = createApp(App)
  .use(router)
  .use(PrimeVue, {
    theme: {
      preset : Aura,
      options : {
        darkModeSelector : false
      }
    },
    //ripple : true
  })
  .use(ToastService);
// Add directive ripple
app.directive('ripple', Ripple);

app.mount('#app');
