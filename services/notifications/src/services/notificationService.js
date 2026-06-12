const { manager } = require('../websocket/manager');

const notificationsStore = [];

class NotificationService {
  static async createNotification(matchData) {
    function buildNotification(userId, role) {
      return {
        id: notificationsStore.length + 1,
        user_id: userId,
        type: 'match_found',
        title: 'Posible coincidencia encontrada',
        message: `Se detecto una posible coincidencia (${Math.round(matchData.score || 0)}%) para tu reporte ${role}.`,
        match_id: matchData._id || null,
        score: matchData.score || 0,
        report_lost_id: matchData.report_lost_id || null,
        report_found_id: matchData.report_found_id || null,
        pet_lost_name: matchData.pet_lost_name || 'Desconocido',
        pet_found_name: matchData.pet_found_name || 'Desconocido',
        read: false,
        created_at: new Date().toISOString(),
      };
    }

    const created = [];
    const userLostId = String(matchData.user_lost_id || '').trim();
    const userFoundId = String(matchData.user_found_id || '').trim();

    const recipients = [];
    if (userLostId) {
      recipients.push([userLostId, 'perdido']);
    }
    if (userFoundId && userFoundId !== userLostId) {
      recipients.push([userFoundId, 'encontrado']);
    }

    for (const [userId, role] of recipients) {
      const notification = buildNotification(userId, role);
      notificationsStore.push(notification);
      created.push(notification);
      console.log(`Notification created for user ${userId}: ${notification.title}`);
      manager.sendToUser(userId, notification);
    }

    return created;
  }

  static getNotifications(userId = null, limit = 50) {
    let results = notificationsStore;
    if (userId) {
      results = results.filter(n => String(n.user_id) === String(userId));
    }
    results = [...results].sort((a, b) => b.created_at.localeCompare(a.created_at));
    return results.slice(0, limit);
  }

  static markAsRead(notificationId, userId = null) {
    for (const n of notificationsStore) {
      if (n.id === notificationId) {
        if (userId && String(n.user_id) !== String(userId)) {
          return false;
        }
        n.read = true;
        return true;
      }
    }
    return false;
  }

  static getUnreadCount(userId = null) {
    if (userId) {
      return notificationsStore.filter(
        n => !n.read && String(n.user_id) === String(userId)
      ).length;
    }
    return notificationsStore.filter(n => !n.read).length;
  }
}

module.exports = NotificationService;
