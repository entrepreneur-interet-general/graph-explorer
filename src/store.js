import Vue from 'vue';
import Vuex from 'vuex';
import { UPDATE_FILTER, UPDATE_FOCUS_NODE, UPDATE_GRAPH, SHOW_MODAL, HIDE_MODAL, 
  SHOW_PROGRESS_SPINNER, HIDE_PROGRESS_SPINNER } from './mutation-types';
import api from './api';
import * as jsnx from 'jsnetworkx'; 

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    filter: {
      country: null,
      departement: null
    },
    focusNodeEntity: null,
    G: new jsnx.MultiDiGraph(),
    showModal: false,
    showProgressSpinner: false
  },
  getters: {
    nodes(state) {
      return state.G.nodes(true).map(([_, node]) => node);
    },
    links(state) {
      return state.G.edges(true).map(([_1, _2, edge]) => edge);
    },
    focusNode(state) {
      if (state.focusNodeEntity) {
        return state.G.nodes(true)
          .map(([_, node]) => node)
          .find(n => n.entity == state.focusNodeEntity) 
      }
      return null;
    },
    focusNodeLinks(state) {
      if (state.focusNodeEntity) {
        const H = state.G.toUndirected();
        const edges = H.edges(state.focusNodeEntity, true).map(([_1, _2, edge]) => edge);
        return edges;
      }
      return [];
    }
  },
  mutations: {
    [UPDATE_FILTER] (state, payload) {
      const filterType = payload.filterType; 
      const value = payload.value;
      state.filter[filterType] = value;
    },
    [UPDATE_FOCUS_NODE] (state, payload) {
      state.focusNodeEntity = payload;
    },
    [UPDATE_GRAPH] (state, payload) {
      state.G = payload;
    },
    [SHOW_MODAL] (state) {
      state.showModal = true;
    },
    [HIDE_MODAL] (state) {
      state.showModal = false;
    },
    [SHOW_PROGRESS_SPINNER] (state) {
      state.showProgressSpinner = true;
    },
    [HIDE_PROGRESS_SPINNER] (state) {
      state.showProgressSpinner = false;
    }
  },
  actions: {
    expand({ commit, state }, entity) {
      let G = state.G.copy();
      if (G.hasNode(entity)) {
        let node = G.get(entity)
        if (G.degree(entity) == node.degree) {
          // the node is already expanded, exit
          return 
        }
      }
      // else retrieves missing neighbors from the backend
      commit(SHOW_PROGRESS_SPINNER);
      const options = {
        params: { node: entity }
      };
      api.neighbors(options, ({ nodes, links }) => {
        nodes.forEach(node => {
          if (!G.hasNode(node.entity)){
            G.addNode(node.entity, node);
          }
        });
        links.forEach(link => {
          if (!G.hasEdge(link.source, link.target)){
            G.addEdge(link.source, link.target, link)
          }
        })
        commit(UPDATE_GRAPH, G);
        commit(UPDATE_FOCUS_NODE, entity);
      });
    },
    hide({ commit, state }, entity) {
      let G = state.G.copy();
      G.removeNode(entity);
      commit(UPDATE_FOCUS_NODE, null);
      commit(UPDATE_GRAPH, G);
    },
    collapse({ commit, state }, entity) {
      let G = state.G.toUndirected();
      const neighbors = G.neighbors(entity);
      const leafs = neighbors.filter(n => G.degree(n) == 1)
      G.removeNodesFrom(leafs);
      commit(UPDATE_GRAPH, G);
    }
  }
})
