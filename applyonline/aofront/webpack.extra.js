var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  output: {
        filename: "[name].js",
        publicPath: 'http://localhost:8000/static/aofront/',
    },
  plugins: [
    new BundleTracker({filename: '../../webpack-stats.json'})
  ]
}
