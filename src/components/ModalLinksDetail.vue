<template>
  <div v-show="transactions" id="modal-links-detail">
    <app-table :columns="columns" :data="transactions" :searchQuery="searchQuery"></app-table>
  </div>
</template>

<script>
import AppTable from './AppTable.vue';
import { mapGetters, mapMutations } from 'vuex';
import { SHOW_PROGRESS_SPINNER, HIDE_PROGRESS_SPINNER } from "../mutation-types";
import api from '../api';

export default {
  components: { AppTable },
  
  data() {

    const columns = [
      "date_operation",
      "valeur_euro",
      "don_entity",
      "don_prenom",
      "don_nom",
      "don_date_naissance",
      "don_telephone",
      "don_numero_piece_identite",
      "don_pays",
      "don_pays_code",
      "don_code_postal",
      "ben_entity",
      "ben_prenom",
      "ben_nom",
      "ben_date_naissance",
      "ben_telephone",
      "ben_numero_piece_identite",
      "ben_pays",
      "ben_pays_code",
      "ben_code_postal",
    ]

    return {
      searchQuery: '',
      columns: columns,
      transactions: []
    }
  },
  mounted() {
    const options = { params: { node: 19336 } };
    const vm = this;
    vm.SHOW_PROGRESS_SPINNER()
    api.transactions(options, data => {
      vm.transactions = data;
      vm.HIDE_PROGRESS_SPINNER();
    })
  },
  computed: {
    ...mapGetters(["focusNodeLinks"]),
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
