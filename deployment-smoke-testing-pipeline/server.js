const http = require('http');

const PORT = 3000;
let appStatus = 'healthy';

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json');

  if (req.url === '/health') {
    res.writeHead(200);
    res.end(JSON.stringify({
      status: 'ok',
      timestamp: new Date().toISOString()
    }));
  } else if (req.url === '/api/data') {
    res.writeHead(200);
    res.end(JSON.stringify({
      message: 'Data endpoint',
      version: '1.0.0'
    }));
  } else if (req.url === '/api/status') {
    res.writeHead(200);
    res.end(JSON.stringify({
      status: appStatus,
      uptime: process.uptime()
    }));
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({
      error: 'Not found'
    }));
  }
});

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
