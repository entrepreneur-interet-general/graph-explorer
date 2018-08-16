<template>
  <div id="drawer-controls" class="md-layout">
    <md-button class="md-layout-item" @click=handleExpandClicked>
      <div ><md-icon>unfold_more</md-icon></div>
      <div>ÉTENDRE</div>
    </md-button>
    <md-button class="md-layout-item" @click=handleHideClicked>
      <div><md-icon>visibility_off</md-icon></div>
      <div>CACHER</div>
    </md-button>
    <md-button class="md-layout-item" @click=handleCollapseClicked>
      <div><md-icon>unfold_less</md-icon></div>
      <div>REPLIER</div>
    </md-button>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  computed: {
    ...mapState(["focusNodeEntity"])
  },
  methods: {
    handleExpandClicked() {
      this.expand(this.focusNodeEntity);
    },
    handleHideClicked(){
      this.hide(this.focusNodeEntity);
    },
    handleCollapseClicked(){
      this.collapse(this.focusNodeEntity);
    },
    ...mapActions(['expand', 'hide', 'collapse'])
  }
}
</script>

<style lang="scss">

@import "../scss/settings.scss";

#drawer-controls {
  width: 100%;
  border-bottom: solid 1px $clouds;
  height: 80px;

  .md-button {
    margin: 0;
    height: 100%;
    min-width: 0;
  }

  .md-button-content {
    margin: 0;
    padding: 0;
  }

}

</style>

