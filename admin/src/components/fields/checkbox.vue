<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <div>
      <input type="checkbox" v-model="scopedData"> {{label}}
    </div>
  </div>
</template>

<script>
import field from '@/mixins/field'

export default {
  name: 'checkbox',
  mixins: [field],
}
</script>
