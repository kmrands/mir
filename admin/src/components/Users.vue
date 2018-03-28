<template>
  <div id="users">
    <div class="row align-center">
      <div class="columns small-12 medium-8 secondary-menu padding-lg">
      </div>
    </div>
  </div>
</template>

<script>
import * as R from 'ramda'

import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Users',
  data() {
    return {
    }
  },
  mounted() {
  },
  methods: {
    ...mapActions(['getCurrentCollection']),
  },
  computed: {
    ...mapGetters(['currentCollection']),
  },
}
</script>

<style lang="scss">
  @import '../scss/settings';
</style>
