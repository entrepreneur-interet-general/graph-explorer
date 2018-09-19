<template>
    <div id="drawer" v-bind:style="drawerStyle" v-if="focusNodeEntity">
      <drawer-toggle-button @click="toggleDrawer" v-bind:expanded="drawerExpanded"></drawer-toggle-button>
      <drawer-title></drawer-title>
      <drawer-controls></drawer-controls> 
      <drawer-node-properties></drawer-node-properties>
      <drawer-links-detail></drawer-links-detail>
    </div>
</template>

<script>
import { mapState } from 'vuex';
import DrawerToggleButton from './DrawerToggleButton.vue';
import DrawerTitle from './DrawerTitle.vue';
import DrawerControls from './DrawerControls.vue';
import DrawerNodeProperties from './DrawerNodeProperties.vue';
import DrawerLinksDetail from './DrawerLinksDetail.vue';

export default {
  components: { DrawerToggleButton, DrawerTitle, DrawerControls, DrawerNodeProperties, DrawerLinksDetail },
  data() {
    return {
      drawerExpanded: true
    };
  },
  computed: {
    drawerStyle() {
      return {
        width: this.drawerExpanded ? "380px" : "0px"
      }
    },
    ...mapState(['focusNodeEntity'])
  },
  methods: {
    toggleDrawer() {
      this.drawerExpanded = !this.drawerExpanded;
      if (this.drawerExpanded) {
        this.$root.$emit("drawer-expanded");
      } else {
        this.$root.$emit("drawer-collapsed");
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


