<template>
  <div>
    <!-- TODO: Implement Relationship / ObjectID -->
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <select name="" id="" v-model="scopedData">
      <option :value="item._id" v-for="item in relationshipCollection._items" v-if="relationshipCollection && relationshipCollection._items">
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
    this.getRelationshipCollection({
      resourceType: this.relationship,
      params: {
        max_results: 500,
      },
    })
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
  },
}
</script>
