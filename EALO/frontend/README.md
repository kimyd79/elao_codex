# LogAnalyzer - Leehs

## Supported environment

- Node.js 20.19 or newer (verified with Node.js 24.18)
- npm 11
- Vue 2.7 compatibility bridge on Vue CLI 5 / Webpack 5

The local `lego-component-0.1.2.tgz` package is required. `npm ci` runs a
small, version-specific SCSS syntax patch from `scripts/patch-lego-component.js`
because the package was originally compiled only with legacy `node-sass`.

## Project setup
```
npm ci
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
