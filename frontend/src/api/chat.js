import session from './session';

export default {
  fetchRooms(user_id, startIdx=0) {
    return session.get(`/api/chat/rooms/get_all?user_id=${user_id}&idx=${startIdx}`)
  },
  addRoom(room) {
    return session.post('api/chat/rooms/', room)
  },
  updateRoom(roomId, data) {
    return session.patch(`api/chat/rooms/${roomId}/`, data)
  },
  addMessage(message) {
    return session.post('/api/chat/messages/', message);
  },
  updateMessage(data) {
    return session.patch(`/api/chat/messages/${data.id}/`, data);
  },
  fetchMessages(roomId, startIdx=0) {
    return session.get(`/api/chat/messages/get_all?room_id=${roomId}&idx=${startIdx}`)
  },
  fetchMessage(roomId) {
    return session.get(`/api/chat/messages/get_by_room?room_id=${roomId}`)
  },
}