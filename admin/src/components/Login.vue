<template>
  <div id="login" class="padding-lg" v-if="loaded">
    <div class="row align-center" v-if="!redirect">
      <div class="columns small-12 medium-6 text-left">
        <h2>
          Login
        </h2>
        <p class="error" v-if="error">Login failed! Please provide proper credentials.</p>
      </div>
    </div>
    <div v-if="!redirect">
      <div class="row align-center">
        <div class="columns small-12 medium-6">
          <label for="">Username</label>
          <input type="text" v-model="username">
        </div>
      </div>
      <div class="row align-center">
        <div class="columns small-12 medium-6">
          <label for="">Password</label>
          <input type="password" v-model="password">
        </div>
      </div>
      <div class="row align-center">
        <div class="columns small-12 medium-6 text-left">
          <a href="#submit" class="button" @click.prevent="login">Submit</a>
        </div>
      </div>
    </div>
    <div v-if="redirect">
      <div class="row align-center padding-md">
        <div class="columns small-12 medium-6 text-center">
          <a :href="redirect" class="button large">Dashboard Login</a>
        </div>
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
      loaded: false,
      redirect: null,
      error: false,
      username: null,
      password: null,
    }
  },
  beforeMount() {
    if (window.token) {
      this.redirect = window.redirect
      localStorage.setItem('token', window.token)
      this.$router.push('/')
    } else {
      if (window.redirect) {
        window.location = window.redirect
      }
    }
    this.loaded = true
  },
  methods: {
    login() {
      api.postResource('authenticate', {
        username: this.username,
        password: this.password,
      }).then((result) => {
        if (result && result.token) {
          localStorage.setItem('username', this.username)
          localStorage.setItem('roles', JSON.stringify(result.roles))
          localStorage.setItem('token', result.token)

          this.$router.push('/')
        }
      }).catch((error) => {
        this.error = true
      })
    }
  }
}
</script>

<style lang="scss">
  @import '../scss/main.scss';
  .error {
    color: $warning-color;
  }
</style>
