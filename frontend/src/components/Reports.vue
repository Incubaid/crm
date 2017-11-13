<template>
  <div>
    <h1>{{ msg }}</h1>
    <router-link to="/deals">All Deals</router-link>
    <router-link to="pendingdeals">All pending deals</router-link>
    <router-view></router-view>
  </div>
  </div>


</template>
<script>
export default {
  name: 'Reports',
  data: function(){
      return ({msg:"Welcome to reporter"})
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
