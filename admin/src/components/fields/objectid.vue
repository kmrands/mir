<template>
  <div>
    <!-- TODO: Fix relationships so that more than one can exist per page -->
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <select name="" id="" v-model="scopedData">
      <option :value="item._id" v-for="item in related._items" v-if="related && related._items">
        {{item.title || item.slug || item._id}}
      </option>
    </select>
  </div>
</template>

<script>
import * as R from 'ramda'
import field from '@/mixins/field'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'objectid',
  mixins: [field],
  mounted() {
    if (!this.related) {
      this.getRelationshipCollection({
        resourceType: this.relationship,
        params: {
          max_results: 500,
        },
      })
    }
    if (R.is(Object, this.data)) {
      this.scopedData = this.data._id
    }
  },
  methods: {
    ...mapActions(['getRelationshipCollection'])
  },
  computed: {
    ...mapGetters(['relationshipCollection']),
    scopedData: {
      get() {
        if (!R.is(Object, this.data)) {
          return this.data
        }
        return this.data._id
      },
      set(val) {
        if (val === "") {
          this.set(null)
        } else {
          if (!R.is(Object, val)) {
            this.set(val)
          } else {
            this.set(val._id)
          }
        }
      }
    },
    related() {
      if (this.relationshipCollection[this.relationship]) {
        return this.relationshipCollection[this.relationship]
      }
      return null
    }
  },
}
</script>
