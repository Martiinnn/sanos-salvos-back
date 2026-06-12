const express = require('express');
const cors = require('cors');
const http = require('http');
const { WebSocketServer } = require('ws');
const { URL } = require('url');
const dotenv = require('dotenv');

dotenv.config();

const { manager } = require('./websocket/manager');
const notificationsRouter = require('./routes/notifications');

const app = express();
app.use(cors());
app.use(express.json());

app.get('/health', (_req, res) => {
  res.json({ status: 'healthy', service: 'notifications-service' });
});

app.use('/api/notifications', notificationsRouter);

const PORT = process.env.PORT || 8004;

const server = http.createServer(app);

const wss = new WebSocketServer({ noServer: true });

server.on('upgrade', (request, socket, head) => {
  const pathname = new URL(request.url, `http://${request.headers.host}`).pathname;

  if (pathname.startsWith('/api/notifications/ws')) {
    wss.handleUpgrade(request, socket, head, (ws) => {
      const parts = pathname.split('/');
      const wsIndex = parts.indexOf('ws');
      const userId = parts[wsIndex + 1] || null;

      manager.connect(ws, userId);

      ws.on('message', (data) => {
        const msg = data.toString();
        if (msg === 'ping') {
          ws.send('pong');
        }
      });

      ws.on('close', () => {
        manager.disconnect(ws, userId);
      });
    });
  } else {
    socket.destroy();
  }
});

server.listen(PORT, () => {
  console.log(`Notifications service running on port ${PORT}`);
});
