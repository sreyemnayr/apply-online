var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  plugins: [
    new BundleTracker({filename: '../webpack-stats.json'})
  ]
}
