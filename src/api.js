import axios from 'axios';

const countriesUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/countries" : getWebAppBackendUrl('countries');
const departmentsUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/departments" : getWebAppBackendUrl('departments');
const searchUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/search" : getWebAppBackendUrl('search');
const subgraphUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/subgraph" : getWebAppBackendUrl('subgraph');

export default {

  getCountries(callback){
    axios.get(countriesUrl).then(response => {
      callback(response.data);
    });
  },
  getDepartments(callback){
    axios.get(departmentsUrl).then(response => {
      callback(response.data);
    });
  },
  search(searchTerm){
    /* return a promise to work with vue-material md-input autocomplete feature */ 
    const fullUrl = `${searchUrl}?search_term=${searchTerm}`;
    return axios.get(fullUrl).then(response => {
      return response.data;
    })
  },
  subgraph(options, callback){
    axios.post(subgraphUrl, options).then(response => {
      callback(response.data);
    })
  } 
}