import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import VeeValidate from 'vee-validate'
import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue);
// LightBootstrap plugin
import LightBootstrap from './light-bootstrap-main'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import 'jquery'


import routes from './routes/routes'
// plugin setup
Vue.use(VueRouter)
Vue.use(LightBootstrap)
Vue.use(VeeValidate)

export const apiLink = '/api';
Vue.prototype.$apiLink = '/api'
// Vue.prototype.$apiLink = 'http://127.0.0.1:5000/api'
// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkActiveClass: 'nav-item active'
})

Vue.config.devtools = true
/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  router
})
