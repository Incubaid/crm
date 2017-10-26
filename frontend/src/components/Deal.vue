
<template>
  <div class='container'>
  <div><span><a v-bind:href="deal.uid">{{deal.uid}}</a> / {{ deal.name }} ( {{deal.amount}} ) : {{deal.dealState}} <span v-if="deal.contact">{{deal.contact['firstname'] + " " +  deal.contact['lastname']}}</span>
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
          return {id: '', uid: '', name: '', amount: '', dealState:'', contact:{}}
        }
      }
    }
  }
</script>
<style>
/* Add some padding inside the card container */
.container {
    padding: 2px 16px;
    margin:10px;
}
</style>