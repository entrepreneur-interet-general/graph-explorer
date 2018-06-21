<template>

  <div class="drawer-links-detail">
    <div class="focus-node-links-details">
      <div>{{focusNode.degree + " links"}}</div>
      <md-button class="md-small" @click="SHOW_MODAL">DETAIL</md-button>
    </div>
  </div>
  
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
import { SHOW_MODAL } from '../mutation-types'

export default {
  computed: {
    ...mapGetters(["focusNode"])
  },
  methods: {
    ...mapMutations([SHOW_MODAL])
  }
}
</script>

<style lang="scss">

  @import "../scss/settings.scss";

  .focus-node-links-details {
    padding-left: 16px;
    padding-right: 16px;
    padding-top: 15px;
    display: flex;
    align-items: center;

  }

  .focus-node-links-details > .md-button {
    // position: relative;
    // top: -15px;
    border: solid 1px $silver;
    margin-left: 30px;
    text-align: center;
  }



 


</style>

