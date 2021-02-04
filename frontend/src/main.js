// =========================================================
// * Vuetify Material Dashboard PRO - v2.1.0
// =========================================================
//
// * Product Page: https://www.creative-tim.com/product/vuetify-material-dashboard-pro
// * Copyright 2019 Creative Tim (https://www.creative-tim.com)
//
// * Coded by Creative Tim
//
// =========================================================
//
// * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/index.js'
import './plugins/base'
import './plugins/chartist'
import './plugins/vee-validate'
import './plugins/vue-world-map'
import vuetify from './plugins/vuetify'
import i18n from './i18n'
import VueAxios from 'vue-axios'
import VueAuthenticate from 'vue-authenticate'
import axios from 'axios';
import { BASE_API } from '@/api/index'
import { TwitterAuthConfig } from '@/config'
import VueNativeSock from 'vue-native-websocket'
import Meta from 'vue-meta'
import VueGtag from "vue-gtag";

Vue.use(VueGtag, {
  config: { id: "G-ZVN752YT85" }
});


Vue.use(Meta);

Vue.use(
  VueNativeSock,
  process.env.VUE_APP_SOCKET_URL, 
  { 
    store,
    format: 'json',
    reconnection: true, // (Boolean) whether to reconnect automatically (false)
    // reconnectionAttempts: 5, // (Number) number of reconnection attempts before giving up (Infinity),
    reconnectionDelay: 3000, // (Number) how long to initially wait before attempting a new (1000)
 }
)

const LoginWithTwitter = require("login-with-twitter");

const twitterAuth = new LoginWithTwitter({
    consumerKey: TwitterAuthConfig.consumerKey,
    consumerSecret: TwitterAuthConfig.consumerSecret,
    callbackUrl: TwitterAuthConfig.callbackUrl
  });

  //Install Vue plugin
Vue.twitterAuth = twitterAuth;
Object.defineProperties(Vue.prototype, {
  $twitterAuth: {
    get: function() {
      return Vue.twitterAuth;
    }
  }
});

Vue.use(VueAxios, axios)
Vue.use(VueAuthenticate, {
  tokenName: 'access_token',
  baseUrl: BASE_API, // Your API domain
  storageType: 'cookieStorage',

  providers: {
    twitter: {
      name: 'twitter',
      url: '/auth/twitter/',
      clientId: 'Szk06qiHVrfrAEyP7XzrjJke7',
    }
  }
})

Vue.config.productionTip = false

const eventsHub = new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: h => h(App),
}).$mount('#app')

// Vue.use(IdleVue, {
//   eventEmitter: eventsHub,
//   store,
//   idleTime: 15*60*1000, // 15 mins  15*60*1000 = 900000
//   startAtIdle: false
// });

Vue.use(require('vue-moment'));
