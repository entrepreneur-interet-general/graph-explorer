<template>
  <button id="drawer-toggle-button" v-bind:style="toggleButtonStyle" @click="handleClick">
    <div class="caret" v-bind:style="caretStyle"></div>
  </button>
</template>

<script>
export default {
  props: {
    expanded: Boolean
  },
  computed: {
    toggleButtonStyle() {
      return {
        'left': this.expanded ? "380px": "0px"
      }
    },
    caretStyle() {
      return {
        'border-right': this.expanded ? "5px solid black" : "none",
        'border-left': this.expanded ? "none" : "5px solid black"
      }
    }
  },
  methods: {
    handleClick(){
      this.$emit("click");
    }
  }
}
</script>

<style lang="scss">

@import "../scss/settings.scss";

#drawer-toggle-button {
  position: fixed;
  top: 20px;
  padding: 0;
  -webkit-transition: left 200ms; /* Safari */
  transition: left 200ms;
  height: 48px;
  width: 20px;
  background-color: $clouds;
  text-align: center;

  .caret {
    width: 0; 
    height: 0; 
    border-top: 5px solid transparent;
    border-bottom: 5px solid transparent; 
    -webkit-transition: border-left 200ms; /* Safari */
    transition: border-left 200ms;
    -webkit-transition: border-right 200ms; /* Safari */
    transition: border-right 200ms;
    margin: auto;
  }
}

#drawer-toggle-button:hover {
  cursor: pointer;
}

</style>

