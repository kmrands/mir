<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <textarea :name="name" v-model="scopedData"></textarea>
  </div>
</template>

<script>
import field from '@/mixins/field'

export default {
  name: 'richtext',
  mixins: [field],
}
</script>
