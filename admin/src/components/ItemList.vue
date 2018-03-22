<template>
  <div id="item-list" v-if="loaded">
    <div class="row">
      <div class="columns shrink secondary-menu padding-sm">
        <h4 class="title-case">{{listTitle}}</h4>
        <input type="text">
        <ul class="item-list">
          <li class="item" v-for="item in currentCollection._items" v-if="currentCollection && currentCollection._items">
            <router-link :to="{name: 'ItemEditor', params: {type: $route.params.type, id: item._id}}">
              {{item.title || item.slug}}
            </router-link>
          </li>
        </ul>
        <div class="padding-sm">
          <router-link :to="{name: 'ItemCreator', params: {type: $route.params.type}}" class="button">Create New Item</router-link>
        </div>
      </div>
      <div class="columns">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import pluralize from 'pluralize'

export default {
  components: {
  },
  name: 'ItemList',
  data() {
    return {
      loaded: false,
    }
  },
  watch: {
    '$route': 'refreshData',
  },
  mounted() {
    this.refreshData()
  },
  methods: {
    ...mapActions(['getCurrentCollection']),
    refreshData() {
      this.getCurrentCollection({ resourceType: this.$route.params.type }).then(() => {
        this.loaded = true
      })
    },
  },
  computed: {
    ...mapGetters(['currentCollection']),
    listTitle() {
      return pluralize(this.$route.params.type)
    }
  },
}
</script>

<style lang="scss">
  @import '../scss/settings';

  .secondary-menu {
    background-color: #f9f9f9;
    min-height: 100vh;
  }
</style>
