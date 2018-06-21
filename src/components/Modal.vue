<template>
  <div class="modal" @click="handleModalClicked">
    <slot></slot>
  </div>
</template>

<script>
import { HIDE_MODAL } from '../mutation-types.js'
import { mapMutations } from 'vuex'; 

export default {
  methods: {
    handleModalClicked(event) {
      if(event.target.getAttribute("class") == "modal"){
        this.HIDE_MODAL();
      }
    },
    ...mapMutations([HIDE_MODAL])
  }
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
    display: flex;
    align-items: center;
  }
</style>

