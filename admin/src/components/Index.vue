<template>
  <div id="main-index">
    <!-- TODO: Implement Media Library -->
    <!-- <mediaLibrary :addToPost="false"></mediaLibrary> -->
    <div class="row fullWidth top-menu">
      <div class="columns">

      </div>
    </div>
    <div class="row fullWidth">
      <div class="columns collapse shrink main-menu padding-sm">
        <h6 class="list-title"><b>Site Resources</b></h6>
        <ul class="resources item-list">
          <li class="item" v-for="(value, key) in schema" v-if="validRoute(key)">
            <router-link :to="{name: 'ItemList', params: {type: key}}">
              {{key}}
            </router-link>
          </li>
          <li class="item">
            <a href="#signout" @click.prevent="logout">Sign Out</a>
          </li>
        </ul>
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

.list-title {
  padding: 0 25px 15px;
  margin: 0;
  color: $light-gray;
  border-bottom: 1px solid lighten($black, 2%);
}

.item-list {
  margin: 0;
  list-style-type: none;
}

.item {
  text-transform: capitalize;
  padding: 0;
  margin: 0;
  border-bottom: 1px solid lighten($black, 2%);
  width: 250px;
}

.item a {
  padding: 15px 25px;
  font-weight: 400;
  background: $black;
  color: $light-gray;
  display: block;
  &.router-link-active {
    background: darken($black, 10%);
    color: $white;
  }
}

.main-menu {
  background-color: $black;
  min-height: 100vh;
}
</style>
