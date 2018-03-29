import * as types from './mutation-types'
import * as R from 'ramda'


export default {
  [types.SCHEMA](state, schema) {
    state.schema = schema
  },
  [types.CURRENT_SCHEMA](state, currentSchema) {
    state.currentSchema = currentSchema
  },
  [types.CURRENT_ITEM](state, currentItem) {
    state.currentItem = { ...state.currentItem, ...currentItem }
  },
  [types.FORCE_CURRENT_ITEM](state, currentItem) {
    state.currentItem = null
    state.currentItem = currentItem
  },
  [types.ITEM_DIFF](state, itemDiff) {
    if (itemDiff) {
      state.itemDiff = { ...state.itemDiff, ...itemDiff }
    } else {
      state.itemDiff = {}
    }
  },
  [types.CLEAR_CURRENT_ITEM](state) {
    state.currentItem = {}
  },
  [types.CURRENT_COLLECTION](state, currentCollection) {
    state.currentCollection = currentCollection
  },
  [types.RELATIONSHIP_COLLECTION](state, relationshipCollection) {
    state.relationshipCollection = { ...state.relationshipCollection, ...relationshipCollection }
  },
  [types.MEDIA_LIBRARY](state, mediaLibrary) {
    state.mediaLibrary = mediaLibrary
  },
  [types.SHOW_MEDIA_SELECTOR](state, mediaSelector) {
    state.mediaSelector = mediaSelector
  },
  [types.MEDIA_SETTER](state, mediaSetter) {
    state.mediaSetter = mediaSetter
  },
  [types.SELECTED_MEDIA](state, selectedMedia) {
    state.selectedMedia = { ...state.selectedMedia, ...selectedMedia }
  },
  [types.EDIT_VIEW](state, editView) {
    state.editViewActive = editView
  },
  [types.STORE_TOKEN](state, data) {
    state.token = data
  },
  [types.STORE_USERNAME](state, data) {
    state.username = data
  },
  [types.STORE_ROLES](state, data) {
    state.roles = data
  },
  [types.LOADING](state, data) {
    state.loading = data
  },
  [types.NOTIFICATION](state, notification) {
    state.notification = notification
    setTimeout(() => {
      state.notification = null
    }, 2000)
  },
}
