<template>
  <div id="media-library" class="media-library">
    <div class="row fullWidth padding-sm" v-if="mediaLibrary && mediaLibrary._items">
      <!-- <div class="column small-12 medium-4 large-2" v-for="item in mediaLibrary._items"> -->
      <div v-for="item in mediaLibrary._items">
        {{item._id}}<br />
        {{getCloudUrl(item.item, { width: 100, crop: "fit"})}}
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
  mounted() {
    this.getMediaLibrary()
  },
  computed: {
    ...mapGetters(['mediaLibrary']),
  },
  methods: {
    ...mapActions(['getMediaLibrary']),
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
</style>
