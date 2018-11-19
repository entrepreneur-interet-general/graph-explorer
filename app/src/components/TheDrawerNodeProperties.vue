<template>
  <div id="drawer-node-properties">
    <div class="table">
      <div
        v-for="property in properties"
        :key="property.key"
        class="table-row">
        <label
          :for="property.key"
          class="table-cell" >{{ property.label }}</label>
        <span
          :id="property.key"
          class="table-cell">
          {{ focusNode[property.key] }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      properties: [
        { key: 'prenom', label: 'Prénom' },
        { key: 'nom', label: 'Nom' },
        { key: 'date_naissance', label: 'Date de naissance' },
        { key: 'pays_code', label: 'Pays' },
        { key: 'code_postal', label: 'Code postal' },
        { key: 'telephone', label: 'Téléphone' },
        { key: 'numero_piece_identite', label: 'ID' }
      ]
    };
  },
  computed: {
    ...mapGetters(['focusNode'])
  }
};
</script>

<style scoped lang="scss">
@import "../scss/settings.scss";

#drawer-node-properties {
  padding-left: 6px;
  padding-right: 16px;
  padding-top: 20px;
  padding-bottom: 20px;
  border-bottom: solid 1px $clouds;

  .table {
    display: table;
    border-collapse: separate;
    border-spacing: 10px;
    width: 100%;
    padding-right: 0;
  }

  .table-row {
    display: table-row;
    width: 100%;
    padding: 0;
  }

  .table-cell {
    display: table-cell;
    overflow: hidden;
    white-space: nowrap;
    max-width: 130px;
  }
}
</style>
