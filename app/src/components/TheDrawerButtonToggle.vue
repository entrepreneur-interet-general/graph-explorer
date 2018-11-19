<template>
  <button
    id="drawer-toggle-button"
    :class="[expanded ? 'expanded' : 'collapsed']"
    @click="handleClick">
    <div class="caret"/>
  </button>
</template>

<script>
export default {
  props: {
    expanded: {
      default: true,
      type: Boolean
    }
  },
  methods: {
    handleClick() {
      this.$emit('toggleDrawer');
    }
  }
};
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

.expanded {
  left: 380px;
  .caret {
    border-right: 5px solid black;
    border-left: none;
  }
}

.collapsed {
  left: 0px;
  .caret {
    border-right: none;
    border-left: 5px solid black;
  }
}
</style>
