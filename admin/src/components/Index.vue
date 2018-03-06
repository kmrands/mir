<template>
  <div id="main-index">
    <mediaLibrary></mediaLibrary>
    <div class="row fullWidth padding-sm">
      <div class="columns small-1">
        <ul>
          <li class="item" v-for="(value, key) in schema" v-if="key !== 'media'">
            <router-link :to="{name: 'ItemList', params: {type: key}}">
              {{key}}
            </router-link>
          </li>
        </ul>
      </div>
      <div class="columns small-11">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import mediaLibrary from '@/components/MediaLibrary'

export default {
  name: 'index',
  components: {
    mediaLibrary,
  },
  computed: {
    ...mapGetters(['schema'])
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
