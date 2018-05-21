import * as R from 'ramda'

export const settings = (state) => {
  const settings = R.path(['_items'], state.settings)
  if (settings) {
    return R.mergeAll(R.map((item) => {
      return R.objOf(
        item.title,
        R.mergeAll(R.map(
          (setting) => R.objOf(setting.key, setting.value),
          item.setting_value
        )
      ))
    }, settings))
  }
  return state.settings
}

export const schema = (state) => {
  return state.schema
}

export const currentSchema = (state) => {
  return state.currentSchema
}

export const currentItem = (state) => {
  return state.currentItem
}

export const itemDiff = (state) => {
  return state.itemDiff
}

export const currentCollection = (state) => {
  return state.currentCollection
}

export const relationshipCollection = (state) => {
  return state.relationshipCollection
}

export const mediaLibrary = (state) => {
  return state.mediaLibrary
}

export const mediaSelector = (state) => {
  return state.mediaSelector
}

export const mediaSetter = (state) => {
  return state.mediaSetter
}

export const editViewActive = (state) => {
  return state.editViewActive
}

export const selectedMedia = (state) => {
  return state.selectedMedia
}

export const loading = (state) => {
  return state.loading
}

export const notification = (state) => {
  return state.notification
}
