<template>
  <div>
    <!-- TODO: Implement Image Field -->
    <div class="upload">
      <label for="">{{label}}</label>
      <div class="help">{{help}}</div>
      <div v-if="scopedData">
        <img :src="getSrc(url)" alt="">
        <a href="#remove" class="button" @click.prevent="removeImage">Remove Image</a>
      </div>
      <div v-if="!scopedData">
        <a href="#add" class="button" @click.prevent="addImage">Add Image</a>
      </div>
    </div>
    <div class="library" v-if="showLibrary">
      <a href="#close" class="close" @click.prevent="closeLibrary">
        <i class="fas fa-times-circle"></i>
      </a>
      <div class="row library-content padding-lg" v-if="mediaLibrary && mediaLibrary._items && mediaLibrary._items.length > 0">
        <div class="columns small-12">
          <input type="text" v-model="mediaSearch" placeholder="Search media">
        </div>
        <hr>
        <div class="column small-12 medium-4 large-3" v-for="item in searched">
          <img
            class="library-img"
            :src="getCloudUrl(item.item, { width: 200, crop: 'fit', quality:100})"
            alt=""
            @click.prevent="selectImage(item)"
          >
          <div v-if="item.title">
            {{item.title}}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as R from 'ramda'
import field from '@/mixins/field'
import { mapGetters, mapActions } from 'vuex'

import cloudinary from '@/mixins/cloudinary'

export default {
  name: 'imagefield',
  mixins: [field, cloudinary],
  data() {
    return {
      id: null,
      showLibrary: false,
      mediaSearch: null,
      url: null,
    }
  },
  watch: {
    showLibrary(val) {
      if (val) {
        document.body.style.height = "100vh"
        document.body.style.overflow = "hidden"
      } else {
        document.body.style.height = "auto"
        document.body.style.overflow = "auto"
      }
    }
  },
  created() {
    this.id = this.guid()
  },
  mounted() {
    if (!this.mediaLibrary._items) {
      this.getMediaLibrary()
    }
    if (this.scopedData && this.scopedData.item) {
      this.url = this.scopedData.item
    }
  },
  computed: {
    ...mapGetters(['mediaLibrary']),
    searched() {
      if (this.mediaLibrary && this.mediaLibrary._items) {
        if (this.mediaSearch) {
          return R.filter((item) => {
            return R.contains(this.mediaSearch.toLowerCase(), item.title.toLowerCase())
          }, this.mediaLibrary._items)
        }
        return this.mediaLibrary._items
      }
    }
  },
  methods: {
    ...mapActions(['getMediaLibrary']),
    guid() {
      function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1)
      }
      return `${s4()}${s4()}-${s4()}-${s4()}-${s4()}-${s4()}${s4()}${s4()}`
    },
    addImage() {
      this.showLibrary = true
    },
    closeLibrary() {
      this.showLibrary = false
    },
    selectImage(img) {
      this.set(img._id)
      this.url = img.item
      this.showLibrary = false;
    },
    removeImage() {
      this.set(null)
    },
    getSrc(url) {
      return process.env.SERVER !== '' ? `${process.env.SERVER}${url}` : url
    },
  },
}
</script>

<style lang="scss">
@import "../../scss/settings";

.library {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: scroll;
  background-color: $light-gray;
  z-index: 8;
}

.library-content {
  width: 90vw;
  margin: 0 auto !important;
  .library-img {
    cursor: pointer;
  }
}
</style>
