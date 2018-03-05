<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
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
</template>

<script>
import * as R from 'ramda'

import field from '@/mixins/field'

import string from '@/components/fields/string'
import richtext from '@/components/fields/richtext'
import list from '@/components/fields/list'
import dropdown from '@/components/fields/dropdown'
import imagefield from '@/components/fields/imagefield'
import checkbox from '@/components/fields/checkbox'
import checklist from '@/components/fields/checklist'
import objectid from '@/components/fields/objectid'
import password from '@/components/fields/password'
import radio from '@/components/fields/radio'
import simplelist from '@/components/fields/simplelist'
import slug from '@/components/fields/slug'


export default {
  name: 'dict',
  mixins: [field],
  components: {
    string,
    richtext,
    list,
    dropdown,
    imagefield,
    checkbox,
    checklist,
    objectid,
    password,
    radio,
    simplelist,
    slug,
  },
  computed: {
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
    setter(property) {
      const setter = (val) => {
        console.log(val)
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
    }
  },
}
</script>
