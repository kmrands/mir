import * as R from 'ramda'
import qs from 'query-string'

import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['settings']),
  },
  methods: {
    getCloudUrl(_id, params) {
      const cdnUrl = R.path(['global', 'cdn'], this.settings)
      let baseUrl = process.env.SERVER !== ""
        ? `${process.env.SERVER}/api/images/${_id}`
        : `/api/images/${_id}`

      if (cdnUrl) {
        baseUrl = `${cdnUrl}/${_id}`
      }

      const queryString = params ? qs.stringify(params) : null

      if (queryString) return `${baseUrl}?${queryString}`
      return baseUrl
    },
  },
}
