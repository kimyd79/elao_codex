import Vue from 'vue'
import App from './App.vue'
import router from './router'

import LegoComponent from 'lego-component'
import './styles/common.scss'

import VueSweetalert2 from 'vue-sweetalert2';
// If you don't need the styles, do not connect
import 'sweetalert2/dist/sweetalert2.min.css';

import Layouts from './components/layout';

// for tooltip
import VueCustomTooltip from '@adamdehaven/vue-custom-tooltip'

import moment from 'moment'

Vue.config.productionTip = false;

Vue.use(VueSweetalert2);
Vue.use(VueCustomTooltip, {
  name: 'VueCustomTooltip',
  color: '#fff',
  background: '#553ca5',
  borderRadius: 12,
  fontWeight: 400,
})

Vue.use(LegoComponent);
Vue.use(Layouts);
//Vue.use(VueSimpleAlert, { reverseButtons: true });

Vue.use(moment);

// Below codes come alert for leaving this site.
window.addEventListener('beforeunload', function (e) { 
  e.preventDefault(); 
  e.returnValue = ''; 
}); 

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
