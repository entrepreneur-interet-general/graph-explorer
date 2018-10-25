<template>
    <div id="drawer" v-bind:style="drawerStyle">
      <drawer-toggle-button @click="toggleDrawer" v-bind:expanded="drawerExpanded"></drawer-toggle-button>
      <slot></slot>
    </div>
</template>

<script>
import { mapState } from 'vuex';
import DrawerToggleButton from './DrawerToggleButton.vue';

export default {
  components: { DrawerToggleButton },
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


