<template>
  <div>
    <h1>{{ msg }}</h1>
     <ul>
      <li><a href="http://localhost:5000/" target="_blank">CRM</a></li>
     </ul>
  </div>
  </div>


</template>
<script>

import axios from 'axios';
export default {
  name: 'Home',
  data: function(){
      msg:'Welcome to CRM home'
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
