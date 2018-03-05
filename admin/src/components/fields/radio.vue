<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
    <div v-for="choice in choices">
      <input type="radio" :id="choice" :value="choice" v-model="scopedData"> {{choice}}
    </div>
  </div>
</template>

<script>
import field from '@/mixins/field'

export default {
  name: 'radio',
  mixins: [field],
}
</script>
