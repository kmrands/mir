import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Index from '@/components/Index'
import ItemEditor from '@/components/ItemEditor'
import ItemList from '@/components/ItemList'

import api from '@/lib/api'

Vue.use(Router)

const auth = (to, from, next) => {
  api.getResource('accounts').then((result) => {
    next()
  }, (error) => {
    next('/login')
  })
}

const router = new Router({
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/',
      name: 'Index',
      component: Index,
      beforeEnter: auth,
      children: [
        {
          path: '/:type',
          name: 'ItemList',
          beforeEnter: auth,
          component: ItemList,
          children: [
            {
              path: 'create',
              name: 'ItemCreator',
              beforeEnter: auth,
              component: ItemEditor
            },
            {
              path: 'edit/:id',
              name: 'ItemEditor',
              beforeEnter: auth,
              component: ItemEditor
            },
          ]
        },
      ]
    },
  ]
})

export default router
