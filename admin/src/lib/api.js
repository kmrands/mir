import Vue from 'vue'
import axios from 'axios'
import { saveAs } from 'file-saver/FileSaver'

var api = axios.create({
  baseURL: `${process.env.SERVER}/api/v1`
});

/* global localStorage, btoa */
function createAuthHeaders() {
  const token = localStorage.getItem('token')

  if (token) {
    return {
      headers: {
        Authorization: token,
      }
    }
  }
  return {}
}

export default {
  getResource(resourceName, params) {
    const headers = createAuthHeaders()
    const options = {
      ...headers,
      ...params,
    }
    return api.get(resourceName, options)
    .then(
      response => response.data
    )
  },
  putResource(resourceName, data, etag) {
    const headers = createAuthHeaders()
    headers.headers["If-Match"] = etag

    const params = {
      ...headers,
    }
    return api.patch(resourceName, data, params)
    .then(
      response => response.data
    )
  },
  postResource(resourceName, data) {
    const headers = createAuthHeaders()

    const params = {
      ...headers,
    }
    return api.post(resourceName, data, params)
    .then(
      response => response.data
    )
  },
  deleteResource(resourceName, etag) {
    const headers = createAuthHeaders()
    headers.headers["If-Match"] = etag

    const params = {
      ...headers,
    }
    return api.delete(resourceName, params)
    .then(
      response => response.data
    )
  },
  exportData(resourceName) {
    const headers = createAuthHeaders()
    const params = {
      ...headers,
      responseType: 'blob',
    }
    return axios.get(`${process.env.SERVER}/export/${resourceName}`, params)
    .then(
      (response) => {
        console.log(response)
        saveAs(response.data)
      }
    )
  },
}
