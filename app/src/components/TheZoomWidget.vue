<template>
  <div id="zoom-widget">
    <app-zoom-button @click="handleClickZoomReset">zoom_out_map</app-zoom-button>
    <app-zoom-button @click="handleClickZoomIn">add</app-zoom-button>
    <app-zoom-button @click="handleClickZoomOut">remove</app-zoom-button>
  </div>
</template>

<script>
import AppZoomButton from './AppZoomButton.vue';

export default {
  components: { AppZoomButton },
  methods: {
    handleClickZoomReset() {
      this.$root.$emit('zoom-reset');
    },
    handleClickZoomIn() {
      this.$root.$emit('zoom-in');
    },
    handleClickZoomOut() {
      this.$root.$emit('zoom-out');
    }
  }
};
</script>

<style scoped lang="scss">
#zoom-widget {
  position: absolute;
  right: 16px;
  bottom: 16px;

  .zoom-button:first-of-type {
    margin-bottom: 5px;
  }

  .zoom-button:nth-of-type(3) {
    border-top: none;
  }
}
</style>
