import Vue from 'vue'
import Router from 'vue-router'
import Reports from '@/components/Reports'
import Home from '@/components/Home'
import DealsList from '@/components/DealsList'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path:'/deals',
      name: 'DealsList',
      component: DealsList
    }

  ]
})
