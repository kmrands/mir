<template>
  <div id="main-index">
    <transition name="notify">
      <div
        class="notification"
        @click="closeNotification"
        v-if="notification"
        :class="`${notification.type}`"
      >
        <span>
          {{notification.msg}}
        </span>
      </div>
    </transition>
    <div class="row fullWidth top-menu">
      <div class="columns">
      </div>
    </div>
    <div class="row fullWidth align-right">
      <div class="columns small-2 collapse main-menu padding-sm">
        &nbsp;
        <ul class="resources item-list">
          <li class="item">
            <router-link :to="{path: '/'}">Main Dashboard</router-link>
          </li>
          <li class="item">
            <router-link :to="{name: 'ItemList', params: {type: 'configuration'}}">Site Configuration</router-link>
          </li>
          <li class="item">
            <router-link :to="{path: '/media'}">Media Library</router-link>
          </li>
          <li class="item" v-for="(value, key) in schema" v-if="validRoute(key)">
            <router-link :to="{name: 'ItemList', params: {type: key}}">
              {{splitResourceName(key)}}
            </router-link>
          </li>
          <li class="item">
            <a href="#signout" @click.prevent="logout">Sign Out</a>
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
import { mapGetters, mapActions } from 'vuex'

import mediaLibrary from '@/components/MediaLibrary'
import blacklist from '@/mixins/blacklist'

export default {
  name: 'index',
  mixins: [blacklist],
  mounted() {
    document.body.style.overflow = 'scroll'
  },
  components: {
    mediaLibrary,
  },
  computed: {
    ...mapGetters(['schema', 'notification'])
  },
  methods: {
    ...mapActions(['notify']),
    logout() {
      localStorage.setItem('token', null)
      localStorage.setItem('username', null)
      this.$router.push('/login')
    },
    closeNotification() {
      this.notify(null)
    },
    splitResourceName(name) {
      return name.replace('_', ' ')
    }
  }
}
</script>

<style lang="scss">
@import '../scss/settings';
@import '../scss/main';

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
  width: 100%;
}

.item {
  text-transform: capitalize;
  padding: 0;
  margin: 0;
  border-bottom: 1px solid lighten($black, 2%);
  width: 100%;
}

.item a {
  padding: 15px 25px;
  font-weight: 400;
  background: $black;
  color: $light-gray;
  display: block;
  &:hover {
    background: darken($black, 5%);
  }
  &.router-link-active {
    background: darken($black, 10%);
    color: $white;
  }
}

.main-menu {
  @include grid-column(2);
  padding: 0 !important;
  margin: 0;
  background-color: $black;
  min-height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
}

.notification {
  cursor: pointer;
  position: fixed;
  top: 25px;
  right: 50px;
  width: 300px;
  padding: 20px;
  &.alert {
    background-color: $alert-color;
  }
  &.success {
    background-color: $success-color;
  }
  &.warning {
    background-color: $warning-color;
  }
  span {
    color: $white;
  }
  z-index: 9;
}
</style>
