<template>
  <div id="item-list" v-if="loaded">
    <div class="row align-center">
      <div class="columns small-12 medium-8 secondary-menu padding-lg">
        <input type="text" :placeholder="`Search ${listTitle}`">
        <ul class="secondary-item-list">
          <li class="secondary-item" v-for="item in currentCollection._items" v-if="currentCollection && currentCollection._items">
            <router-link :to="{name: 'ItemEditor', params: {type: $route.params.type, id: item._id}}">
              {{item.title || item.slug}}
            </router-link>
          </li>
        </ul>
        <div class="padding-sm">
          <router-link :to="{name: 'ItemCreator', params: {type: $route.params.type}}" class="button">Create New Item</router-link>
        </div>
      </div>
    </div>
    <div>
      <router-view></router-view>
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
    },
  },
}
</script>

<style lang="scss">
  @import '../scss/settings';

  .secondary-item-list {
    list-style-type: none;
    margin: 0;
    padding: 0;
  }

  .secondary-item {
    margin: 0;
    padding: 0;
    border-bottom: 1px solid $light-gray;
    &:first-of-type {
      border-top: 1px solid $light-gray;
    }
  }

  .secondary-item a {
    display: block;
    padding: 15px 25px;
    &:hover {
      background-color: $black;
      color: $white;
    }
  }

</style>
