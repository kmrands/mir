<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <select v-model="activeSet">
      <option :value="item" v-for="item in anyof">{{getFieldSetName(item)}}</option>
    </select>
    <div class="" v-for="item in anyof" v-show="isActiveSet(item)">
      <div v-for="property in properties" v-if="properties" class="sub-field">
        <component
          :is="propertyMetaAttr(property, 'field')"
          :name="property"
          :help="propertyMetaAttr(property, 'help')"
          :label="propertyMetaAttr(property, 'label')"
          :choices="propertyMetaAttr(property, 'choices')"
          :schema="propertySchema(property)"
          :set="setter(property)"
          :data="getter(property)"
        ></component>
      </div>
    </div>
  </div>
</template>

<script>
import * as R from 'ramda'
import utils from '@/lib/utils'
import field from '@/mixins/field'

import string from '@/components/fields/string'
import richtext from '@/components/fields/richtext'
import dropdown from '@/components/fields/dropdown'
import imagefield from '@/components/fields/imagefield'
import checkbox from '@/components/fields/checkbox'
import checklist from '@/components/fields/checklist'
import objectid from '@/components/fields/objectid'
import password from '@/components/fields/password'
import radio from '@/components/fields/radio'
import slug from '@/components/fields/slug'

import dict from '@/components/fields/nested/dict'
import list from '@/components/fields/nested/list'
import simplelist from '@/components/fields/nested/simplelist'

export default {
  name: 'flexible_content',
  mixins: [field],
  components: {
    string,
    richtext,
    dropdown,
    imagefield,
    checkbox,
    checklist,
    objectid,
    password,
    radio,
    slug,
    dict,
    list,
    simplelist,
  },
  data() {
    return {
      activeSet: null
    }
  },
  watch: {
    activeSet() {
      if (this.scopedData) {
        this.set({})
      }
    },
  },
  mounted() {
    if (this.anyof && this.anyof.length > 0) {
      this.activeSet = this.anyof[0]
    }
  },
  computed: {
    localSchema() {
      return this.activeSet ? this.activeSet.schema : null
    },
    properties() {
      return utils.getProperties(this.localSchema)
    },
    scopedData: {
      get() {
        if (!this.data) return {}
        return this.data
      },
      set(val) {
        this.set(val)
      },
    },
  },
  methods: {
    isActiveSet(set) {
      return this.activeSet === set
    },
    getFieldSetName(set) {
      return R.path(['_metadata', 'label'], set)
    },
    setter(property) {
      const setter = (val) => {
        if (this.scopedData[property]) {
          this.scopedData[property] = val
          this.set(this.scopedData)
        } else {
          this.set(R.merge(this.scopedData, R.objOf(property, val)))
        }
      }
      return setter
    },
    getter(property) {
      return this.scopedData[property]
    },
  },
}
</script>
