<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <input type="text" v-model="scopedData">
  </div>
</template>

<script>
import field from '@/mixins/field'

export default {
  name: 'string',
  mixins: [field],
}
</script>
