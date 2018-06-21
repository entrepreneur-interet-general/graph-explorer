<template>
  <div class="filter-menu">
    <md-menu :md-offset-y="5" @md-opened="handleOpen" @md-closed="handleClose" >
      <md-button md-menu-trigger v-bind:style=menuButtonStyle disabled>{{menuButtonLabel}}</md-button>
      <md-menu-content class="filter-menu-content">
        <!-- <div>
          <md-checkbox v-model="filter" v-for="country in countries" :key="country.code" v-bind:value="country.code">{{country.name}}</md-checkbox>
          <button class="erase" v-show="filter.length > 0" @click="filter=[]">
            <span class="md-body-1">Effacer</span>
          </button>
        </div> -->
      </md-menu-content>
    </md-menu>
  </div>
</template>

<script>
import { UPDATE_FILTER } from "../mutation-types";
import api from "../api";

export default {
  data() {
    return {
      opened: false,
      countries: [],
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
        filterType: "country",
        value: filter
      });
    }
  },
  mounted() {
    var vm = this;
    /* get a list of available countries */
    api.getCountries(countries => {
      vm.countries = countries;
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
        return "Origine / Destination";
      } else {
        var filterCountryCode = this.filter[0];
        var filterCountry = this.countries.find(country => {
          return country.code == filterCountryCode;
        });
        return filterCountry.name;
      }
    }
  }
};
</script>

