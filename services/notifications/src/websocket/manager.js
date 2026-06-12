const WebSocket = require('ws');

class ConnectionManager {
  constructor() {
    this.activeConnections = {};
    this.broadcastConnections = [];
  }

  connect(ws, userId = null) {
    if (userId) {
      if (!this.activeConnections[userId]) {
        this.activeConnections[userId] = [];
      }
      this.activeConnections[userId].push(ws);
      console.log(`🔌 User ${userId} connected via WebSocket`);
    } else {
      this.broadcastConnections.push(ws);
      console.log('🔌 Broadcast listener connected');
    }
  }

  disconnect(ws, userId = null) {
    if (userId && this.activeConnections[userId]) {
      this.activeConnections[userId] = this.activeConnections[userId].filter(c => c !== ws);
      if (this.activeConnections[userId].length === 0) {
        delete this.activeConnections[userId];
      }
      console.log(`🔌 User ${userId} disconnected`);
    } else {
      this.broadcastConnections = this.broadcastConnections.filter(c => c !== ws);
    }
  }

  sendToUser(userId, message) {
    if (!this.activeConnections[userId]) return;
    const data = JSON.stringify(message);
    const disconnected = [];
    for (const ws of this.activeConnections[userId]) {
      try {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(data);
        } else {
          disconnected.push(ws);
        }
      } catch (_) {
        disconnected.push(ws);
      }
    }
    for (const ws of disconnected) {
      this.disconnect(ws, userId);
    }
  }

  broadcast(message) {
    const data = JSON.stringify(message);
    const disconnected = [];
    for (const ws of this.broadcastConnections) {
      try {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(data);
        } else {
          disconnected.push(ws);
        }
      } catch (_) {
        disconnected.push(ws);
      }
    }
    for (const ws of disconnected) {
      this.broadcastConnections = this.broadcastConnections.filter(c => c !== ws);
    }

    for (const [userId, connections] of Object.entries(this.activeConnections)) {
      for (const ws of connections) {
        try {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(data);
          }
        } catch (_) {}
      }
    }
  }

  getConnectedUsers() {
    return Object.keys(this.activeConnections);
  }
}

const manager = new ConnectionManager();

module.exports = { manager, ConnectionManager };
