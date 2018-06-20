<template>
  <div class="filter-menu">
    <md-menu :md-offset-y="5" @md-opened="handleOpen" @md-closed="handleClose">
      <md-button disabled md-menu-trigger v-bind:style=menuButtonStyle>{{menuButtonLabel}}</md-button>
      <md-menu-content class="filter-menu-content">
        <div>
          <md-checkbox v-model="filter" v-for="department in departments" v-bind:key="department.code" v-bind:value="department.code">{{department.name}}</md-checkbox>
          <button class="erase" v-show="filter.length > 0" @click="filter=[]">
            <span class="md-body-1">Effacer</span>
          </button>
        </div>
      </md-menu-content>
    </md-menu>
  </div>
</template>

<script>
import api from "../api";
import { UPDATE_FILTER } from "../mutation-types";

export default {
  data() {
    return {
      opened: false,
      departments: [],
      filter: []
    };
  },
  methods: {
    handleOpen() {
      this.opened = true;
    },
    handleClose() {
      this.opened = false;
      this.applyFilter();
    },
    applyFilter() {
      let filter = this.filter.length > 0 ? this.filter[0] : null;
      this.$store.commit(UPDATE_FILTER, {
        filterType: "department",
        value: filter
      });
    }
  },
  mounted() {
    var vm = this;
    /* get a list of available datasets */
    api.getDepartments(departments => {
      vm.departments = departments;
    });
  },
  watch: {
    filter() {
      /* simulates the behavior of a radio button for the moment */
      if (this.filter.length > 1) {
        this.filter.shift();
      }
    }
  },
  computed: {
    menuButtonStyle() {
      if (this.opened || this.filter.length > 0) {
        return { "background-color": "#1ABC9C" };
      }
    },
    menuButtonLabel() {
      if (this.filter.length == 0) {
        return "Département";
      } else {
        var filterDepartmentCode = this.filter[0];
        var filterDepartment = this.departments.find(department => {
          return department.code == filterDepartmentCode;
        });
        return filterDepartment.name;
      }
    }
  }
};
</script>
