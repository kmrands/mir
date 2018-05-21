<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <wysiwyg :name="name" v-model="scopedData" />
  </div>
</template>

<script>

import field from '@/mixins/field'

export default {
  name: 'richtext',
  mixins: [field],
}
</script>

<style lang="scss">
@import "../../scss/settings";

.editr--content {
  min-height: 500px;
  color: $dark-gray;
  background-color: $white;
}
</style>
