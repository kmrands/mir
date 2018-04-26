<template>
  <div id="media-library" class="">
    <div class="loading" v-if="loading">
      <i class="fas fa-spinner loading-icon"></i>
    </div>
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
        <!-- If image type -->
        <img class="library-img" :src="getCloudUrl(item._id, {thumbnail: '300,300'})" alt="" v-if="item.type === 'image' || !item.type">
        <!-- If video type -->
        <video class="library-video" :src="getCloudUrl(item._id)" v-if="item.type === 'video'"></video>
        <!-- If file type -->
        <div class="file" v-if="item.type === 'file'">
          <a :href="getCloudUrl(item._id)">
            <span class="icon">
              <i class="fas fa-file-alt"></i>
            </span>
          </a>
        </div>
        <br>
        <div v-if="item.title">
          <b>Title:</b> {{item.title}}<br />
        </div>
        <div v-if="item.tags">
          <b>Tags:</b> {{item.tags.join(', ')}}
        </div>
        <div class="controls padding-sm">
          <a href="#delete" class="button alert" @click.prevent="deleteMedia(item._id, item._etag)">Delete</a>
          <a href="#edit" class="button secondary" @click.prevent="edit(item)">Edit</a>
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
        <div>
          <label for="">Type</label>
          <select name="type" v-model="type">
            <option value="image">Image</option>
            <option value="video">Video</option>
            <option value="file">File</option>
          </select>
        </div>
        <div class="tags-form">
          <div class="tag row" v-for="(tag, ind) in tags" v-if="tags.length > 0">
            <div class="columns small-10"><input type="text" v-model="tags[ind]"></div>
            <div class="columns small-1">
              <a href="#remove-tag" class="remove" @click.prevent="removeTag(ind)">
                <i class="fas fa-minus-circle"></i>
              </a>
            </div>
          </div>
          <div>
            <a href="#new-tag" @click.prevent="addTag">Add a tag</a>
          </div>
        </div>
        <div class="padding-sm">
          <a href="" class="button" @click.prevent="upload">Upload</a>
          <a href="" class="button alert" @click.prevent="cancel">Cancel</a>
        </div>
      </div>
    </div>
    <div class="editor" v-show="editor">
      <a href="#close" class="close" @click.prevent="closeEditor()">
        <i class="fas fa-times-circle"></i>
      </a>
      <imageEditor :editUrl="editUrl" :item="editItem" :isImage="editItem && editItem.type === 'image'"></imageEditor>
    </div>
  </div>
</template>

<script>
import * as R from 'ramda'
import { mapGetters, mapActions } from 'vuex'
import VueCropper from 'vue-cropperjs'

import cloudinary from '@/mixins/cloudinary'
import imageEditor from '@/components/partials/imageEditor'

export default {
  name: 'mediaLibrary',
  mixins: [cloudinary],
  props: ['addToPost'],
  components: {
    imageEditor
  },
  mounted() {
    this.getMediaLibrary().then(() => {
      this.loading = false;
    })
  },
  data() {
    return {
      loading: true,
      uploading: false,
      type: null,
      title: null,
      tags: [],
      mediaSearch: null,
      editor: false,
      editUrl: null,
      editItem: null,
    }
  },
  computed: {
    ...mapGetters(['mediaLibrary']),
    searched() {
      if (this.mediaLibrary && this.mediaLibrary._items) {
        if (this.mediaSearch) {
          return R.filter((item) => {
            return R.contains(
              this.mediaSearch.toLowerCase(),
              item.title.toLowerCase()
            ) || R.contains(
              this.mediaSearch.toLowerCase(),
              R.map((tag) => tag.toLowerCase(), item.tags || [])
            )
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
        this.getMediaLibrary()
      }, (error) => {
        // TODO: Handle Error with notification
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
        formData.append('type', this.type)
        formData.append('title', this.title)
        formData.append('tags', JSON.stringify(this.tags))

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
          // TODO: Handle Error with notification
        })
      }
    },
    upload() {
      document.querySelector('#addImage').click()
    },
    copyUrl(_id) {
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
    edit(item) {
      this.editor = true
      this.editUrl = this.getCloudUrl(item._id)
      this.editItem = item
    },
    closeEditor() {
      this.editor = false
      this.editUrl = null
    },
    addTag() {
      this.tags.push('')
    },
    removeTag(ind) {
      this.tags.splice(ind, 1)
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
.library-video {
  width: 100%;
  height: auto;
}

.close {
  position: fixed;
  top: 20px;
  right: 30px;
  width: 20px;
  height: 20px;
  font-size: 25px;
}

.editor {
  padding: 50px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: $white;
  overflow: scroll;
}
.remove {
  font-size: 25px;
  color: $secondary-color;
}
.file a {
  display: block;
  background: $light-gray;
  width: 100%;
  height: 200px;
  text-align: center;

  .icon {
    font-size: 35px;
    display: block;
    position: relative;
    top: 50%;
    transform: translateY(-50%);
  }
}
</style>
