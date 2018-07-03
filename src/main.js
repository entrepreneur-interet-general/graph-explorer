import Vue from 'vue'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css' 
import App from './components/App.vue'
import store from './store.js'

Vue.use(VueMaterial);

new Vue({
  el: '#app',
  store,
  render: h => h(App),
});

window.Event = new Vue();