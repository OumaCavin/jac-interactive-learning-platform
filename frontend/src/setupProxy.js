const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // Get API URL from environment variable or use default
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  
  // Proxy API requests to backend
  app.use(
    '/api',
    createProxyMiddleware({
      target: apiUrl,
      changeOrigin: true,
      pathRewrite: {
        '^/api': '/api', // keep /api in the path
      },
      onError: (err, req, res) => {
        console.error('Proxy error:', err);
        res.status(500).json({ error: 'Proxy error', details: err.message });
      },
      onProxyReq: (proxyReq, req, res) => {
        console.log(`[Proxy] ${req.method} ${req.url} -> ${apiUrl}${req.url}`);
      },
    })
  );

  // Proxy WebSocket connections
  app.use(
    '/ws',
    createProxyMiddleware({
      target: apiUrl.replace('http', 'ws'),
      changeOrigin: true,
      ws: true,
      pathRewrite: {
        '^/ws': '/ws', // keep /ws in the path
      },
      onError: (err, req, res) => {
        console.error('WebSocket proxy error:', err);
      },
      onProxyReq: (proxyReq, req, res) => {
        console.log(`[WebSocket Proxy] ${req.method} ${req.url} -> ${apiUrl.replace('http', 'ws')}${req.url}`);
      },
    })
  );
};