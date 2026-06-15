const express = require('express');
const NotificationService = require('../services/notificationService');

const router = express.Router();

router.get('/', (req, res) => {
  const userId = req.query.user_id || null;
  let limit = parseInt(req.query.limit, 10);
  if (isNaN(limit) || limit < 1) limit = 50;
  if (limit > 100) limit = 100;
  const results = NotificationService.getNotifications(userId, limit);
  res.json(results);
});

router.post('/', async (req, res) => {
  const matchData = req.body;
  const created = await NotificationService.createNotification(matchData);
  res.status(201).json(created);
});

router.get('/unread-count', (req, res) => {
  const userId = req.query.user_id || null;
  res.json({ count: NotificationService.getUnreadCount(userId) });
});

router.patch('/:notification_id/read', (req, res) => {
  const notificationId = parseInt(req.params.notification_id, 10);
  const userId = req.query.user_id || null;
  const success = NotificationService.markAsRead(notificationId, userId);
  if (success) {
    return res.json({ message: 'Marcada como leída' });
  }
  res.json({ message: 'Notificación no encontrada' });
});

module.exports = router;
