<template>
  <div v-show="columns" id="modal-links-detail">
    <app-table :columns="columns" :rows="rows" :searchQuery="searchQuery"></app-table>
  </div>
</template>

<script>
import AppTable from './AppTable.vue';
import { mapState, mapMutations } from 'vuex';
import { SHOW_PROGRESS_SPINNER, HIDE_PROGRESS_SPINNER } from "../mutation-types";
import api from '../api';

export default {
  components: { AppTable },
  
  data() {
    return {
      searchQuery: '',
      columns: [],
      rows: []
    }
  },
  mounted() {
    const options = { params: { node: this.focusNodeEntity } };
    const vm = this;
    vm.SHOW_PROGRESS_SPINNER()
    api.transactions(options, data => {
      vm.columns = data.columns;
      vm.rows = data.rows;
      vm.HIDE_PROGRESS_SPINNER();
    })
  },
  computed: {
    ...mapState(["focusNodeEntity"]),
  },
  methods: {
    ...mapMutations([SHOW_PROGRESS_SPINNER, HIDE_PROGRESS_SPINNER])
  }
}
</script>

<style lang="scss">

#modal-links-detail {
  margin: auto;
  max-width: 90%;
  max-height: 90%;
  overflow: scroll;
}

</style>
