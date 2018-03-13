<template>
  <div id="media-library" class="media-library">
    <input id="addImage" type="file" @change="onFileChange($event)" class="hidden" multiple>
    <div class="row fullWidth padding-sm">
      <div class="columns small-12 medium-6">
        <h2>Media Library</h2>
      </div>
      <div class="columns small-12 medium-6 text-right">
        <a href="#add" class="button" @click.prevent="addMedia">Add Media</a>
      </div>
    </div>
    <div class="row fullWidth padding-sm" v-if="mediaLibrary && mediaLibrary._items && mediaLibrary._items.length > 0">
      <div class="column small-12 medium-4 large-2" v-for="item in mediaLibrary._items">
        <label>{{item.title}}</label>
        <img :src="getCloudUrl(item.item, { width: 200, crop: 'fit', quality:100})" alt="">
        <div class="controls padding-sm">
          <a href="#delete" class="button alert" @click.prevent="deleteMedia(item._id, item._etag)">Delete</a>
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
  </div>
</template>

<script>
import cloudinary from '@/mixins/cloudinary'
import { mapGetters, mapActions } from 'vuex'


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
    }
  },
  computed: {
    ...mapGetters(['mediaLibrary']),
  },
  methods: {
    ...mapActions([
      'getMediaLibrary',
      'deleteItem',
      'createItem',
    ]),
    deleteMedia(_id, _etag) {
      this.deleteItem({
        resourceType: 'media',
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
          resourceType: 'media',
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
  },
}
</script>

<style lang="scss">
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
</style>
