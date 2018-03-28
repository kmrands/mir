import { mapGetters, mapActions } from 'vuex'
import utils from '@/lib/utils'
import * as R from 'ramda'

export default {
  props: [
    'name',
    'field',
    'help',
    'label',
    'choices',
    'schema',
    'set',
    'get',
    'data',
    'anyof',
    'relationship',
  ],
  computed: {
    ...mapGetters(['currentSchema', 'currentItem']),
    localSchema() {
      if (this.name) {
        return R.path([this.name, 'schema'], this.schema)
          ? R.path([this.name, 'schema'], this.schema)
          : this.schema[this.name]
      }
    },
    properties() {
      if (this.localSchema) {
        return utils.getProperties(this.localSchema)
      }
      return utils.getProperties(this.currentSchema)
    },
    propertyMetaAttr() {
      if (this.localSchema) {
        return utils.getMetadataAttr(this.localSchema)
      }
      return utils.getMetadataAttr(this.currentSchema)
    },
    propertySchema() {
      if (this.localSchema) {
        return utils.getPropertySchema(this.localSchema)
      }
      return utils.getPropertySchema(this.currentSchema)
    },
    propertyAnyOf() {
      if (this.localSchema) {
        return utils.getPropertyAnyOf(this.localSchema)
      }
      return utils.getPropertyAnyOf(this.currentSchema)
    },
    scopedData: {
      get() {
        return this.data
      },
      set(val) {
        if (val === "") {
          this.set(null)
        } else {
          this.set(val)
        }
      }
    },
  },
  methods: {
    ...mapActions([
      'getCurrentSchema',
      'setCurrentItem',
      'getCurrentItem',
      'clearCurrentItem'
    ]),
  }
}
