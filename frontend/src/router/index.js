import Vue from 'vue'
import Router from 'vue-router'
import Reports from '@/components/Reports'
import Home from '@/components/Home'
import DealsList from '@/components/DealsList'
import PendingDeals from '@/components/DealsPending'


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
    },
    {
      path:'/reports',
      name: 'Reports',
      component: Reports
    },
    { path:'/pendingdeals',
      name: 'PendingDeals',
      component: PendingDeals
    }

  ]
})
