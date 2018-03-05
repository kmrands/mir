<template>
  <div>
    <div class="upload-form">
      <label for="">{{label}}</label>
      <div class="help">{{help}}</div>

    </div>
    <div class="media-library">

    </div>
  </div>
</template>

<script>
import field from '@/mixins/field'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'imagefield',
  mixins: [field],
  mounted() {
    this.getMediaLibrary()
  },
  methods: {
    ...mapActions(['getMediaLibrary'])
  },
  computed: {
    ...mapGetters(['mediaLibrary'])
  }
}
</script>
