import Vue from 'vue';
import Vuex from 'vuex';
import { UPDATE_FILTER, UPDATE_FOCUS_NODE, UPDATE_NODES, UPDATE_LINKS } from './mutation-types';
import api from './api';


Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    filter: {
      country: null,
      departement: null
    },
    focusNodeEntity: null,
    nodes: [],
    links: []
  },
  getters: {
    focusNode(state) {
      return state.nodes.find(node => node.entity == state.focusNodeEntity)
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
    [UPDATE_NODES] (state, payload) {
      state.nodes = payload;
    },
    [UPDATE_LINKS] (state, payload) {
      state.links = payload;
    }
  },
  actions: {
    expand({ commit, state }, entity) {
      const options = {
        nodes: state.nodes.map(n => n.entity),
        expand_node: entity
      };
      api.subgraph(options, ({nodes, links}) => {

        let update_nodes = state.nodes;
        let update_links = state.links;

        nodes.forEach(node => {
          const exists = state.nodes.find(n => { 
            return n.entity == node.entity
          });
          if (!exists) {
            update_nodes.push(node);
          }
        })
        links.forEach(link => {
          const exists = state.links.find(l => {
            const s = l.source.entity ? l.source.entity : l.source;
            const t = l.target.entity ? l.target.entity : l.target;
            return link.source == s && link.target == t;
          });
          if (!exists) {
            update_links.push(link);
          }
        })
        commit(UPDATE_FOCUS_NODE, entity);
        commit(UPDATE_NODES, update_nodes);
        commit(UPDATE_LINKS, update_links);
      });
    },
    hide({ commit, state }, entity) {
      const nodes = state.nodes.filter(n => n.entity != entity);
      const links = state.links.filter(link => {
        const source = link.source.entity ? link.source.entity : link.source;
        const target = link.target.entity ? link.target.entity : link.target;
        return source != entity && target != entity
      })
      commit(UPDATE_FOCUS_NODE, null);
      commit(UPDATE_NODES, nodes);
      commit(UPDATE_LINKS, links);
    },
    collapse({ commit, state }, entity) {
      const options = {
        nodes: state.nodes.map(n => n.entity),
        collapse_node: entity
      }
      api.subgraph(options, ({ nodes, links }) => {

        let leafs = []
        const update_nodes = state.nodes.filter(node => {
          const exists = nodes.find(n => {
            return node.entity == n.entity;
          });
          if (!exists) {
            leafs.push(node.entity);
          }
          return exists;
        })

        const update_links = state.links.filter(l => {
          const s = l.source.entity ? l.source.entity : l.source;
          const t = l.target.entity ? l.target.entity : l.target;
          return !(leafs.includes(s) || leafs.includes(t)); 
        }) 


        commit(UPDATE_NODES, update_nodes);
        commit(UPDATE_LINKS, update_links);
      });
    }
  }
})
