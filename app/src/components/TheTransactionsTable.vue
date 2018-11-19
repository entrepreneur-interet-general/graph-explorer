<template>
  <div
    v-show="columns"
    id="modal-links-detail">
    <app-table
      :columns="columns"
      :rows="rows"/>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import AppTable from './AppTable.vue';
import { SHOW_PROGRESS_SPINNER, HIDE_PROGRESS_SPINNER } from '../mutation-types';
import api from '../api';

export default {
  components: { AppTable },

  data() {
    return {
      columns: [],
      rows: []
    };
  },
  computed: {
    ...mapState(['focusNodeEntity', 'G'])
  },
  mounted() {
    const H = this.G.toUndirected();
    const neighbors = H.neighbors(this.focusNodeEntity);
    const entities = neighbors.concat([this.focusNodeEntity]);
    const options = { data: { entities } };
    const vm = this;
    vm.SHOW_PROGRESS_SPINNER();
    api.transactions(options, (transactions) => {
      if (transactions.length > 0) {
        vm.columns = Object.keys(transactions[0]);
        vm.rows = transactions.map((transaction) => {
          const row = [];
          vm.columns.forEach((column) => {
            row.push(transaction[column]);
          });
          return row;
        });
      }
      vm.HIDE_PROGRESS_SPINNER();
    });
  },
  methods: {
    ...mapMutations([SHOW_PROGRESS_SPINNER, HIDE_PROGRESS_SPINNER])
  }
};
</script>

<style lang="scss">
#modal-links-detail {
  margin: auto;
  max-width: 90%;
  max-height: 90%;
  overflow: scroll;
}
</style>
