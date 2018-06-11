<template>

  <div class="drawer-links-detail">
    <div class="focus-node-links-details">
      <div>{{focusNode.degree + " links"}}</div>
      <md-button class="md-small">DETAIL</md-button>
    </div>
    <!-- <div class="table">
      <div class="table-row" v-for="link in focusNodeLinks">
        <span class="table-cell">{{link.source.prenom + " " + link.source.nom}}</span>
        <i class="table-cell material-icons">arrow_right_alt</i>
        <span class="table-cell">{{link.target.prenom + " " + link.target.nom}}</span>
      </div>
    </div> -->
  </div>
  
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(["focusNode"])
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

