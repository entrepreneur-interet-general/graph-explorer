<template>
  <div class="zoom-button">
    <md-button @click="handleClick">
      <md-icon>
        <slot />
      </md-icon>
    </md-button>
  </div>
</template>

<script>
export default {
  methods: {
    handleClick() {
      this.$emit('click');
    }
  }
};
</script>

<style scoped lang="scss">
.zoom-button {
  border: solid 1px;
  border-radius: 0;

  .md-button {
    display: block;
    height: 30px;
    width: 30px;
    min-width: 0;
    position: relative;
    margin: 0;
    padding: 0;

    :hover {
      cursor: pointer;
    }
  }
}
</style>
