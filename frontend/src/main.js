import Vue from 'vue'
import App from './App.vue'
import router from './router'

import LegoComponent from 'lego-component'
import './styles/common.scss'
import Layouts from './components/layout'

import VueSimpleAlert from "vue-simple-alert";

Vue.config.productionTip = false

Vue.use(LegoComponent);
Vue.use(Layouts);
Vue.use(VueSimpleAlert, { reverseButtons: true });

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
