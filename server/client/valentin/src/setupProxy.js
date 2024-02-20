const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use('/iot', createProxyMiddleware({
    target: 'https://dhbwapi.maytastix.de',
    changeOrigin: true,
  }));
};