<template>
  <div class="modal">
    <slot></slot>
  </div>
</template>

<script>
export default {

}
</script>

<style lang="scss">
  /* The Modal (background) */
  .modal {
      position: fixed; /* Stay in place */
      z-index: 3; /* Sit on top */
      left: 0;
      top: 0;
      width: 100%; /* Full width */
      height: 100%; /* Full height */
      overflow: auto; /* Enable scroll if needed */
      background-color: rgb(0,0,0); /* Fallback color */
      background-color: rgba(0,0,0,0.5); /* Black w/ opacity */
  }
</style>

