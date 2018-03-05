import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import ItemEditor from '@/components/ItemEditor'
import ItemList from '@/components/ItemList'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
      children: [
        {
          path: '/:type',
          name: 'ItemList',
          component: ItemList,
          children: [
            {
              path: 'create',
              name: 'ItemCreator',
              component: ItemEditor
            },
            {
              path: 'edit/:id',
              name: 'ItemEditor',
              component: ItemEditor
            },
          ]
        },
      ]
    },
  ]
})
