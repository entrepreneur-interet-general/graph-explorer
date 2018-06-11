<template>
  <md-autocomplete id="search" v-model="value" :md-options="people" md-layout="box" @md-changed="search" autofocus @md-selected="handleSelected" v-bind:class="{ 'search-visible': isVisible, 'search-hidden': !isVisible }"> 
    <label>Rechercher</label>
    <md-icon id="ic-search">search</md-icon>
    <template slot="md-autocomplete-item" slot-scope="{ item, term }">
      <md-highlight-text :md-term="term">{{ item.prenom_nom + " #" + item.entity}}</md-highlight-text>
    </template>
  </md-autocomplete>
</template>

<script>
import api from "../api";
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      isVisible: true,
      value: null,
      selected: null,
      people: []
    };
  },
  methods: {
    search(searchTerm) {
      this.people = api.search(searchTerm);
    },
    handleSelected(person){
      this.value = person.prenom_nom;
      this.expand(person.entity)
    },
    ...mapActions(['expand'])
  },
  mounted() {
    const vm = this;
    vm.$root.$on("drawer-expanded", () => {
      vm.isVisible = true;
    })
    vm.$root.$on("drawer-collapsed", () => {
      vm.isVisible = false;
    })
  }
};
</script>

<style lang="scss">
@import "../scss/settings.scss";

#search {
  position: absolute;
  left: 16px;
  top: 16px;
  width: 350px;
  box-shadow: none !important;
  border: solid 1px $silver;
  z-index: 3;
  -webkit-transition: opacity 200ms; /* Safari */
  transition: opacity 200ms;
}

#ic-search {
  position: absolute;
  left: 5px;
  top: 8px;
  color: $silver;
}

#search:focus-within {
  border: solid 1px $turquoise;
}

#search:focus-within i {
  color: $turquoise;
}

#search button .md-icon {
  color: $turquoise;
}

#search input {
  border: none;
  padding-left: 40px !important;
}

#search label {
  color: $silver;
  left: 40px !important;
}

.md-menu-content {
  max-height: 300px !important;
}

.md-autocomplete-box-content:after {
  border-bottom: none;
}

.md-menu-item:hover {
  background-color: $turquoise;
}

.search-hidden {
  opacity: 0;
}

.search-visible {
  opacity: 1;
}
</style>

