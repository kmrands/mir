import Vue from 'vue'
import axios from 'axios'

var api = axios.create({
  baseURL: process.env.SERVER
});

/* global localStorage, btoa */
function createAuthHeaders() {
  const user = localStorage.getItem('username')
  const token = localStorage.getItem('token')

  if (user && token) {
    return {
      auth: {
        username: user,
        password: token
      }
    }
  }
  return null
}

export default {
  getResource(resourceName, params) {
    const auth = createAuthHeaders()
    const options = {
      ...auth,
      ...params,
    }
    return api.get(resourceName, options)
    .then(
      response => response.data
    )
  },
  putResource(resourceName, data, etag) {
    const headers = {
      headers: {
        "If-Match": etag,
      }
    }
    const auth = createAuthHeaders()
    const params = {
      ...auth,
      ...headers,
    }
    return api.put(resourceName, data, params)
    .then(
      response => response.data,
      error => error.data
    )
  },
  postResource(resourceName, data) {
    const auth = createAuthHeaders()
    const params = {
      ...auth,
    }
    return api.post(resourceName, data, params)
    .then(
      response => response.data,
      error => error.data
    )
  },
  deleteResource(resourceName, etag) {
    const headers = {
      headers: {
        "If-Match": etag,
      }
    }
    const auth = createAuthHeaders()
    const params = {
      ...auth,
      ...headers,
    }
    return api.delete(resourceName, params)
    .then(
      response => response.data,
      error => error.data
    )
  },
}
