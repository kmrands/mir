<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <div class="choice" v-for="choice in choices">
      <input type="checkbox" :name="choice" :value="choice" v-model="scopedData">
      {{choice}}
    </div>
  </div>
</template>

<script>
import field from '@/mixins/field'

export default {
  name: 'checklist',
  mixins: [field],
  computed: {
    scopedData: {
      get() {
        if (!this.data) return []
        return this.data
      },
      set(val) {
        this.set(val)
      }
    },
  },
}
</script>
