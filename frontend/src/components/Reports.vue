<template>
  <div>
    <h1>{{ msg }}</h1>
     <ul>
      <li><a href="https://localhost:10000/" target="_blank">CRM</a></li>
      <li><a href="https://vuejs.org" target="_blank">total funding received & from who </a></li>
      <li><a href="https://forum.vuejs.org" target="_blank">show open pending amount for investors </a></li>
      <li><a href="https://chat.vuejs.org" target="_blank">Example query</a></li>
     </ul>

  <div class="deals">
    <template v-if="loading > 0">
        Loading...
    </template>

    <template v-else>
      {{allDeals}} IN ELSE
    </template>

  </div>
  </div>


</template>
<script>
import gql from 'graphql-tag'
  // GraphQL query
const DealsQuery = gql`
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

export default {
  name: 'Reports',
  data () {
    return {
      msg: 'Welcome to CRM reports',
      allDeals: {}
    }
  },
  apollo: {
    allDeals: {
      query: DealsQuery,
      loadingKey: 'loading'
    }
  }
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
