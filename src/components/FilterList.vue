<template>
  <div id="filters">
    <filter-country></filter-country>
    <filter-department></filter-department>
    <filter-date></filter-date>
  </div>
</template>

<script>
import FilterCountry from "./FilterCountry.vue";
import FilterDepartment from "./FilterDepartment.vue";
import FilterDate from "./FilterDate.vue";

export default {
  components: { FilterCountry, FilterDepartment, FilterDate }
};
</script>

<style lang="scss">
@import "../scss/settings.scss";

#filters {
  position: absolute;
  top: 31px;
  left: 500px;
  display: flex;
}

.filter-menu {
  margin-left: 15px;
  margin-right: 15px;
  z-index: 2;

  .md-button {
    border: solid 1px $silver;
    border-radius: 5px;
    background-color: white;
  }
}

.filter-menu-content {
  padding-left: 10px;
  padding-right: 10px;
  max-height: none;

  .md-checkbox {
    display: flex !important;
  }
}

.erase {
  float: left;
  border: none;
  padding: 0;
  cursor: pointer;
}

</style>


