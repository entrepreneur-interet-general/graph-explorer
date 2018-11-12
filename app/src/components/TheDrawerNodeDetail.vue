<template>
  <div id="drawer-links-detail">
    <div class="table">
      <div class="table-row">
        <label class="table-cell">Total reçu</label>
        <span class="table-cell">
          {{ money_in }}
        </span>
      </div>
      <div class="table-row">
        <label class="table-cell">Total envoyé</label>
        <span class="table-cell">
          {{ money_out }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['focusNode']),
    money_in() {
      const m = parseInt(this.focusNode.in_degree_weighted, 10);
      return m.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' });
    },
    money_out() {
      const m = parseInt(this.focusNode.out_degree_weighted, 10);
      return m.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' });
    }
  }
};
</script>

<style scoped lang="scss">
@import "../scss/settings.scss";

#drawer-links-detail {
  padding-left: 6px;
  padding-right: 16px;
  padding-top: 20px;
  padding-bottom: 20px;

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
    max-width: 80px;
  }

  .md-button {
    border: solid 1px $silver;
    margin: 0;
    margin-top: 10px;
    margin-left: 10px;
  }
}
</style>
