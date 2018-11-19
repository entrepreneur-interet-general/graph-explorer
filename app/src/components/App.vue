<template>
  <div id="app">
    <the-search/>
    <the-drawer v-if="showDrawer"/>
    <the-graph/>
    <the-zoom-widget v-if="showGraphWidgets"/>
    <the-button-download v-if="showGraphWidgets"/>
    <the-progress-spinner v-show="showProgressSpinner"/>
    <the-modal v-if="showModal">
      <the-transactions-table/>
    </the-modal>
    <the-navigation
      :app-name="config.appName"
      :help-url="config.helpUrl"/>
  </div>
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex';
import TheSearch from './TheSearch.vue';
import TheDrawer from './TheDrawer.vue';
import TheGraph from './TheGraph.vue';
import TheZoomWidget from './TheZoomWidget.vue';
import TheButtonDownload from './TheButtonDownload.vue';
import TheProgressSpinner from './TheProgressSpinner.vue';
import TheModal from './TheModal.vue';
import TheTransactionsTable from './TheTransactionsTable.vue';
import TheNavigation from './TheNavigation.vue';

export default {
  name: 'App',
  components: {
    TheSearch,
    TheDrawer,
    TheGraph,
    TheZoomWidget,
    TheButtonDownload,
    TheProgressSpinner,
    TheModal,
    TheTransactionsTable,
    TheNavigation
  },
  data() {
    const configElement = document.getElementById('config');
    const config = JSON.parse(configElement.innerHTML);
    return { config };
  },
  computed: {
    filter() {
      return this.$store.state.filter;
    },
    ...mapState(['showModal', 'showProgressSpinner', 'showDrawerSearchResults', 'showNavigation']),
    ...mapGetters(['showGraphWidgets', 'showDrawer'])
  },
  methods: {
    ...mapActions(['expand'])
  }
};
</script>

<style lang="scss">
@import "../scss/settings.scss";
@import "../scss/fonts.scss";

html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
}

#app {
  font-family: "Roboto Mono", monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 0;
  height: 100%;
}

#toto {
  position: absolute;
  left: 400px;
  top: 100px;
  z-index: 10;
  background-color: black;
}
</style>
