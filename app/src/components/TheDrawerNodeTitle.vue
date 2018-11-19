<template>
  <div
    id="drawer-title"
    class="md-title">
    {{ focusNode.prenom_nom }} #{{ focusNode.entity }}
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['focusNode'])
  }
};
</script>

<style scoped lang="scss">
@import "../scss/settings.scss";

#drawer-title {
  margin-top: 110px;
  background-color: $peter-river;
  color: white;
  padding-left: 16px;
  padding-right: 16px;
  padding-top: 20px;
  padding-bottom: 20px;
}

</style>
