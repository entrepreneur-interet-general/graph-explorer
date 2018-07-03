<template>
  <div id="drawer-title">
    <div id="drawer-title-content" class="md-title">
      {{focusNode.prenom_nom}} {{`#${focusNode.entity}`}}
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['focusNode'])
  }

}
</script>

<style lang="scss">

@import "../scss/settings.scss";

#drawer-title {
  margin-top: 87px;
  background-color: $peter-river;
  color: white;
  min-width: 0;
}

#drawer-title-content {
  padding-left: 16px;
  padding-right: 16px;
  padding-top: 20px;
  padding-bottom: 20px;
}

</style>

