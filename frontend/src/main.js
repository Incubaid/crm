// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { ApolloClient, createNetworkInterface } from 'apollo-client'
import VueApollo from 'vue-apollo'
import axios from 'axios';
Vue.config.productionTip = false

// Create the apollo client
const apolloClient = new ApolloClient({
  networkInterface: createNetworkInterface({
    uri: 'http://localhost:5000/api',
    reduxRootKey: 'apollo'
  }),
  connectToDevTools: true
})
// Install the vue plugin
Vue.use(VueApollo)
const apolloProvider = new VueApollo({
  defaultClient: apolloClient
})
/* eslint-disable no-new */
var crmapp = new Vue({
  el: '#app',
  apolloProvider,
  router,
  template: '<App/>',
  components: { App }
})
console.log(crmapp)
