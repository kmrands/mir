<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <select v-model="scopedData">
      <option v-for="item in choices" :value="item">{{item}}</option>
    </select>
  </div>
</template>

<script>
import field from '@/mixins/field'

export default {
  name: 'dropdown',
  mixins: [field],
}
</script>
