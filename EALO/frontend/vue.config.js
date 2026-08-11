module.exports = {
  publicPath: '',
  css: {
    loaderOptions: {
      scss: {
        prependData: `@import "~@/styles/_variables.scss";`
      }
    }
  }
}