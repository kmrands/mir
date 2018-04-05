<template>
  <div id="slide-contain" class="slider-contain text-right" @click="setValue">
    <div class="slider-value" :style="{width: widthValue}">&nbsp;</div>
    <span>{{parseInt(value * 100)}}%</span>
  </div>
</template>

<script>
import * as R from 'ramda'
import VueCropper from 'vue-cropperjs'
import { mapGetters, mapActions } from 'vuex'


export default {
  name: 'slider',
  props: ['value', 'set'],
  data() {
    return {
      slideWidth: null,
    }
  },
  computed: {
    widthValue() {
      const val = (this.value / 2) * this.slideWidth
      if (val) {
        return `${val}px`
      } else {
        return '50%'
      }
    }
  },
  methods: {
    setValue(e) {
      const slideContain = document.getElementById('slide-contain')
      this.slideWidth = slideContain.clientWidth

      const val = e.offsetX / (this.slideWidth / 2)
      this.set(val)
    },
  },
}
</script>

<style lang="scss">
@import '../../scss/settings';

.slider-contain {
  background-color: $light-gray;
  height: 20px;
  width: 100%;
  position: relative;
  padding: 0 5px;

  .slider-value {
    position: absolute;
    top: 0;
    left: 0;
    height: 20px;
    width: 50%;
    background-color: $primary-color;
  }
  span {
    font-size: 11px;
    position: relative;
    top: -3px;
    color: $black;
  }
}
</style>
