import * as R from 'ramda'

import * as types from './mutation-types'
import api from '@/lib/api'

/* global btoa */

function stringifyParameters(obj) {
  return R.map(value => JSON.stringify(value), obj)
}

function removeMeta(data) {
  if (data instanceof Array) {
    data = R.map(removeMeta, data)
  } else if (typeof data === 'object' && data !== null) {
    /* eslint-disable */
    data = R.pickBy((value, key) => {
      return !key.startsWith('_')
    }, data)
    data = R.map(removeMeta, data)
    /* eslint-enable */
  }
  return data
}

// Schema
// ------------------------------
export const getSchema = ({ commit }) => {
  api.getResource('info').then((result) => {
    commit(types.SCHEMA, result)
  })
}

export const getCurrentSchema = ({ state, commit }, resourceType) => {
  if (resourceType) {
    api.getResource(`info/${resourceType}`).then((result) => {
      commit(types.CURRENT_SCHEMA, result)
    })
  }
}

// Single Resource
// ------------------------------
export const getCurrentItem = ({ state, commit }, data) => {
  commit(types.LOADING, true)
  const filters = data.params ? stringifyParameters(data.params) : null
  if (data.resourceType && data.resourceId) {
    return api.getResource(`${data.resourceType}/${data.resourceId}`, { params: filters }).then((result) => {
      if (filters && filters.version) {
        result._etag = state.currentItem ? state.currentItem._etag : null
      }
      commit(types.CURRENT_ITEM, result)
      commit(types.LOADING, false)
    })
  }
  return null
}

export const getItemDiff = ({ state, commit }, data) => {
  commit(types.LOADING, true)
  const filters = data.params ? stringifyParameters(data.params) : {}
  filters.version = 'diffs'

  if (data.resourceType && data.resourceId) {
    console.log('test')
    return api.getResource(`${data.resourceType}/${data.resourceId}`, { params: filters }).then((result) => {
      commit(types.ITEM_DIFF, result)
      commit(types.LOADING, false)
    })
  }
  commit(types.ITEM_DIFF, null)
  commit(types.LOADING, false)
  return null
}

export const setCurrentItem = ({ state, commit }, data) => {
  commit(types.CURRENT_ITEM, data)
}

export const clearCurrentItem = ({ commit }) => {
  commit(types.CLEAR_CURRENT_ITEM)
}

export const createItem = ({ state, commit }, data) => {
  let payload = null
  if (data.resourceType !== 'media') {
    payload = removeMeta(data.payload)
  } else {
    payload = data.payload
  }
  return api.postResource(`${data.resourceType}`, payload).then((result) => {
    commit(types.CURRENT_ITEM, {})
  })
}

export const updateItem = ({ state, commit }, data) => {
  const payload = removeMeta(data.payload)
  const etag = data.etag
  console.log(etag)
  return api.putResource(`${data.resourceType}/${data.resourceId}`, payload, etag).then((result) => {
    commit(types.CURRENT_ITEM, {})
    return result
  })
}

export const deleteItem = ({ state, commit }, data) => {
  const etag = data.etag
  return api.deleteResource(`${data.resourceType}/${data.resourceId}`, etag).then((result) => {
    commit(types.CURRENT_ITEM, {})
    return result
  })
}

// Resource Collection
// ------------------------------
export const getCurrentCollection = ({ state, commit }, data) => {
  const filters = data.params ? stringifyParameters(data.params) : null
  if (data.resourceType) {
    return api.getResource(`${data.resourceType}`, { params: filters }).then((result) => {
      commit(types.CURRENT_COLLECTION, result)
      return result
    })
  }
  return null
}
export const getRelationshipCollection = ({ state, commit }, data) => {
  const filters = data.params ? stringifyParameters(data.params) : null
  if (data.resourceType) {
    return api.getResource(`${data.resourceType}`, { params: filters }).then((result) => {
      commit(types.RELATIONSHIP_COLLECTION, result)
    })
  }
  return null
}

// Media Library
// ------------------------------
export const getMediaLibrary = ({ state, commit }, data) => {
  const filters = (data && data.params) ? stringifyParameters(data.params) : null
  api.getResource('media', { params: filters }).then((result) => {
    commit(types.MEDIA_LIBRARY, result)
  })
}

export const showMediaSelector = ({ state, commit }, data) => {
  if (data) {
    commit(types.SHOW_MEDIA_SELECTOR, data.show)
    commit(types.MEDIA_SETTER, data.setter)
  } else {
    commit(types.SHOW_MEDIA_SELECTOR, null)
    commit(types.MEDIA_SETTER, null)
  }
}

export const setMedia = ({ state, commit }, data) => {
  let newSelectedMedia = state.selectedMedia
  if (newSelectedMedia) {
    newSelectedMedia[data.guid] = data.url
  } else {
    newSelectedMedia = {}
    newSelectedMedia[data.guid] = data.url
  }
  commit(types.SELECTED_MEDIA, newSelectedMedia)
}

// Edit View
// ------------------------------
export const showEditView = ({ state, commit }, data) => {
  commit(types.EDIT_VIEW, data)
}

// Authentication
// ------------------------------
export const login = ({ state, commit }, data) => {
  const authString = btoa(`${data.username}:${data.password}`)
  const loginOptions = {
    headers: {
      Authorization: `Basic ${authString}`,
    },
  }
  return api.getResource('accounts', loginOptions)
}

export const handleCredentials = ({ commit }, response) => {
  const token = response._items[0].token
  const username = response._items[0].username
  const roles = response._items[0].roles
  // Store in localStorage
  /* global localStorage */
  localStorage.setItem('token', token)
  localStorage.setItem('username', username)
  localStorage.setItem('roles', roles)
}

export const notify = ({ commit }, notification) => {
  commit(types.NOTIFICATION, notification)
}
