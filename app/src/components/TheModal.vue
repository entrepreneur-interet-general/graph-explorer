<template>
  <div
    class="modal"
    @click.stop="handleModalClicked">
    <slot/>
  </div>
</template>

<script>
import { mapMutations } from 'vuex';
import { HIDE_MODAL } from '../mutation-types';

export default {
  methods: {
    handleModalClicked(event) {
      if (event.target.getAttribute('class') === 'modal') {
        this.HIDE_MODAL();
      }
    },
    ...mapMutations([HIDE_MODAL])
  }
};
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
