<template>
  <div
    id="drawer"
    :style="drawerStyle">
    <the-drawer-button-toggle
      :expanded="drawerExpanded"
      @toggleDrawer="toggleDrawer"/>
    <the-drawer-search-results-list v-if="showDrawerSearchResults"/>
    <div v-else-if="showDrawerNodeInfo">
      <the-drawer-node-title/>
      <the-drawer-node-controls/>
      <the-drawer-node-properties/>
      <the-drawer-node-detail/>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import TheDrawerButtonToggle from './TheDrawerButtonToggle.vue';
import TheDrawerSearchResultsList from './TheDrawerSearchResultsList.vue';
import TheDrawerNodeTitle from './TheDrawerNodeTitle.vue';
import TheDrawerNodeControls from './TheDrawerNodeControls.vue';
import TheDrawerNodeProperties from './TheDrawerNodeProperties.vue';
import TheDrawerNodeDetail from './TheDrawerNodeDetail.vue';


export default {
  components: {
    TheDrawerButtonToggle,
    TheDrawerSearchResultsList,
    TheDrawerNodeTitle,
    TheDrawerNodeControls,
    TheDrawerNodeProperties,
    TheDrawerNodeDetail
  },
  data() {
    return {
      drawerExpanded: true
    };
  },
  computed: {
    drawerStyle() {
      return { width: this.drawerExpanded ? '380px' : '0px' };
    },
    ...mapState(['focusNodeEntity', 'showDrawerSearchResults']),
    ...mapGetters(['showDrawerNodeInfo'])
  },
  methods: {
    toggleDrawer() {
      this.drawerExpanded = !this.drawerExpanded;
      if (this.drawerExpanded) {
        this.$root.$emit('drawer-expanded');
      } else {
        this.$root.$emit('drawer-collapsed');
      }
    }
  }
};
</script>

<style lang="scss">
@import "../scss/settings.scss";

#drawer {
  position: fixed;
  height: 100%;
  border-left: none;
  -webkit-transition: width 200ms; /* Safari */
  transition: width 200ms;
  border-right: 1px solid $clouds;
  z-index: 2;
  overflow-x: hidden;
  background-color: white;
}
</style>
