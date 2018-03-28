<template>
  <div id="users">
    <div class="row align-center">
      <div class="columns small-12 medium-8 secondary-menu padding-lg" v-if="!showUserForm">
        <h5>Accounts Dashboard</h5>
        <table>
          <thead v-if="currentCollection && currentCollection._items">
            <tr>
              <th width="200">Username</th>
              <th>Roles</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in currentCollection._items">
              <td>{{user.username}}</td>
              <td>
                <span v-if="user.roles && user.roles.length > 0">
                  {{formatRoles(user.roles)}}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="createUser" v-if="superuser">
          <a href="#createUser" class="button" @click.prevent="createUser">Create User</a>
        </div>
      </div>
      <div class="columns small-12 medium-8 secondary-menu padding-lg" v-if="showUserForm">
        <h5>Create User</h5>
        <div>
          <input type="text" placeholder="your@email.com" v-model="username">
          <input type="password" placeholder="Password" v-model="password">
          <input type="password" placeholder="Confirm Password" v-model="confirmPassword">
        </div>
        <div class="row">
          <div class="columns small-12">
            <h6>Roles</h6>
          </div>
          <div class="columns small-12" v-for="(item, idx) in roles" >
            <div class="row">
              <div class="columns small-11">
                <input type="text" v-model="item.role">
              </div>
              <div class="columns small-1" v-if="roles.length > 1">
                <a href="" @click.prevent="removeRole(idx)">
                  <i class="fas fa-minus-circle"></i>
                </a>
              </div>
            </div>
          </div>
          <div class="columns small-12">
            <a href="#addRole" class="" @click.prevent="addRole">
              Add Role
            </a>
          </div>
        </div>
        <hr>
        <div>
          <a href="#create" class="button" @click.prevent="sendCreateUser">Create</a>
          <a href="#cancel" class="button secondary" @click.prevent="closeUserForm">Cancel</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as R from 'ramda'

import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Users',
  data() {
    return {
      superuser: false,
      showUserForm: false,
      username: null,
      password: null,
      confirmPassword: null,
      roles: [{
        'role': 'user'
      }],
      match: false,
    }
  },
  mounted() {
    this.setState()
  },
  methods: {
    ...mapActions(['getCurrentCollection', 'createItem', 'notify']),
    setState() {
      const roles = R.map(
        item => item.role,
        JSON.parse(localStorage.getItem('roles'))
      )

      if (R.contains('superuser', roles)) {
        this.superuser = true
        this.getCurrentCollection({
          resourceType: 'users',
          params: {
            max_results: 500,
          }
        })
      } else {
        this.getCurrentCollection({
          resourceType: 'accounts',
          params: {
            max_results: 500,
          }
        })
      }
    },
    formatRoles(roles) {
      const roleNames = R.map(item => item.role, roles)
      return roleNames.join(', ')
    },
    createUser() {
      this.showUserForm = true
    },
    sendCreateUser() {
      if ((this.password == this.confirmPassword)) {
        this.createItem({
          resourceType: 'users',
          payload: {
            username: this.username,
            password: this.password,
            roles: this.roles,
          }
        }).then((result) => {
          this.showUserForm = false
          this.notify({
            msg: 'User created successfully!',
            type: 'success',
          })
          this.setState()
        }).catch((error) => {
          this.handleError(error)
        })
      } else {
        this.notify({
          msg: 'Your passwords do not match!',
          type: 'warning',
        })
      }
    },
    closeUserForm() {
      this.showUserForm = false
    },
    addRole() {
      this.roles = R.append({role: null}, this.roles)
    },
    removeRole(idx) {
      this.roles = R.remove(idx, 1, this.roles)
    },
    handleError(error) {
      if (error.response.status === 412) {
        this.notify({
          msg: 'Oops! It looks like someone else has edited this document. Please refresh the page for the latest version.',
          type: 'warning',
        })
      }
      if (error.response.status === 404) {
        this.notify({
          msg: 'Oops! It looks like you are trying to edit a resource that no longer exists.',
          type: 'warning',
        })
        this.$router.push({
          name: 'ItemList',
          params: {type: this.$route.params.type }
        })
      }
      if (error.response.status === 422) {
        this.notify({
          msg: 'Oops! Your updates contain validation errors.',
          type: 'warning',
        })
        if (error.response.data && error.response.data._issues) {
          this.errors = R.keys(error.response.data._issues)
        }
      }
      if (error.response.status === 500) {
        this.notify({
          msg: 'Something went wrong! Please try again in a moment.',
          type: 'warning',
        })
      }
    },
  },
  computed: {
    ...mapGetters(['currentCollection']),
  },
}
</script>

<style lang="scss">
@import '../scss/settings';

svg.svg-inline--fa {
  position: relative;
  top: 10px;
  width: 25px !important;
  height: auto;
}
</style>
