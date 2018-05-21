<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <textarea v-model="scopedData"></textarea>
  </div>
</template>

<script>
import field from '@/mixins/field'

export default {
  name: 'textfield',
  mixins: [field],
}
</script>
