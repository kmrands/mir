<template>
  <div id="item-list" v-if="loaded">
    <div class="row">
      <div class="columns small-2">
        <ul>
          <li class="item" v-for="item in currentCollection._items" v-if="currentCollection && currentCollection._items">
            <router-link :to="{name: 'ItemEditor', params: {type: $route.params.type, id: item._id}}">
              {{item.title || item.slug}}
            </router-link>
          </li>
        </ul>
        <div>
          <router-link :to="{name: 'ItemCreator', params: {type: $route.params.type}}" class="button">Create New Item</router-link>
        </div>
      </div>
      <div class="columns small-10">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

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
    ...mapGetters(['currentCollection'])
  },
}
</script>

<style lang="scss">
  @import '../scss/settings';
</style>
