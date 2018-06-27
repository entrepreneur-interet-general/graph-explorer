import axios from 'axios';

const countriesUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/countries" : getWebAppBackendUrl('countries');
const departmentsUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/departments" : getWebAppBackendUrl('departments');
const searchUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/search" : getWebAppBackendUrl('search');
const neighborsUrl = typeof (getWebAppBackendUrl) === 'undefined' ? "/neighbors" : getWebAppBackendUrl('neighbors');

export default {

  search(searchTerm){
    /* return a promise to work with vue-material md-input autocomplete feature */ 
    const fullUrl = `${searchUrl}?search_term=${searchTerm}`;
    return axios.get(fullUrl).then(response => {
      return response.data;
    })
  },
  neighbors(options, callback){
    axios.get(neighborsUrl , options).then(response => {
      callback(response.data);
    })
  } 
}