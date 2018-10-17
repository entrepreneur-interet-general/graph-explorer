<template>
  <div id="search-container" v-on:keyup.enter="handleSubmit">
    <md-autocomplete id="search" 
      v-model="value" 
      :md-options="people" 
      md-layout="box" 
      @md-changed="handleChange" 
      autofocus 
      @md-selected="handleSelected" 
      v-bind:class="{'search-hidden': !isVisible}"> 
      <label>Rechercher</label>
      <md-icon id="ic-search">search</md-icon>
      <template slot="md-autocomplete-item" slot-scope="{ item, term }">
        {{ item.prenom_nom + " #" + item.entity}}
      </template>
    </md-autocomplete>
    <div id="back-to-results" v-if="showBackToResults" @click="SHOW_DRAWER_SEARCH_RESULTS">
      <a>Retours aux résultats</a>
    </div>
  </div>
</template>

<script>
import api from "../api";
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { debounce } from '../utils';
import { UPDATE_SEARCH_RESULTS, SHOW_DRAWER_SEARCH_RESULTS, HIDE_DRAWER_SEARCH_RESULTS } from '../mutation-types';

const debouncedSearch = debounce(api.search, 800, {leading: true});

export default {
  data() {
    return {
      isVisible: true,
      value: null,
      selected: null,
      people: []
    };
  },
  computed: {
    ...mapGetters(['showBackToResults'])
  },
  methods: {
    handleChange(searchTerm) {
      if (searchTerm === "") {
        this.UPDATE_SEARCH_RESULTS([]);
      }
      const options = { params: { search_term: searchTerm } };
      this.people = debouncedSearch(options);
    },
    handleSelected(person){
      this.UPDATE_SEARCH_RESULTS([]);
      this.value = person.prenom_nom;
      this.expand(person.entity);
    },
    handleSubmit(){
      document.activeElement.blur();
      if (this.value != "") {
        this.search(this.value);
      }
    },  
    ...mapActions(['expand', 'search']),
    ...mapMutations([UPDATE_SEARCH_RESULTS, SHOW_DRAWER_SEARCH_RESULTS])
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

#search-container {
  position: absolute;
  left: 16px;
  top: 16px;
}

#back-to-results {
  position: relative;
  top: -24px;
  z-index: 3;
  border-left: solid 1px $silver;
  border-right: solid 1px $silver;
  border-bottom: solid 1px $silver;
  padding: 4px;
  font-size: 12px;
  color: $peter-river;
  background-color: white;
}

#back-to-results:hover {
  cursor: pointer;
  text-decoration: underline;
}

#search {
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
  position: absolute;
  top: 75px !important;
}

.md-autocomplete-box-content:after {
  border-bottom: none;
}

.md-menu-item {
  background-color: white;
}

.md-list-item-button, .md-list-item-content {
  height: 50px !important;
}

.md-menu-item:hover {
  background-color: $turquoise;
}

.search-hidden {
  display: none
}



</style>

