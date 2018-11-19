<template>
  <div>
    <md-drawer :md-active.sync="showNavigation">
      <md-toolbar class="md-transparent" md-elevation="0">
        <span class="md-title">{{ appName }}</span>
      </md-toolbar>
      <md-list>
        <md-list-item :href="helpUrl" target="_blank">
          <md-icon>help</md-icon>
          <span class="md-list-item-text">Aide</span>
        </md-list-item>
      </md-list>
    </md-drawer>
  </div>
</template>

<script>
export default {
  props: {
    appName: {
      type: String,
      default: ''
    },
    helpUrl: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      showNavigation: false
    };
  },
  mounted() {
    const vm = this;
    vm.$root.$on('show-navigation', () => {
      vm.showNavigation = true;
    });
  }
};
</script>

<style lang="scss" scoped>

  .md-list-item {
    cursor: pointer;
  }
</style>
