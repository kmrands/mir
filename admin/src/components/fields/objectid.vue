<template>
  <div>
    <label for="">{{label}}</label>
    <div class="help">{{help}}</div>
  </div>
</template>

<script>
import field from '@/mixins/field'

export default {
  name: 'objectid',
  mixins: [field],
}
</script>
