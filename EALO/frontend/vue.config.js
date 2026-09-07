module.exports = {
  publicPath: '',
  css: {
    loaderOptions: {
      scss: {
        additionalData: `@import "~@/styles/_variables.scss";`
      }
    }
  }
}
