<template>
  <div class="share-button">
    <md-button @click="handleClick">
      <md-icon>share</md-icon>
    </md-button>
  </div>
</template>

<script>
import { saveSvgAsPng } from 'save-svg-as-png';

export default {
  methods: {
    handleClick(){
      saveSvgAsPng(document.getElementById("graph"), "graph.png", {scale: 2});
    }
  }
}
</script>

<style>

.share-button {
  position: absolute;
  right: 30px;
  top: 30px;
}

.share-button .md-button {
  display: block;
  height: 30px;
  width: 30px;
  min-width: 0;
  position: relative;
  margin: 0;
  border-radius: 0;
  padding: 0;
}

</style>
