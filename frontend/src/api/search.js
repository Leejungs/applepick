import axiosInstance from '../utils/axiosInstance';

const enc = encodeURIComponent;

class SearchAPI {
  getProducts() {
    return axiosInstance.get('/api/search/products');
  }

  searchPriceQuery(searchWord, size) {
    return axiosInstance.get(`/api/search/price/${enc(searchWord)}/${size}`);
  }

  searchPageQuery(searchWord, page) {
    return axiosInstance.get(`/api/search/${enc(searchWord)}/${page}`);
  }

  searchWeeklyPriceQuery(searchWord) {
    return axiosInstance.get(`/api/search/weekly/${enc(searchWord)}`);
  }

  searchRecentQuery(page) {
    return axiosInstance.get(`/api/search/recent/${page}`);
  }
}

export default new SearchAPI();
