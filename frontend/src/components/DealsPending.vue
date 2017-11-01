<template>
  <div>
    <h1>List of Pending Deals</h1>
    <span v-if="loading">Still loading</span>
    <span v-else>
    <ul>
        <li v-for="(deal, idx) in allDeals" :key="deal.id"> 
            <div class="dealcard">
                <deal :deal='deal' class='deal'/>
            </div>
        </li>
    </ul>
    <h1>TOTAL of pending: </h1>{{total}}
    </span>
  </div>
  </div>
</template>
<script>
import * as axioshelpers from '../axioshelpers'

import Deal from './Deal.vue'

export default {
  name: 'DealsPending',
  data: function(){
      return ({loading: 1, allDeals:this.getPendingDeals(), total:0})
  },
  created: function () {
      this.allDeals = this.getPendingDeals()
  },
  methods: {
    getPendingDeals: function() {
      axioshelpers.getAllDeals()
      .then(response => {
        this.allDeals = response.data['items'].filter( (deal) => deal.dealState=='PENDING')
        this.allDeals.forEach( (d) => this.total += d.amount)
        this.loading = 0
      })
      .catch(e => {
        console.log(e)
      })
    }
  },
  components: {
      // <my-component> will only be available in parent's template
      'deal': Deal 
    },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
