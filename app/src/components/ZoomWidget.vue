<template>
  <div id="zoom-widget">
    <zoom-button id="zoom-reset" @click="handleClickZoomReset">zoom_out_map</zoom-button>
    <zoom-button id="zoom-in" @click="handleClickZoomIn">add</zoom-button>
    <zoom-button id="zoom-out" @click="handleClickZoomOut">remove</zoom-button>
  </div>
</template>

<script>

import ZoomButton from './ZoomButton.vue';

export default {
  components: { ZoomButton },
  methods: {
    handleClickZoomReset() {
      this.$root.$emit("zoom-reset");
    },
    handleClickZoomIn() {
      this.$root.$emit("zoom-in");
    },
    handleClickZoomOut() {
      this.$root.$emit("zoom-out");
    }
  }
};
</script>

<style lang="scss">

#zoom-widget {
  position: absolute;
  right: 16px;
  bottom: 16px;

  .zoom-button .md-button {
    display: block;
    height: 30px;
    width: 30px;
    min-width: 0;
    position: relative;
    margin: 0;
    border-radius: 0;
    padding: 0;
  }

  .zoom-button:first-child {
      
    margin-bottom: 5px;
    .md-button {
      border: solid 1px;
    }
  }

  .zoom-button:nth-child(2) .md-button {
    border: solid 1px;
  }

  .zoom-button:nth-child(3) .md-button {
    border-left: solid 1px;
    border-right: solid 1px;
    border-bottom: solid 1px;
  }

  .zoom-widget .md-button:hover {
    cursor: pointer;
  }
}


</style>

