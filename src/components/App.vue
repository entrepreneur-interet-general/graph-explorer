<template>
  <div id="app">
    <search></search>
    <filter-list></filter-list>
    <drawer></drawer>
    <graph></graph>
    <zoom-widget></zoom-widget>
    <!-- <modal>
      <spreadsheet></spreadsheet>
    </modal> -->
  </div>
</template>

<script>
import Search from "./Search.vue";
import FilterList from "./FilterList.vue";
import Drawer from "./Drawer.vue";
import Graph from "./Graph.vue";
import ZoomWidget from "./ZoomWidget.vue";
import Modal from "./Modal.vue";
import Spreadsheet from "./Spreadsheet.vue";
import { mapActions } from 'vuex';

export default {
  name: "app",
  components: {Search, FilterList, Drawer, Graph, ZoomWidget, Modal, Spreadsheet },
  computed: {
    filter() {
      return this.$store.state.filter;
    }
  },
  methods: {
    ...mapActions(['expand'])
  },
  mounted() {
    //this.expand(19336) // 19336 = Jill Sanchez, 23709 Jasmine Calderon 
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
