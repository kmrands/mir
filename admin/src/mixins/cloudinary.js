import * as R from 'ramda'
import cloudinary from 'cloudinary-core'

// const cl = cloudinary.Cloudinary.new({ cloud_name: process.env.CLOUDINARY_CLOUD_NAME })

export default {
  methods: {
    getCloudUrl(_id, params) {
      return process.env.SERVER !== "" ? `${process.env.SERVER}/api/images/${_id}` : `/api/images/${_id}`
      // return cl.url(R.last(R.split('/', url)), params)
    },
  },
}
