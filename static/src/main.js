import Vue from 'vue'
import App from './demo.vue'
import 'xterm/dist/xterm.css'
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
