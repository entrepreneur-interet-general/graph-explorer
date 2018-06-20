<template>
  <div id="caption">
    <div class="table">
      <div class="table-row">
        <span class="table-cell france"></span>
        <span class="table-cell">FRANCE</span>
      </div>
      <div class="table-row">
        <span class="table-cell serbie"></span>
        <span class="table-cell">SERBIE</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {

}
</script>

<style lang="scss">

@import "../scss/settings.scss";

#caption {
  position: fixed;
  right: 20px;
  top: 21px;

  .table {
    display: table;
    border-collapse: separate;
    border-spacing: 10px ; 
    width: 100%;
    padding-right: 0;
  }

  .table-row {
    display: table-row;
    width: 100%;
    padding:0;
  }

  .table-cell {
    display: table-cell;
    overflow: hidden;
    white-space: nowrap;
    max-width: 130px;
    min-width: 20px;
  }

  .france {
    background-color: $peter-river;
  }

  .serbie {
    background-color: $pomegrenate;
  }

}






</style>
