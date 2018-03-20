import * as R from 'ramda'

export default {
  methods: {
    validRoute(route) {
      return !R.contains(
        route,
        [
          'accounts',
          'users',
          'media',
          'log',
        ]
      )
    },
  },
}
