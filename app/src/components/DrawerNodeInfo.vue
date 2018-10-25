<template>
  <div>
    <drawer-node-info-title></drawer-node-info-title>
    <drawer-node-info-controls></drawer-node-info-controls> 
    <drawer-node-info-properties></drawer-node-info-properties>
    <drawer-node-info-detail></drawer-node-info-detail>
  </div>
</template>

<script>
import DrawerNodeInfoTitle from './DrawerNodeInfoTitle.vue';
import DrawerNodeInfoControls from './DrawerNodeInfoControls.vue';
import DrawerNodeInfoProperties from './DrawerNodeInfoProperties.vue';
import DrawerNodeInfoDetail from './DrawerNodeInfoDetail.vue';

export default {
  name: "drawer-node-info",
  components: { DrawerNodeInfoTitle, DrawerNodeInfoControls, DrawerNodeInfoProperties, DrawerNodeInfoDetail },
}
</script>

<style lang="scss">

</style>
