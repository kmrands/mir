<template>
  <div id="media-library" class="">
    <input id="addImage" type="file" @change="onFileChange($event)" class="hidden" multiple>
    <div class="row fullWidth padding-sm">
      <div class="columns small-12 medium-6">
        <h2>Media Library</h2>
      </div>
      <div class="columns small-12 medium-6 text-right">
        <a href="#add" class="button" @click.prevent="addMedia">Add Media</a>
      </div>
      <div class="columns small-12">
        <input type="text" placeholder="Search media" v-model="mediaSearch">
      </div>
    </div>
    <div class="row fullWidth padding-sm" v-if="mediaLibrary && mediaLibrary._items && mediaLibrary._items.length > 0">
      <div class="column small-12 medium-4 large-3" v-for="item in searched">
        <img class="library-img" :src="getCloudUrl(item._id)" alt="">
        <div v-if="item.title">
          {{item.title}}
        </div>
        <div class="controls padding-sm">
          <a href="#delete" class="button alert" @click.prevent="deleteMedia(item._id, item._etag)">Delete</a>
          <a href="#edit" class="button secondary" @click.prevent="edit(item._id)">Edit</a>
          <a href="#copy" class="button" @click.prevent="copyUrl(item._id)">Copy URL</a>
        </div>
      </div>
    </div>
    <div class="upload-form-container" v-if="uploading">
      <div class="upload-form">
        <div>
          <label for="">Title</label>
          <input type="text" v-model="title">
        </div>
        <a href="" class="button" @click.prevent="upload">Upload</a>
        <a href="" class="button alert" @click.prevent="cancel">Cancel</a>
      </div>
    </div>
    <div class="editor" v-show="editor">
      <a href="#close" class="close" @click.prevent="closeEditor()">
        <i class="fas fa-times-circle"></i>
      </a>
      <div class="row">
        <div class="columns small-12 medium-8">
          <div class="image-editor" v-if="editId">
            <vue-cropper
              :src="getCloudUrl(editId)"
              :zoomable="false"
            ></vue-cropper>
          </div>
        </div>
        <div class="columns small-12 medium-4">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as R from 'ramda'
import cloudinary from '@/mixins/cloudinary'
import { mapGetters, mapActions } from 'vuex'

import VueCropper from 'vue-cropperjs'


export default {
  name: 'mediaLibrary',
  mixins: [cloudinary],
  props: ['addToPost'],
  mounted() {
    this.getMediaLibrary()
  },
  data() {
    return {
      loading: false,
      uploading: false,
      type: null,
      title: null,
      mediaSearch: null,
      editor: false,
      editId: null,
      cropper: null,
    }
  },
  watch: {
    editId(val) {
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
    ...mapActions([
      'getMediaLibrary',
      'deleteItem',
      'createItem',
      'notify',
    ]),
    deleteMedia(_id, _etag) {
      this.deleteItem({
        resourceType: 'sitemedia',
        resourceId: _id,
        etag: _etag
      }).then((result) => {
        console.log(result)
        this.getMediaLibrary()
      }, (error) => {
        console.log(error)
      })
    },
    addMedia() {
      this.uploading = true
    },
    cancel() {
      this.uploading = false
      this.title = null
    },
    onFileChange(e) {
      const files = e.target.files || e.dataTransfer.files
      let formData = null

      for (let i = 0; i < files.length; i += 1) {
        formData = new FormData()
        formData.append('item', files[i])
        // formData.append('type', this.type)
        formData.append('title', this.title)

        this.loading = true
        this.uploading = false

        this.createItem({
          resourceType: 'sitemedia',
          payload: formData,
        }).then(() => {
          this.getMediaLibrary({
            params: {
              max_results: 200,
            },
          }).then(() => {
            this.loading = false
          })
        }, (error) => {
          console.log(error)
        })
      }
    },
    upload() {
      document.querySelector('#addImage').click()
    },
    copyUrl(_id) {
      console.log(`${window.location.protocol}//${window.location.host}/`)
      var textArea = document.createElement("textarea");
      textArea.value = process.env.SERVER !== ''
        ? `${process.env.SERVER}/api/images/${_id}`
        : `${window.location.protocol}//${window.location.host}/api/images/${_id}`
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();

      try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        this.notify({
          msg: "Copied to clipboard successfully!",
          type: "success"
        })
      } catch (err) {
        this.notify({
          msg: "Copy to clipboard failed!",
          type: "warning"
        })
      }

      document.body.removeChild(textArea);
    },
    edit(_id) {
      this.editor = true
      this.editId = _id
    },
    closeEditor() {
      this.editor = false
      this.editId = null
      this.cropper.destroy()
    },
  },
}
</script>

<style lang="scss">
@import '../scss/settings';
.media-library {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  min-height: 100vh;
  background-color: #f1f1f1;
}
.upload-form-container {
  background-color: rgba(0,0,0,.8);
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
}
.upload-form {
  width: 500px;
  height: auto;
  background-color: #fff;
  margin-left: -250px;
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translateY(-50%);
  padding: 50px 50px 30px;
}
.hidden {
  display: none;
}
.library-img {
  border: 1px solid $light-gray;
}

.close {
  position: fixed;
  top: 20px;
  right: 25px;
}

.editor {
  padding: 50px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: $white;
}
</style>
