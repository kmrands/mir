<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'app',
  methods: {
    ...mapActions(['getSchema', 'getSettings']),
    fetchSettings() {
      if (!this.settings) {
        this.getSettings()
      }
    }
  },
  computed: {
    ...mapGetters(['settings']),
  },
  watch: {
    '$route': 'fetchSettings'
  },
  mounted() {
    this.getSchema()
    this.getSettings()
  },
}
</script>

<style lang="scss">
  @import './scss/main.scss';
</style>
