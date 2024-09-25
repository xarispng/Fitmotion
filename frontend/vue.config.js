const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],
  // Configure public path for production
  publicPath: process.env.NODE_ENV === 'production' ? '/' : '/',
  devServer: {
    // Use your Render backend URL in development mode
    proxy: process.env.VUE_APP_API_URL || 'http://localhost:8000'
  }
});