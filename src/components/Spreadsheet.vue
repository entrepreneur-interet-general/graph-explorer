<template>
  <div id="hot-preview">
    <HotTable :root="root" :settings="hotSettings"></HotTable>
  </div>
</template>

<script>
import HotTable from '@handsontable/vue';

export default {
  data() {
    return {
      root: 'hot-preview',
      hotSettings: {
        data: [['cos_oper_prenom', 'cos_oper_nom'],['Jill', 'Sanchez']],
        colHeaders: true,
        readOnly: true,
      }
    }
  },
  components: { HotTable }
}
</script>

<style lang="scss">
@import "../../node_modules/handsontable/dist/handsontable.full.css";

#hot-preview {
  width: 600px;
  height: 400px;
  overflow: hidden;
}
</style>

