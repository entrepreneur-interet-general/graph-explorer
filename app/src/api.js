import axios from 'axios';

const searchUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/search" : getWebAppBackendUrl('search');
const neighborsUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/neighbors" : getWebAppBackendUrl('neighbors');
const transactionsUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/transactions" : getWebAppBackendUrl('transactions');

export default {

  search(options){
    /* return a promise to work with vue-material md-input autocomplete feature */ 
    return axios.get(searchUrl, options).then(response => {
      return response.data;
    })
  },
  neighbors(options, callback){
    axios.get(neighborsUrl, options).then(response => {
      callback(response.data);
    })
  },
  transactions(options, callback){
    axios.get(transactionsUrl, options).then(response => {
      callback(response.data);
    })
  } 
}