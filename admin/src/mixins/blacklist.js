import * as R from 'ramda'

export default {
  methods: {
    validRoute(route) {
      return !R.contains(
        route,
        [
          'accounts',
          'configuration',
          'users',
          'media',
          'sitemedia',
          'log',
        ]
      )
    },
  },
}
