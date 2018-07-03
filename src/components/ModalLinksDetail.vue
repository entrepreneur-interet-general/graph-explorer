<template>
  <div id="modal-links-detail">
    <app-table :columns="columns" :data="transactions" :searchQuery="searchQuery"></app-table>
  </div>
</template>

<script>
import AppTable from './AppTable.vue';
import { mapGetters } from 'vuex';

export default {
  components: { AppTable },
  
  data() {

    const columns = [
      "date",
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
      columns: columns
    }
  },
  computed: {
    ...mapGetters(["focusNodeLinks"]),
    transactions() {
      let allTransactions = [];
      this.focusNodeLinks.forEach(link => {
        allTransactions.push(...link['transactions'])
      });
      return allTransactions;
    }
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
