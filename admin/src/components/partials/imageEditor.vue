<template>
  <div>
    <div class="row">
      <div class="columns small-12 medium-8">
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
        <a href="#Copy" class="button" @click.prevent="copyUrl()">Copy URL</a>
        <a :href="outUrl" target="_blank" class="button secondary">Visit URL</a>
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
  props: ['editUrl', 'set'],
  components: {
    slider,
  },
  data() {
    return {
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
  },
  methods: {
    ...mapActions(['notify']),
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
  }
}
</script>

<style lang="scss">
</style>
