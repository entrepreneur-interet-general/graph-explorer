import Vue from 'vue';
import Vuex from 'vuex';
import * as jsnx from 'jsnetworkx';
import {
  UPDATE_FILTER,
  UPDATE_FOCUS_NODE,
  UPDATE_GRAPH,
  SHOW_PROGRESS_SPINNER,
  HIDE_PROGRESS_SPINNER,
  SHOW_DRAWER_SEARCH_RESULTS,
  HIDE_DRAWER_SEARCH_RESULTS,
  UPDATE_SEARCH_RESULTS
} from './mutation-types';
import api from './api';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    filter: {
      country: null,
      departement: null
    },
    focusNodeEntity: null,
    searchResults: [],
    G: new jsnx.MultiDiGraph(),
    showProgressSpinner: false,
    showDrawerSearchResults: false
  },
  getters: {
    nodes(state) {
      return state.G.nodes(true).map(([, node]) => node);
    },
    links(state) {
      const links = state.G.edges(true).map(([,, edge]) => edge);
      // aggregates parallel edges when a pair of nodes (source, target)
      // has several transactions associated
      const aggregated = links.reduce((rv, x) => {
        const groupKey = `${x.source},${x.target}`;
        /* eslint no-param-reassign: ["error", { "props": false }] */
        rv[groupKey] = rv[groupKey] || {
          source: x.source,
          target: x.target,
          valeur_euro: 0,
          number_of_links: 0
        };
        rv[groupKey].valeur_euro += x.valeur_euro;
        rv[groupKey].number_of_links += 1;
        return rv;
      }, {});
      return Object.values(aggregated);
    },
    focusNode(state) {
      if (state.focusNodeEntity) {
        return state.G.nodes(true)
          .map(([, node]) => node)
          .find(n => n.entity === state.focusNodeEntity);
      }
      return null;
    },
    showGraphWidgets(state) {
      return state.G.numberOfNodes() > 0;
    },
    showDrawer(state, getters) {
      return getters.showDrawerNodeInfo || state.showDrawerSearchResults;
    },
    showDrawerNodeInfo(state) {
      return state.focusNodeEntity;
    },
    showBackToResults(state) {
      return !state.showDrawerSearchResults && state.searchResults.length > 0;
    }
  },
  mutations: {
    [UPDATE_FILTER](state, payload) {
      const { filterType } = payload;
      const { value } = payload;
      state.filter[filterType] = value;
    },
    [UPDATE_FOCUS_NODE](state, payload) {
      state.focusNodeEntity = payload;
      state.showDrawerSearchResults = false;
    },
    [UPDATE_GRAPH](state, payload) {
      state.G = payload;
    },
    [SHOW_PROGRESS_SPINNER](state) {
      state.showProgressSpinner = true;
    },
    [HIDE_PROGRESS_SPINNER](state) {
      state.showProgressSpinner = false;
    },
    [SHOW_DRAWER_SEARCH_RESULTS](state) {
      state.showDrawerSearchResults = true;
    },
    [HIDE_DRAWER_SEARCH_RESULTS](state) {
      state.showDrawerSearchResults = false;
    },
    [UPDATE_SEARCH_RESULTS](state, payload) {
      if (payload.constructor === Array && payload.length === 0) {
        state.showDrawerSearchResults = false;
      }
      state.searchResults = payload;
    }
  },
  actions: {
    expand({ commit, state }, entity) {
      const G = state.G.copy();
      if (G.hasNode(entity)) {
        const node = G.get(entity);
        if (G.degree(entity) === node.degree) {
          // the node is already expanded, exit
          return;
        }
      }
      // else retrieves missing neighbors from the backend
      commit(SHOW_PROGRESS_SPINNER);
      const options = {
        params: { node: entity }
      };
      api.neighbors(options, ({ nodes, links }) => {
        nodes.forEach((node) => {
          if (!G.hasNode(node.entity)) {
            G.addNode(node.entity, node);
          }
        });
        links.forEach((link) => {
          G.addEdge(link.source, link.target, link);
        });
        commit(UPDATE_GRAPH, G);
        commit(UPDATE_FOCUS_NODE, entity);
      });
    },
    hide({ commit, state }, entity) {
      const G = state.G.copy();
      G.removeNode(entity);
      commit(UPDATE_FOCUS_NODE, null);
      commit(UPDATE_GRAPH, G);
    },
    collapse({ commit, state }, entity) {
      const G = state.G.toUndirected();
      const neighbors = G.neighbors(entity);
      const leafs = neighbors.filter(n => G.neighbors(n).length === 1);
      G.removeNodesFrom(leafs);
      commit(UPDATE_GRAPH, G);
    }
  }
});
