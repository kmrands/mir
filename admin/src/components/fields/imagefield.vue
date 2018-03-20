<template>
  <div>
    <!-- TODO: Implement Image Field -->
    <!-- <div class="upload">
      <label for="">{{label}}</label>
      <div class="help">{{help}}</div>

    </div> -->
  </div>
</template>

<script>
import field from '@/mixins/field'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'imagefield',
  mixins: [field],
  data() {
    return {
      id: null,
    }
  },
  created() {
    this.id = this.guid()
  },
  methods: {
    guid() {
      function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1)
      }
      return `${s4()}${s4()}-${s4()}-${s4()}-${s4()}-${s4()}${s4()}${s4()}`
    },
  },
}
</script>
