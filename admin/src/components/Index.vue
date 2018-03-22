<template>
  <div id="main-index">
    <!-- TODO: Implement Media Library -->
    <!-- <mediaLibrary :addToPost="false"></mediaLibrary> -->
    <div class="row fullWidth top-menu">
      <div class="columns">

      </div>
    </div>
    <div class="row fullWidth">
      <div class="columns shrink main-menu padding-sm">
        <h4>Resources</h4>
        <input type="text">
        <ul class="item-list">
          <li class="item" v-for="(value, key) in schema" v-if="validRoute(key)">
            <router-link :to="{name: 'ItemList', params: {type: key}}">
              {{key}}
            </router-link>
          </li>
        </ul>
        <div class="padding-sm">
            <a href="#logout" @click.prevent="logout" class="button">Sign Out</a>
        </div>
      </div>
      <div class="columns">
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
}

.fullWidth {
  width: 100% !important;
  margin-left: auto;
  margin-right: auto;
  max-width: initial;
}

.item-list {
  margin: 0;
  list-style-type: none;
}

.item a {
  font-weight: 400;
  text-transform: uppercase;
  color: $black;
  &.router-link-active {
    color: $primary-color;
  }
}

.main-menu {
  background-color: #f1f1f1;
  min-height: 100vh;
}
</style>
