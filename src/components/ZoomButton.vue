<template>
  <div class="zoom-button">
  <md-button @click="handleClick" id="widget-zoom-out">
    <md-icon><slot></slot></md-icon>
  </md-button>
  </div>
</template>

<script>
export default {
  methods: {
    handleClick(){
      this.$emit("click")
    }
  }
}
</script>

<style>

</style>
