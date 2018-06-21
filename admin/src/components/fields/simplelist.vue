<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <div
      v-if="scopedData && scopedData.length > 0 && scopedData.length <= 10"
      v-for="(value, idx) in scopedData"
      class="sub-field"
    >
      <component
        :key="idx"
        :is="propertyMetaAttr(name, 'field')"
        :choices="propertyMetaAttr(name, 'choices')"
        :schema="propertySchema(name)"
        :relationship="propertyMetaAttr(name, 'relationship')"
        :set="setter(idx)"
        :data="getter(idx)"
      ></component>
      <a href="#remove" @click.prevent="removeItem(idx)">Remove Item</a>
    </div>
    <div
      v-if="scopedData && scopedData.length > 0 && scopedData.length > 10"
    >
        <input type="text" name="search" placeholder="Search items..." v-model="searchTerm">
        <div
          v-for="(value, idx) in scopedData"
          class="sub-field"
          v-show="isValidItem(value, idx) && isSearched(value)"
        >
          <component
            :key="idx"
            :is="propertyMetaAttr(name, 'field')"
            :choices="propertyMetaAttr(name, 'choices')"
            :schema="propertySchema(name)"
            :relationship="propertyMetaAttr(name, 'relationship')"
            :set="setter(idx)"
            :data="getter(idx)"
          ></component>
          <a href="#remove" @click.prevent="removeItem(idx)">Remove Item</a>
        </div>
    </div>
    <div v-if="scopedData && scopedData.length > 0 && scopedData.length > 10">
      <div class="text-center row" v-if="!searchTerm">
        <div class="columns">
          <a href="#prev" @click.prevent="prevPage">
            <i class="fas fa-arrow-left"></i>
          </a>
          <span class="pagecount">
            Page {{currentPage + 1}} of {{Math.ceil(scopedData.length / 5)}}
          </span>
          <a href="#next" @click.prevent="nextPage">
            <i class="fas fa-arrow-right"></i>
          </a>
        </div>
      </div>
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
import slug from '@/components/fields/slug'
import flexible_content from '@/components/fields/flexible_content'

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
    simplelist,
    slug,
    flexible_content,
  },
  data() {
    return {
      currentPage: 0,
      searchTerm: null,
    }
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
    getter(idx, property) {
      return this.scopedData[idx]
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
      if (this.scopedData && this.scopedData.length > 0 && this.scopedData.length > 10) {
        this.currentPage = Math.ceil(this.scopedData.length / 5) - 1
      }
    },
    removeItem(idx) {
      const itemClone = this.data
      itemClone.splice(idx, 1)
      this.set(itemClone)
    },
    nextPage() {
      if (this.currentPage < Math.ceil(this.scopedData.length / 5) - 1) {
        this.currentPage += 1
      } else {
        this.currentPage = Math.ceil(this.scopedData.length / 5) - 1
      }
    },
    prevPage() {
      if (this.currentPage > 0) {
        this.currentPage -= 1
      } else {
        this.currentPage = 0
      }
    },
    isValidItem(value, idx) {
      return (
        idx >= (this.currentPage * 5) && idx < ((this.currentPage * 5) + 5)
      )
    },
    isSearched(value) {
      if (this.searchTerm) {
        return R.contains(this.searchTerm, value)
      }
      return true
    }
  },
}
</script>

<style lang="scss">
.pagecount {
    margin-left: 10px;
    margin-right: 10px;
}
</style>
