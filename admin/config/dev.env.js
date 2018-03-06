'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  SERVER: '"http://localhost:8080/api/v1"',
  CLOUDINARY_CLOUD_NAME: '"dru5oe8vy"'
})
