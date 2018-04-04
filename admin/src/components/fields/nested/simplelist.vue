<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <div
      v-if="scopedData && scopedData.length > 0"
      v-for="(value, idx) in scopedData"
      class="sub-field"
    >
      <component
        :key="idx"
        :is="propertyMetaAttr(name, 'field')"
        :choices="propertyMetaAttr(name, 'choices')"
        :schema="propertySchema(name)"
        :set="setter(idx)"
      ></component>
      <a href="#remove" @click.prevent="removeItem(idx)">Remove Item</a>
    </div>
    <div>
      <a href="#add" @click.prevent="addItem">Add Item</a>
    </div>
  </div>
</template>

<script>
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
import slug from '@/components/fields/slug'

export default {
  name: 'simplelist',
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
    slug,
  },
  computed: {
    localSchema() {
      return this.schema
    },
    scopedData() {
      if (!this.data) return []
      return this.data
    }
  },
  methods: {
    setter(idx) {
      const setter = (val) => {
        this.scopedData[idx] = val
        this.set(this.scopedData)
      }
      return setter
    },
    addItem() {
      let itemClone = null
      if (this.data) {
        itemClone = this.data
      } else {
        itemClone = []
      }
      itemClone.push('')
      this.set(itemClone)
    },
    removeItem(idx) {
      const itemClone = this.data
      itemClone.splice(idx, 1)
      this.set(itemClone)
    }
  },
}
</script>
