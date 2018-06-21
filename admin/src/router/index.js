import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Index from '@/components/Index'
import ItemEditor from '@/components/ItemEditor'
import ItemList from '@/components/ItemList'
import Users from '@/components/Users'
import MediaLibrary from '@/components/MediaLibrary'

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
          path: '',
          component: Users,
        },
        {
          path: '/media',
          component: MediaLibrary,
        },
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

router.afterEach((to, from) => {
  document.body.style.overflow = 'scroll'
})

export default router
