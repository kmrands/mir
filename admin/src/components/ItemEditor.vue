<template>
  <div id="main-index" v-if="loaded">
    <div class="row align-center">
      <div class="columns padding-sm">
        <div v-for="property in properties" class="form-field">
          <component
            :is="propertyMetaAttr(property, 'field')"
            :name="property"
            :help="propertyMetaAttr(property, 'help')"
            :label="propertyMetaAttr(property, 'label')"
            :choices="propertyMetaAttr(property, 'choices')"
            :schema="propertySchema(property)"
            :anyof="propertyAnyOf(property)"
            :set="setter(property)"
            :data="getter(property)"
          ></component>
        </div>
      </div>
    </div>
    <div class="row align-center">
      <div class="columns">
        <a href="#save" class="button" @click.prevent="saveResource" v-if="!$route.params.id">Save</a>
        <a href="#update" class="button" @click.prevent="saveResource" v-if="$route.params.id">Update</a>
        <a href="#delete" class="button alert" @click.prevent="deleteResource" v-if="$route.params.id">Delete</a>
        <router-link :to="{name: 'ItemList', params: {type: $route.params.type}}" class="button secondary">Cancel</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import * as R from 'ramda'

import { mapGetters, mapActions } from 'vuex'
import utils from '@/lib/utils'
import field from '@/mixins/field'

import string from '@/components/fields/string'
import richtext from '@/components/fields/richtext'
import list from '@/components/fields/list'
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
  components: {
    string,
    richtext,
    list,
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
  mixins: [field],
  name: 'itemEditor',
  watch: {
    '$route': 'refreshData',
  },
  mounted() {
    this.refreshData()
  },
  data() {
    return {
      loaded: false,
    }
  },
  methods: {
    ...mapActions(['createItem', 'updateItem', 'deleteItem']),
    setter(property) {
      const setter = (data) => {
        const itemClone = this.currentItem
        itemClone[property] = data
        this.setCurrentItem(itemClone)
      }
      return setter
    },
    getter(property) {
      return this.currentItem[property]
    },
    refreshData() {
      this.loaded = false
      this.clearCurrentItem()

      console.log(this.$route)
      const _type = this.$route.params.type
      const _id = this.$route.params.id

      this.getCurrentSchema(this.$route.params.type)

      if (_id) {
        this.getCurrentItem({
          resourceId: _id,
          resourceType: _type,
        }).then((result) => {
          this.loaded = true
        }).catch(() => {
          this.$router.push({ name: 'Index' })
        })
      } else {
        this.loaded = true
      }
    },
    saveResource() {
      const _type = this.$route.params.type
      const _id = this.$route.params.id

      if (_id) {
        const data = {
          resourceType: _type,
          resourceId: _id,
          payload: this.currentItem,
          etag: this.currentItem._etag,
        }
        this.updateItem(data).then((result) => {
          this.$router.push({
            name: 'ItemList',
            params: {type: this.$route.params.type }
          })
        }, (error) => {
          console.log(error)
        })
      } else {
        const data = {
          resourceType: _type,
          payload: this.currentItem,
        }
        this.createItem(data).then((result) => {
          this.$router.push({
            name: 'ItemList',
            params: {type: this.$route.params.type }
          })
        }, (error) => {
          console.log(error)
        })
      }
    },
    deleteResource() {
      const data = {
        resourceType: this.$route.params.type,
        resourceId: this.$route.params.id,
        etag: this.currentItem._etag
      }
      this.deleteItem(data).then((result) => {
          this.$router.push({
            name: 'ItemList',
            params: {type: this.$route.params.type }
          })
      }, (error) => {
        console.log(error)
      })
    },
  },
}
</script>

<style lang="scss">
  @import '../scss/settings';
  pre {
    padding: 50px;
    background-color: #f1f1f1;
  }
  textarea {
    height: 250px;
  }
  .form-field {
    margin-bottom: 50px;
    padding: 20px;
    background-color: #f1f1f1;
  }
  .sub-field {
    background-color: #f9f9f9;
    padding: 10px;
    margin-top: 25px;
    margin-bottom: 25px;
    border-bottom: 1px solid #fff;
    .sub-field {
      border-bottom: none;
    }
  }
</style>
