<template>
  <div id="app">
    <search></search>
    <!-- <filter-list></filter-list> -->
    <drawer v-if="showDrawer">
      <drawer-search-results v-if="showDrawerSearchResults"></drawer-search-results>
      <drawer-node-info v-else-if="showDrawerNodeInfo"></drawer-node-info>
    </drawer>
    <graph></graph>
    <zoom-widget v-if="showGraphWidgets"></zoom-widget>
    <the-button-download v-if="showGraphWidgets"></the-button-download>
    <progress-spinner v-show="showProgressSpinner"></progress-spinner>
  </div>
</template>

<script>
import Search from "./Search.vue";
import FilterList from "./FilterList.vue";
import Drawer from "./Drawer.vue";
import DrawerNodeInfo from "./DrawerNodeInfo";
import DrawerSearchResults from "./DrawerSearchResults";
import Graph from "./Graph.vue";
import ZoomWidget from "./ZoomWidget.vue";
import TheButtonDownload from "./TheButtonDownload.vue";
import ProgressSpinner from "./ProgressSpinner";
import { mapActions, mapState, mapGetters } from 'vuex';


export default {
  name: "app",
  components: { Search, FilterList, Drawer, Graph, ZoomWidget, TheButtonDownload, 
    ProgressSpinner, DrawerNodeInfo, DrawerSearchResults },
  computed: {
    filter() {
      return this.$store.state.filter;
    },
    ...mapState(["showModal", "showProgressSpinner", "showDrawerSearchResults"]),
    ...mapGetters(["showGraphWidgets", "showDrawer", "showDrawerNodeInfo"])
  },
  methods: {
    ...mapActions(['expand'])
  },
  mounted() {
    // this.expand(19336) // 19336 = Jill Sanchez, 23709 Jasmine Calderon 
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
</style>
