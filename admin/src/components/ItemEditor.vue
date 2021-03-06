<template>
  <div id="main-index" class="takeover" :class="{'setHeight': showItemDiff}" v-if="loaded">
    <div class="row align-center">
      <div class="columns small-12 medium-8 padding-lg">
        <router-link :to="{name: 'ItemList', params: {type: $route.params.type}}" class="close">
          <i class="fas fa-times-circle"></i>
        </router-link>
        <h2 v-if="currentItem" class="title-case">
          {{currentItem.title || `New ${$route.params.type}`}}
        </h2>
        <div v-if="currentItem" class="row">
          <div class="columns shrink">
            <b>Current Version:</b> {{currentItem._version}}
          </div>
          <div class="columns">
            <b>Latest Version:</b> {{currentItem._latest_version}}
          </div>
          <!-- TODO: Milestone 1.2 -->
          <!-- <div class="columns shrink text-right">
            <a href="#diff" @click.prevent="showDiff">Show Version History</a>
          </div> -->
          <!-- END -->
          <div class="columns small-12 padding-sm">
            <select
              name="version"
              id="version-select"
              v-if="parseInt(currentItem._latest_version) > 1"
              v-model="selectedVersion"
              @change="selectVersion"
            >
              <option :value="n" v-for="n in parseInt(currentItem._latest_version)">
                Version {{n}}
              </option>
            </select>
          </div>
          <div class="diffs padding-md" v-if="showItemDiff">
            <a href="#closeDiff" class="close" @click.prevent="closeDiff">
              <i class="fas fa-times-circle"></i>
            </a>
            <div v-for="(diff, idx) in itemDiff._items" class="row align-center padding-sm">
              <div class="columns small-12 medium-8">
                <h4>
                  Version {{diff._version}}
                </h4>
                <table>
                  <thead>
                    <tr>
                      <th width="200">Updated Property</th>
                      <th>Previous Value</th>
                      <th>Current Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(value, key) in diff" v-if="validDiffValue(key)">
                      <td>{{key}}</td>
                      <td>
                        <div v-if="idx > 0">
                          <div v-if="valueType(value) === 'simple'">
                            {{lastVersionValue(key, idx) || 'Value not set'}}
                          </div>
                          <div v-if="valueType(value) === 'array'">
                            <div v-for="sub in lastVersionValue(value)">
                              {{sub}}
                            </div>
                          </div>
                          <div v-if="valueType(value) === 'object'">
                            <div v-for="sub in lastVersionValue(value)">
                              {{sub}}
                            </div>
                          </div>
                        </div>
                        <div v-if="idx === 0">
                          &mdash;
                        </div>
                      </td>
                      <td>
                        <div v-if="valueType(value) === 'simple'">
                          {{value}}
                        </div>
                        <div v-if="valueType(value) === 'array'">
                          <div v-for="sub in value">
                            {{sub}}
                          </div>
                        </div>
                        <div v-if="valueType(value) === 'object'">
                          <div v-for="sub in value">
                            {{sub}}
                          </div>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div class="text-right">
                  <a href="#selectVersion" @click.prevent="specifyVersion(parseInt(diff._version))">
                    Select this version
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-for="property in properties" class="form-field" :class="{error: getError(property)}" v-if="propertyMetaAttr(property, 'field')">
          <component
            :is="propertyMetaAttr(property, 'field')"
            :name="property"
            :help="propertyMetaAttr(property, 'help')"
            :label="propertyMetaAttr(property, 'label')"
            :relationship="propertyMetaAttr(property, 'relationship')"
            :choices="propertyMetaAttr(property, 'choices')"
            :schema="propertySchema(property)"
            :anyof="propertyAnyOf(property)"
            :set="setter(property)"
            :data="getter(property)"
          ></component>
          <div class="error-msg" v-if="getError(property)">
            {{propertyMetaAttr(property, 'error') || 'This field contains errors'}}
          </div>
        </div>
      </div>
    </div>
    <div class="row align-center">
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
import textfield from '@/components/fields/textfield'
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
    textfield,
  },
  mixins: [field],
  name: 'itemEditor',
  watch: {
    '$route': 'refreshData',
    currentItem(val) {
      this.selectedVersion = val._version || null
    },
  },
  mounted() {
    this.refreshData()
  },
  data() {
    return {
      loaded: false,
      selectedVersion: null,
      showItemDiff: false,
      errors: [],
    }
  },
  computed: {
    ...mapGetters(['itemDiff']),
  },
  methods: {
    ...mapActions([
      'createItem',
      'updateItem',
      'deleteItem',
      'getItemDiff',
      'notify',
    ]),
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

      const _type = this.$route.params.type
      const _id = this.$route.params.id

      this.getCurrentSchema(this.$route.params.type)

      if (_id) {
        this.getCurrentItem({
          resourceId: _id,
          resourceType: _type,
        }).then((result) => {
          this.loaded = true
        }).catch((error) => {
          // TODO: Handle Error with Notification
          this.$router.push({ name: 'Index' })
        })
      } else {
        this.loaded = true
      }
    },
    specifyVersion(version) {
      this.selectedVersion = version
      this.showItemDiff = false
      this.selectVersion()
    },
    selectVersion() {
      this.loaded = false

      const _type = this.$route.params.type
      const _id = this.$route.params.id

      if (_id) {
        this.getCurrentItem({
          resourceId: _id,
          resourceType: _type,
          params: {
            version: parseInt(this.selectedVersion),
          },
        }).then((result) => {
          this.loaded = true
        }).catch((error) => {
          // TODO: Handle Error with notification
          this.$router.push({ name: 'Index' })
        })
      } else {
        this.loaded = true
      }
    },
    showDiff() {
      const _type = this.$route.params.type
      const _id = this.$route.params.id

      if (_id) {
        this.getItemDiff({
          resourceId: _id,
          resourceType: _type,
        }).then((result) => {
          this.showItemDiff = true
        }).catch((error) => {
          // TODO: Handle Error with notification
          this.showItemDiff = false
        })
      } else {
        this.showItemDiff = false
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
          this.notify({
            msg: 'Item saved!',
            type: 'success',
          })
          this.$router.push({
            name: 'ItemList',
            params: {type: this.$route.params.type }
          })
        }).catch((error) => {
          this.handleError(error)
        })
      } else {
        const data = {
          resourceType: _type,
          payload: this.currentItem,
        }
        this.createItem(data).then((result) => {
          this.notify({
            msg: 'Item saved!',
            type: 'success',
          })
          this.$router.push({
            name: 'ItemList',
            params: {type: this.$route.params.type }
          })
        }).catch((error) => {
          this.handleError(error)
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
        this.handleError(error)
      })
    },
    validDiffValue(value) {
      return !R.startsWith('_', value)
    },
    lastVersionValue(key, idx) {
      const allValues = R.slice(0, idx, R.map(item => item[key], this.itemDiff._items))
      const validValues = R.filter(
        item => typeof item !== 'undefined' && item !== null,
        allValues
      )
      return R.last(validValues)
    },
    valueType(value) {
      if (R.is(Object, value)) {
        return 'object'
      }
      if (R.is(Array, value)) {
        return 'array'
      }
      return 'simple'
    },
    closeDiff() {
      this.getItemDiff({})
      this.showItemDiff = false;
    },
    handleError(error) {
      if (error.response.status === 412) {
        this.notify({
          msg: 'Oops! It looks like someone else has edited this document. Please refresh the page for the latest version.',
          type: 'warning',
        })
      }
      if (error.response.status === 404) {
        this.notify({
          msg: 'Oops! It looks like you are trying to edit a resource that no longer exists.',
          type: 'warning',
        })
        this.$router.push({
          name: 'ItemList',
          params: {type: this.$route.params.type }
        })
      }
      if (error.response.status === 422) {
        this.notify({
          msg: 'Oops! Your updates contain validation errors.',
          type: 'warning',
        })
        if (error.response.data && error.response.data._issues) {
          this.errors = R.keys(error.response.data._issues)
        }
      }
      if (error.response.status === 500) {
        this.notify({
          msg: 'Something went wrong! Please try again in a moment.',
          type: 'warning',
        })
      }
    },
    getError(property) {
      return R.contains(property, this.errors)
    },
  },
}
</script>

<style lang="scss">
  @import '../scss/settings';

  .takeover {
    background-color: $white;
    position: absolute;
    min-height: 100vh;
    width: 100vw;
    left: 0;
    top: 0;
    &.setHeight {
      height: 100vh !important;
      overflow: hidden;
    }
    z-index: 3;
  }

  .close {
    position: fixed;
    top: 20px;
    right: 30px;
    width: 20px;
    height: 20px;
    font-size: 25px;
  }

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
  .diffs {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    overflow: scroll;
    background-color: #fff;
  }
  .error-msg {
    color: $warning-color;
  }
  .error {
    border: 2px solid $warning-color;
  }
</style>
