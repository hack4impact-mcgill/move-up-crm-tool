export default {
  build: {
    host: process.env.NODE_ENV === "development" ? "http://127.0.0.1" : "",
    port: process.env.NODE_ENV === "development" ? 8080 : 443,
    backendHost:
      process.env.NODE_ENV === "development" ? "http://127.0.0.1" : "",
    backendPort: process.env.NODE_ENV === "development" ? 5000 : 443,
    assetsSubDirectory: "static",
    assetsPublicPath: "/",
    productionSourceMap: true,
    // Gzip off by default as many popular static hosts such as
    // Surge or Netlify already gzip all static assets for you.
    // Before setting to `true`, make sure to:
    // npm install --save-dev compression-webpack-plugin
    productionGzip: false,
    productionGzipExtensions: ["js", "css"]
  },
  dev: {
    host: "127.0.0.1",
    port: 8080,
    backendHost: "127.0.0.1",
    backendPort: 5000,
    autoOpenBrowser: true,
    assetsSubDirectory: "static",
    assetsPublicPath: "/",
    proxyTable: {},
    // CSS Sourcemaps off by default because relative paths are "buggy"
    // with this option, according to the CSS-Loader README
    // (https://github.com/webpack/css-loader#sourcemaps)
    // In our experience, they generally work as expected,
    // just be aware of this issue when enabling this option.
    cssSourceMap: false
  }
};
