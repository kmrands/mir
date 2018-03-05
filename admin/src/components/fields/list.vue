<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <div
      v-if="scopedData && scopedData.length > 0"
      v-for="(value, idx) in scopedData"
    >
      <div v-for="property in properties" v-if="properties" class="sub-field">
        <component
          :is="propertyMetaAttr(property, 'field')"
          :name="property"
          :help="propertyMetaAttr(property, 'help')"
          :label="propertyMetaAttr(property, 'label')"
          :choices="propertyMetaAttr(property, 'choices')"
          :schema="propertySchema(property)"
          :anyof="propertyAnyOf(property)"
          :set="setter(idx, property)"
          :data="getter(idx, property)"
        ></component>
      </div>
      <a href="#remove" @click.prevent="removeItem(idx)">Remove Item</a>
    </div>
    <div>
      <a href="#add" @click.prevent="addItem">Add Item</a>
    </div>
  </div>
</template>

<script>
import * as R from 'ramda'

import field from '@/mixins/field'

import string from '@/components/fields/string'
import richtext from '@/components/fields/richtext'
import dropdown from '@/components/fields/dropdown'
import dict from '@/components/fields/dict'
import imagefield from '@/components/fields/imagefield'
import checkbox from '@/components/fields/checkbox'
import checklist from '@/components/fields/checklist'
import objectid from '@/components/fields/objectid'
import password from '@/components/fields/password'
import radio from '@/components/fields/radio'
import simplelist from '@/components/fields/simplelist'
import flexible_content from '@/components/fields/flexible_content'
import slug from '@/components/fields/slug'


export default {
  name: 'list',
  mixins: [field],
  components: {
    string,
    richtext,
    dropdown,
    dict,
    imagefield,
    checkbox,
    checklist,
    objectid,
    password,
    radio,
    simplelist,
    flexible_content,
    slug,
  },
  data() {
    return {
      hasFlex: false,
    }
  },
  computed: {
    scopedData() {
      if (!this.data) return []
      return this.data
    },
    localSchema() {
      if (this.name && R.path([this.name, 'anyof'], this.schema)) {
        return this.schema
      }
      if (this.name && !R.path([this.name, 'anyof'], this.schema)) {
        return R.path([this.name, 'schema'], this.schema)
          ? R.path([this.name, 'schema'], this.schema)
          : this.schema[this.name]
      }
    },
  },
  methods: {
    setter(idx, property) {
      const setter = (val) => {
        if (!R.path([this.name, 'anyof'], this.schema)) {
          if (this.scopedData[idx][property]) {
            this.scopedData[idx][property] = val
          } else {
            this.scopedData[idx] = R.merge(
              this.scopedData[idx],
              R.objOf(property, val)
            )
          }
        } else {
          this.scopedData[idx] = this.scopedData[idx] && !R.isEmpty(val)
            ? R.merge(this.scopedData[idx], val)
            : val
        }
        this.set(this.scopedData)
      }
      return setter
    },
    getter(idx, property) {
      if (R.path([this.name, 'anyof'], this.schema)) {
        return this.scopedData[idx]
      }
      return this.scopedData[idx][property]
    },
    addItem() {
      let itemClone = null
      if (this.data) {
        itemClone = this.data
      } else {
        itemClone = []
      }
      itemClone.push({})
      this.set(itemClone)
    },
    removeItem(idx) {
      const itemClone = this.data
      itemClone.splice(idx, 1)
      if (itemClone.length === 0) {
        this.set(null)
      } else {
        this.set(itemClone)
      }
    }
  },
}
</script>
