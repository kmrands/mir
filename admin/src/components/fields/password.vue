<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <input type="password" v-model="scopedData">
  </div>
</template>

<script>
import field from '@/mixins/field'

export default {
  name: 'password',
  mixins: [field],
}
</script>
