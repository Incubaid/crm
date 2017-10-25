
<template>
  <div class='container'>
  <div><h1>{{ deal.name }}</h1> {{deal.amount}}
  </div>
  </div>
</template>

<script>
  export default {
    data: () => ({
    }),
    props: {
      deal: {
        type: Object,
        default: function () {
          return {id:'', name: '', amount: '' }
        }
      },
    },
  }
</script>
<style>
/* Add some padding inside the card container */
.container {
    padding: 2px 16px;
    margin:10px;
}
</style>