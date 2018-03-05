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
    ...mapActions(['getSchema']),
  },
  mounted() {
    this.getSchema()
  }
}
</script>

<style lang="scss">
  @import './scss/main.scss';
</style>
