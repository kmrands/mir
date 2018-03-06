import * as R from 'ramda'
import cloudinary from 'cloudinary-core'

const cl = cloudinary.Cloudinary.new({ cloud_name: process.env.CLOUDINARY_CLOUD_NAME })

export default {
  methods: {
    getCloudUrl(url, params) {
      return cl.url(R.last(R.split('/', url)), params)
    },
  },
}
