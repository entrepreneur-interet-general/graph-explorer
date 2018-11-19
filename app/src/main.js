import Vue from 'vue';
import VueMaterial from 'vue-material';
import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';
import App from './components/App.vue';
import store from './store';

Vue.use(VueMaterial);

new Vue({ // eslint-disable-line no-new
  el: '#app',
  store,
  render: h => h(App)
});

window.Event = new Vue();
