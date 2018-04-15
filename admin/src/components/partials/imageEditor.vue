<template>
  <div>
    <div class="row controls padding-sm">
      <div class="columns">
        <div class="button-group alert expanded">
          <a href="#visual" class="button" @click.prevent="editorType(true)">Visual Editor</a>
          <a href="#meta" class="button" @click.prevent="editorType(false)">Metadata Editor</a>
        </div>
      </div>
    </div>
    <div class="row visual" v-if="visual">
      <div class="columns small-12 medium-8">
        <p>You are using the Visual Image Editor. No changes will be saved to your original image.</p>
        <div class="image-editor" v-if="editUrl">
          <vue-cropper
            ref="cropper"
            :src="editUrl"
            :zoomable="false"
            :crop="setUrl"
          ></vue-cropper>
        </div>
      </div>
      <div class="columns small-12 medium-4">
        <div class="padding-sm">
          <label for="contrast">Contrast</label>
          <slider :value="contrast" :set="setter('contrast')"></slider>
          <br />
          <label for="contrast">Saturation</label>
          <slider :value="saturation" :set="setter('saturation')"></slider>
          <br />
          <label for="contrast">Brightness</label>
          <slider :value="brightness" :set="setter('brightness')"></slider>
          <br />
          <label for="contrast">sharpness</label>
          <slider :value="sharpness" :set="setter('sharpness')"></slider>
          <br />
          <label for="contrast">blur</label>
          <slider :value="blur" :set="setter('blur')"></slider>
          <br />
        </div>
        <a href="#Copy" class="button" @click.prevent="copyUrl()">Copy URL</a>
        <a :href="outUrl" target="_blank" class="button secondary">Visit URL</a>
      </div>
    </div>
    <div class="row metadata" v-if="!visual">
      <div class="columns small-12 medium-8">
        <p>You are using the Metadata Editor. Update the tags and title for your image.</p>
        <img class="library-img" :src="editUrl" alt="">
      </div>
      <div class="columns small-12 medium-4">
        <div>
          <label for="">
            Title
          </label>
          <input type="text" v-model="editable.title">
        </div>
        <div class="tags-form">
          <label for="">
            Tags
          </label>
          <div class="tag row" v-for="(tag, ind) in editable.tags" v-if="editable.tags.length > 0">
            <div class="columns small-10"><input type="text" v-model="editable.tags[ind]"></div>
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
        <div class="controls padding-sm">
          <a href="#save" class="button" @click.prevent="save">Save</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as R from 'ramda'
import VueCropper from 'vue-cropperjs'
import { mapGetters, mapActions } from 'vuex'

import slider from '@/components/partials/slider'

export default {
  name: 'imageEditor',
  props: ['editUrl', 'set', 'item'],
  components: {
    slider,
  },
  data() {
    return {
      visual: true,
      outUrl: null,
      contrast: 1,
      saturation: 1,
      blur: 0,
      brightness: 1,
      sharpness: 1,
    }
  },
  watch: {
    imageAttrs() {
      this.setUrl()
    },
    editUrl() {
      console.log('test')
      this.contrast = 1
      this.saturation = 1
      this.blur = 0
      this.brightness = 1
      this.sharpness = 1
    },
  },
  mounted() {
    this.outUrl = this.editUrl
  },
  computed: {
    imageAttrs() {
      return [
        this.contrast,
        this.saturation,
        this.blur,
        this.brightness,
        this.sharpness,
      ].join()
    },
    editable() {
      return this.item
    },
  },
  methods: {
    ...mapActions(['notify', 'updateItem']),
    copyUrl() {
      var textArea = document.createElement("textarea");
      textArea.value = this.outUrl
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
    setUrl(e) {
      if (e) {
        const fullWidth = e.target.naturalWidth
        const fullHeight = e.target.naturalHeight
        const height = e.detail.height
        const width = e.detail.width
        const x = e.detail.x
        const y = e.detail.y

        this.outUrl = `
          ${this.editUrl}
          ?crop=${parseInt(width)},${parseInt(height)},${parseInt((x/fullWidth)*100)},${parseInt((y/fullHeight)*100)}
          &contrast=${this.contrast}
          &saturation=${this.saturation}
          &blur=${this.blur * 5}
          &brightness=${this.brightness}
          &sharpness=${this.sharpness}
        `.replace(/\s/g, '')

      } else {
        this.outUrl = `
          ${this.outUrl.split('&', 1)[0]}
          &contrast=${this.contrast}
          &saturation=${this.saturation}
          &blur=${this.blur * 5}
          &brightness=${this.brightness}
          &sharpness=${this.sharpness}
        `.replace(/\s/g, '')

        const base = this.outUrl.split('?')
        const end = base[1]

        this.$refs.cropper.replace(`${base[0]}?${R.tail(end.split('&')).join('&')}`, true)
      }
    },
    setter(name) {
      return (val) => {
        if (val) {
          this[name] = val
        }
      }
    },
    editorType(visual) {
      this.visual = visual
    },
    addTag() {
      this.item.tags.push('')
    },
    removeTag(ind) {
      this.item.tags.splice(ind, 1)
    },
    save() {
      const data = {
        resourceType: 'sitemedia',
        resourceId: this.item._id,
        payload: R.omit(['item'], this.editable),
        etag: this.editable._etag,
      }
      console.log(data.payload)
      this.updateItem(data).then((result) => {
        this.notify({
          msg: 'Item saved!',
          type: 'success',
        })
      }).catch((error) => {
        console.log(error)
      })
    },
  }
}
</script>

<style lang="scss">
</style>
