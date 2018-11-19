<template>
  <div
    id="search-container"
    @:keyup.enter="handleSubmit">
    <md-autocomplete
      id="search"
      v-model="value"
      :md-options="people"
      :class="{'search-hidden': !isVisible}"
      class="search"
      md-layout="box"
      autofocus
      @md-changed="handleChange"
      @md-selected="handleSelected">
      <label>Rechercher</label>
      <md-icon id="ic-search">search</md-icon>
      <template
        slot="md-autocomplete-item"
        slot-scope="{ item, term }">
        {{ item.prenom_nom }} #{{ item.entity }}
      </template>
    </md-autocomplete>
    <div
      v-if="showBackToResults"
      id="back-to-results"
      @click="SHOW_DRAWER_SEARCH_RESULTS">
      <a>Retours aux résultats</a>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import api from '../api';
import { debounce } from '../utils';
import { UPDATE_SEARCH_RESULTS, SHOW_DRAWER_SEARCH_RESULTS } from '../mutation-types';

const debouncedSearch = debounce(api.search, 800, { leading: true });

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
  mounted() {
    const vm = this;
    vm.$root.$on('drawer-expanded', () => {
      vm.isVisible = true;
    });
    vm.$root.$on('drawer-collapsed', () => {
      vm.isVisible = false;
    });
  },
  methods: {
    handleChange(prenomNom) {
      if (prenomNom === '') {
        this.UPDATE_SEARCH_RESULTS([]);
      }
      const options = { params: { prenom_nom: prenomNom } };
      this.people = debouncedSearch(options);
    },
    handleSelected(person) {
      this.UPDATE_SEARCH_RESULTS([]);
      this.value = person.prenom_nom;
      this.expand(person.entity);
    },
    handleSubmit() {
      const vm = this;
      // clear previous searches
      vm.UPDATE_SEARCH_RESULTS([]);
      // remove focus from the search bar
      document.activeElement.blur();
      if (vm.value !== '') {
        const options = { params: { prenom_nom: vm.value } };
        api.search(options).then((results) => {
          if (results.length === 1) {
            const { entity } = results[0];
            vm.expand(entity);
          } else if (results.length > 1) {
            vm.UPDATE_SEARCH_RESULTS(results);
            vm.SHOW_DRAWER_SEARCH_RESULTS();
          }
        });
      }
    },
    ...mapActions(['expand']),
    ...mapMutations([UPDATE_SEARCH_RESULTS, SHOW_DRAWER_SEARCH_RESULTS])
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

#search {
  width: 350px;
  box-shadow: none !important;
  border: solid 1px $silver;
  z-index: 3;
  -webkit-transition: opacity 200ms; /* Safari */
  transition: opacity 200ms;
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

#search .md-input {
  border: none;
  padding-left: 40px !important;
}

#search label {
  color: $silver;
  left: 40px !important;
}

#ic-search {
  position: absolute;
  left: 5px;
  top: 8px;
  color: $silver;
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

.md-list-item-button,
.md-list-item-content {
  height: 50px !important;
}

.md-menu-item:hover {
  background-color: $turquoise;
}

.search-hidden {
  display: none;
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
</style>
