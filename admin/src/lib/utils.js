import * as R from 'ramda'

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

function getProperties(schema) {
  return R.map(
    item => item[0],
    R.sortBy(
      item => item[1],
      R.filter(
        item => !item[0].startsWith('_'),
        R.map(
          (item) => [item[0], R.path(['_metadata', 'order'], item[1])],
          R.toPairs(schema)
        )
      )
    )
  )
}

function getMetadataAttr(schema, property, attr) {
    return R.path([property, '_metadata', attr], schema)
}

function getPropertySchema(schema, property) {
  return R.objOf(
    property,
    R.path([property, 'schema'], schema)
  )
}

function getPropertyAnyOf(schema, property) {
  return R.path([property, 'anyof'], schema)
}

export default {
  removeMeta,
  getProperties,
  getMetadataAttr: R.curry(getMetadataAttr),
  getPropertySchema: R.curry(getPropertySchema),
  getPropertyAnyOf: R.curry(getPropertyAnyOf),
}
