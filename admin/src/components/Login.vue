<template>
  <div id="login">
    <div class="row align-center">
      <div class="columns small-12 medium-6 text-left">
        <h2>
          Login
        </h2>
      </div>
    </div>
    <div class="row align-center">
      <div class="columns small-12 medium-6">
        <label for="">Username</label>
        <input type="text" v-model="username">
      </div>
    </div>
    <div class="row align-center">
      <div class="columns small-12 medium-6">
        <label for="">password</label>
        <input type="password" v-model="password">
      </div>
    </div>
    <div class="row align-center">
      <div class="columns small-12 medium-6 text-left">
        <a href="#submit" class="button" @click.prevent="login">Submit</a>
      </div>
    </div>
  </div>
</template>

<script>
import * as R from 'ramda'
import api from '@/lib/api'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Login',
  data() {
    return {
      username: null,
      password: null,
    }
  },
  methods: {
    login() {
      api.postResource('authenticate', {
        username: this.username,
        password: this.password,
      }).then((result) => {
        console.log(result)
        if (result && result.token) {
          localStorage.setItem('username', this.username)
          localStorage.setItem('token', result.token)

          this.$router.push('/')
        }
      })
    }
  }
}
</script>

<style lang="scss">
</style>
