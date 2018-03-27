import Vue from 'vue'
import Vuex from 'vuex'

import * as actions from './actions'
import * as getters from './getters'
import mutations from './mutations'

Vue.use(Vuex)

const state = {
  schema: {},
  currentSchema: {},
  currentItem: {},
  itemDiff: {},
  currentCollection: {},
  relationshipCollection: {},
  mediaLibrary: [],
  selectedMedia: null,
  mediaSelector: false,
  mediaSetter: null,
  editViewActive: false,
  token: null,
  username: null,
  roles: null,
  loading: false,
}

export default new Vuex.Store({
  state,
  actions,
  getters,
  mutations,
})
