<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <input type="text" v-model="scopedData">
  </div>
</template>

<script>
import field from '@/mixins/field'

export default {
  name: 'slug',
  mixins: [field],
  computed: {
    scopedData: {
      get() {
        return this.data
      },
      set(val) {
        const slug = val.toString().toLowerCase()
        .replace(/\s+/g, '-')
        .replace(/[^\w\-]+/g, '')
        .replace(/\-\-+/g, '-')
        .replace(/^-+/, '')
        .replace(/-+$/, '')

        this.set(slug)
      }
    }
  },
}
</script>
