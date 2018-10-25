<template>
  <div class="search-result-list-item" @click="handleClick">
    <div class="search-result-list-item-content">
      <div>
        <span>{{prenom}} {{nom}} #{{entity}}</span> 
        <md-icon v-if="star">star</md-icon>
      </div>
      <div>Code postal: {{code_postal}} {{pays_code}}</div>
      <div>ID n° {{numero_piece_identite}}</div>
      <div v-if="degree > 1">{{degree}} liens</div>
      <div v-else>{{degree}} lien</div>
    </div>
  </div>
</template>

<script>

import { mapActions, mapMutations } from 'vuex';

export default {
  props: ['prenom', 'nom', 'entity', 'code_postal', 'pays_code', 'numero_piece_identite', 'star', 'degree'],
  methods: {
    handleClick(){
      this.expand(this.entity);
    },
    ...mapActions(['expand'])
  }
}
</script>

<style lang="scss">

  @import "../scss/settings.scss";

  .search-result-list-item:first-of-type {
    border-top: 1px solid $clouds;
  } 

  .search-result-list-item {

    padding-top: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid $clouds;
    padding-left: 16px;

    .md-icon {
      margin: 0px;
      font-size: 18px !important;
      position: relative;
      top: -2px;
      color:black !important;
    }

    .md-button {
     border: solid 1px black; 
    }
  }

  .search-result-list-item:hover {
    background-color: $clouds;
    cursor: pointer;
  }

  .search-result-list-item-content {
    flex-grow: 8
  }

  .search-result-list-item-content div:first-child {
    font-weight: bold;
  } 

</style>
