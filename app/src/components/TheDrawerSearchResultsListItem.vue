<template>
  <div
    class="search-result-list-item"
    @click="handleClick">
    <div class="search-result-list-item-content">
      <div>
        <span>{{ prenom }} {{ nom }} #{{ entity }}</span>
        <md-icon v-if="star">star</md-icon>
      </div>
      <div>Code postal: {{ code_postal }} {{ pays_code }}</div>
      <div>ID n° {{ numero_piece_identite }}</div>
      <div>{{ degree > 1 ? liens : lien }} liens</div>
    </div>
  </div>
</template>

<script>

import { mapActions } from 'vuex';

export default {
  props: {
    prenom: {
      type: String,
      default: ''
    },
    nom: {
      type: String,
      default: ''
    },
    entity: {
      type: String,
      default: ''
    },
    code_postal: {
      type: String,
      default: ''
    },
    pays_code: {
      type: String,
      default: ''
    },
    numero_piece_identite: {
      type: String,
      default: ''
    },
    star: {
      type: String,
      default: ''
    },
    degree: {
      type: String,
      default: ''
    }
  },
  methods: {
    handleClick() {
      this.expand(this.entity);
    },
    ...mapActions(['expand'])
  }
};
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
