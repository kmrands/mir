<template>
  <div id="main-index">
    <!-- TODO: Implement Media Library -->
    <!-- <mediaLibrary :addToPost="false"></mediaLibrary> -->
    <div class="row fullWidth padding-sm">
      <div class="columns small-2">
        <ul>
          <li class="item" v-for="(value, key) in schema" v-if="validRoute(key)">
            <router-link :to="{name: 'ItemList', params: {type: key}}">
              {{key}}
            </router-link>
          </li>
          <li class="item">
            <a href="#logout" @click.prevent="logout">sign out</a>
          </li>
        </ul>
      </div>
      <div class="columns small-10">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import * as R from 'ramda'
import { mapGetters } from 'vuex'

import mediaLibrary from '@/components/MediaLibrary'
import blacklist from '@/mixins/blacklist'

export default {
  name: 'index',
  mixins: [blacklist],
  components: {
    mediaLibrary,
  },
  computed: {
    ...mapGetters(['schema'])
  },
  methods: {
    logout() {
      localStorage.setItem('token', null)
      localStorage.setItem('username', null)
      this.$router.push('/login')
    }
  }
}
</script>

<style lang="scss">
@import '../scss/settings';

.container {
  padding-bottom: 50px;
}

.fullWidth {
  width: 100% !important;
  margin-left: auto;
  margin-right: auto;
  max-width: initial;
}
</style>
