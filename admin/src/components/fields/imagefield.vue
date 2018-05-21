<template>
  <div>
    <!-- TODO: Implement Image Field -->
    <div class="upload">
      <label for="">{{label}}</label>
      <div class="help">{{help}}</div>
      <div v-if="scopedData">
        <!-- TODO: Add video and file -->
        <div>
          <!-- image type -->
          {{getSrc}}
          <img :src="getSrc" alt="" v-if="filedata && filedata.type === 'image'">
          <!-- file type -->
          <div v-if="filedata && filedata.type === 'file'">
            <b>Content Type:</b> {{filedata.item.content_type}}<br />
            <b>Name:</b> {{filedata.item.name}}<br /><br />
            <a :href="getCloudUrl(filedata._id)" target="_blank" class="button small secondary">View File</a>
          </div>
          <!-- video type -->
          <video :src="getCloudUrl(filedata._id)" v-if="filedata && filedata.type === 'video'"></video>
        </div>
        <a href="#remove" class="button" @click.prevent="removeImage">Remove Media</a>
      </div>
      <div v-if="!scopedData">
        <a href="#add" class="button" @click.prevent="addImage">Add Media</a>
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
        <div class="column small-12 medium-4 large-3 library-item" v-for="item in searched">
          <!-- TODO: Add video and file -->
          <img
            class="library-img"
            :src="getCloudUrl(item._id, { thumbnail: '200,200'})"
            alt=""
            @click.prevent="selectImage(item)"
          >
          <!-- file type -->
          <div v-if="item.type === 'file'">
            <b>Content Type:</b> {{item.item.content_type}}<br />
            <b>Name:</b> {{item.item.name}}<br /><br />
            <a href="#select" @click.prevent="selectImage(item)" class="button">select</a>
          </div>
          <!-- video type -->
          <video @click.prevent="selectImage(item)" :src="getCloudUrl(item._id)" v-if="item.type === 'video'"></video>
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
import api from '@/lib/api'
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
      filedata: null,
      loaded: false,
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
    if (this.scopedData && this.scopedData.item) {
      this.filedata = this.scopedData
      this.set(this.scopedData._id)
      this.loaded = true
    }
    if (this.scopedData && !this.scopedData.item) {
      api.getResource(`sitemedia/${this.scopedData}`).then((result) => {
        if (result) {
          this.filedata = result
          this.set(result._id)
          this.loaded = true
        }
      })
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
    },
    getSrc() {
      if (this.filedata) {
        return this.getCloudUrl(this.filedata._id)
      } else {
        if (this.scopedData && !this.scopedData.item) {
          api.getResource(`sitemedia/${this.scopedData}`).then((result) => {
            if (result) {
              this.filedata = result
            }
          })
        }
      }
    },
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
      if (!this.mediaLibrary._items) {
        this.getMediaLibrary()
      }
      this.showLibrary = true
    },
    closeLibrary() {
      this.showLibrary = false
    },
    selectImage(img) {
      this.set(img._id)
      this.filedata = img
      this.showLibrary = false;
    },
    removeImage() {
      this.set(null)
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

.library-item {
  img, video {
    width: 100%;
    height: auto;
  }
}
</style>
