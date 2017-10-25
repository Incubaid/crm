<template>
  <div>
    <h1>List of Deals</h1>
    <ul>
        <li v-for="(deal, idx) in allDealsAxios" :key="deal.id"> 
            <div class="dealcard">
                <deal :deal='deal' class='deal'/>
            </div>
        </li>
    </ul>
  </div>
  </div>


</template>
<script>

const myq = `
  query allDeals {
    deals(first:3){
      edges{
        node{
          id,
          name,
          amount
        }
      }
    }
  }

`
import axios from 'axios';
import Deal from './Deal.vue'

export default {
  name: 'Reports',
  data: function(){
      return ({allDeals: {}, loading: 0, allDealsAxios:this.getAllDeals()})
  },
  methods: {
    getAllDeals: function() {
      axios.post(`http://localhost:5000/api`, {'query': myq }, {'headers':{'Content-Type':'application/json'}})
      .then(response => {
        this.allDealsAxios = response.data['items']
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
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
