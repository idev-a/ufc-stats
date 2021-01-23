<template>
  <div>
    <chat-window
      theme="dark"
      height="calc(100vh - 80px)"
      :styles="styles"
      :current-user-id="currentUserId"
      :rooms="loadedRooms"
      :loading-rooms="false"
      :messages="messages"
      :messages-loaded="messagesLoaded"
      :rooms-loaded="true"
      :menu-actions="menuActions"
      text-formatting
      :room-message="roomMessage"
      @fetch-more-rooms="fetchMoreRooms"
      @fetch-messages="fetchMessages"
      @send-message="sendMessage"
      @edit-message="editMessage"
      @delete-message="deleteMessage"
      @open-file="openFile"
      @add-room="addRoom"
      @menu-action-handler="menuActionHandler"
      @message-action-handler="messageActionHandler"
      @send-message-reaction="sendMessageReaction"
      @typing-message="typingMessage"
      :show-files="false"
      :show-audio="false"
      :show-add-room="false"
    >
    </chat-window>
  </div>
</template>
<script>
import  { mapState, mapActions } from 'vuex'
import ChatWindow from 'vue-advanced-chat'
import 'vue-advanced-chat/dist/vue-advanced-chat.css'
import chatAPI from "@/api/chat"
import authAPI from "@/api/auth"
import { parseTimestamp, isSameDay } from '@/util'

export default {
  name: 'app',
    
  components: {
    ChatWindow
  },

  data() {
    return {
      roomsPerPage: 15,
      startRooms: 0,
      endRooms: 0,
      roomsLoaded: false,
      loadingRooms: true,
      allUsers: [],
      loadingLastMessageByRoom: 0,
      roomsLoadedCount: false,
      selectedRoom: null,
      messagesPerPage: 20,
      messages: [],
      rooms: [],
      messagesLoaded: false,
      roomMessage: '',
      startMessages: 0,
      endMessages: null,
      roomsListeners: [],
      listeners: [],
      typingMessageCache: '',
      disableForm: false,
      addNewRoom: null,
      addRoomUsername: '',
      inviteRoomId: null,
      invitedUsername: '',
      removeRoomId: null,
      removeUserId: '',
      removeUsers: [],
      menuActions: [],
      styles: { container: { borderRadius: '4px' } }
    }
  },

  mounted() {
    this.fetchRooms()
    // this.updateUserOnlineStatus()

    this.$options.sockets.onmessage = ({data}) => this.watchMessage(data)
  },
  destroyed() {
    this.resetRooms()

    delete this.$options.sockets.onmessage
  },

  computed: {
    ...mapState('auth', ['authUser']),
    currentUserId () {
      return this.authUser.pk || this.authUser.id
    },
    loadedRooms() {
      return this.rooms.slice(0, this.roomsLoadedCount)
    }
  },

  methods: {
    resetRooms() {
      this.loadingRooms = true
      this.loadingLastMessageByRoom = 0
      this.roomsLoadedCount = 0
      this.rooms = []
      this.roomsLoaded = true
      this.startRooms = 0
      this.endRooms = 0
      this.roomsListeners.forEach(listener => listener())
      this.roomsListeners = []
      this.resetMessages()
    },
    resetMessages() {
      this.messages = []
      this.messagesLoaded = false
      this.startMessages = 0
      this.endMessages = 0
      this.listeners.forEach(listener => listener())
      this.listeners = []
    },
    fetchRooms() {
      this.resetRooms()
      this.fetchMoreRooms()
    },
    watchMessage (data) {
      const json_data = JSON.parse(data)
      if (json_data['messages'][0].room != this._room.id) return

      this.listenMessages(json_data['messages'], this._room)
      if (json_data.commands == 'new_message') {
      } else if (json_data.commands == 'delete_message' || json_data.commands == 'edit_message') {

      }
    },
    async fetchMoreRooms() {
      if (this.endRooms && !this.startRooms) return (this.roomsLoaded = true)
      const { data: { rooms } } = await chatAPI.fetchRooms(this.currentUserId, this.startRooms)
      this.roomsLoaded = rooms.empty || rooms.size < this.roomsPerPage
      if (this.startRooms) this.endRooms = this.startRooms
      this.startRooms = rooms[rooms.length - 1]?.id || 0
      const roomUserIds = []
      rooms.forEach(room => {
        room.users.forEach(userId => {
          const foundUser = this.allUsers.find(user => user._id === userId)
          if (!foundUser && roomUserIds.indexOf(userId) === -1) {
            roomUserIds.push(userId)
          }
        })
      })
      // this.incrementDbCounter('Fetch Room Users', roomUserIds.length)
      const { data: { users } } = await authAPI.fetchUsers(roomUserIds)
      this.allUsers = [...this.allUsers, ...users]
      const roomList = {}
      rooms.forEach(room => {
        roomList[room.id] = { ...room, users: [] }
        room.users.forEach(userId => {
          const foundUser = this.allUsers.find(user => user._id === userId)
          if (foundUser) roomList[room.id].users.push(foundUser)
        })
      })
      const formattedRooms = []
      Object.keys(roomList).forEach(key => {
        const room = roomList[key]
        const roomContacts = room.users.filter(
          user => user._id !== this.currentUserId
        )
        // room.roomName = roomContacts.map(user => user.username).join(', ') || 'Me'
        room.roomName = 'UFC Group'
        // const roomAvatar =
        //   roomContacts.length === 1 && roomContacts[0].avatar
        //     ? roomContacts[0].avatar
        //     : require('@/assets/logo.png')
        const roomAvatar = require('@/assets/ufc.png')
        formattedRooms.push({
          ...{
            roomId: key,
            avatar: roomAvatar,
            ...room
          }
        })
      })
      this.rooms = this.rooms.concat(formattedRooms)
      formattedRooms.map(room => this.listenLastMessage(room))
      if (!this.rooms.length) {
        this.loadingRooms = false
        this.roomsLoadedCount = 0
      }
      // this.listenUsersOnlineStatus(formattedRooms)
      // this.listenRoomsTypingUsers(query)
      // setTimeout(() => console.log('TOTAL', this.dbRequestCount), 2000)
    },
    openFile({ message, action }) {
      window.open(message.file.url, '_blank')
    },
    async listenLastMessage(room) {
      const { data: {messages} } = await chatAPI.fetchMessages(room.roomId, -1)
      let _messages = messages.reverse()
      _messages.forEach(message => {
        const lastMessage = this.formatLastMessage(message)
        const roomIndex = this.rooms.findIndex(
          r => room.roomId === r.roomId
        )
        this.rooms[roomIndex].lastMessage = lastMessage
        this.rooms = [...this.rooms]
      })
      if (this.loadingLastMessageByRoom < this.rooms.length) {
        this.loadingLastMessageByRoom++
        if (this.loadingLastMessageByRoom === this.rooms.length) {
          this.loadingRooms = false
          this.roomsLoadedCount = this.rooms.length
        }
      }
      // this.roomsListeners.push(listener)
    },
    formatLastMessage(message) {
      if (!message.timestamp) return
      const date = new Date(message.timestamp)
      const timestampFormat = isSameDay(date, new Date()) ? 'HH:mm' : 'DD/MM/YY'
      let timestamp = parseTimestamp(message.timestamp, timestampFormat)
      if (timestampFormat === 'HH:mm') timestamp = `Today, ${timestamp}`
      let content = message.content
      if (message.file)
        content = `${message.file.name}.${message.file.extension ||
          message.file.type}`
      return {
        ...message,
        ...{
          content,
          timestamp,
          date: message.timestamp,
          seen: message.sender_id === this.currentUserId ? message.seen : null,
          new:
            message.sender_id !== this.currentUserId &&
            (!message.seen)
        }
      }
    },
    listenMessages(messages, room) {
      messages.forEach(message => {
        const formattedMessage = this.formatMessage(room, message)
        const messageIndex = this.messages.findIndex(m => m._id === message.id)
        if (messageIndex === -1) {
          this.messages = this.messages.concat([formattedMessage])
        } else {
          this.$set(this.messages, messageIndex, formattedMessage)
        }
        this.markMessagesSeen(room, message)
      })
    },
    async markMessagesSeen(room, message) {
      if (
        message.sender !== this.currentUserId &&
        (!message.seen || !message.seen)
      ) {
        message.seen = this.$moment().format('YYYY-MM-DD HH:mm:ss')
        const res = await chatAPI.updateMessage(message)
      }
    },
    formatMessage(room, message) {
      const senderUser = room.users.find(
        user => message.sender_id === user._id
      )
      const { sender_id, timestamp } = message
      return {
        ...message,
        ...{
          sender_id,
          _id: message.id,
          seconds: this.$moment(timestamp).format('ss'),
          timestamp: parseTimestamp(timestamp, 'HH:mm'),
          date: parseTimestamp(timestamp, 'DD MMMM YYYY'),
          username: senderUser ? senderUser.displayname : null,
          distributed: true
        }
      }
    },
    async fetchMessages({ room, options = {} }) {
      console.log('------------------ ', this.startMessages)
      this._room = room
      if (options.reset) this.resetMessages()
      if (this.endMessages && !this.startMessages)
        return (this.messagesLoaded = true)

      this.selectedRoom = room.roomId

      const { data: { messages } } = await chatAPI.fetchMessages(room.roomId, this.startMessages)
      if (this.selectedRoom !== room.roomId) return
      if (messages.empty) this.messagesLoaded = true
      if (this.startMessages) this.endMessages = this.startMessages
      this.startMessages = messages[messages.length - 1]?.id || 0

      // let listenerQuery = ref.orderBy('timestamp')
      // if (this.startMessages)
      //   listenerQuery = listenerQuery.startAfter(this.startMessages)
      // if (this.endMessages)
      //   listenerQuery = listenerQuery.endAt(this.endMessages)

      if (options.reset) this.messages = []
      messages.forEach(message => {
        const formattedMessage = this.formatMessage(room, message)
        this.messages.unshift(formattedMessage)
      })

      // subs
    },
    async sendMessage({ content, roomId, file, replyMessage }) {
      const message = {
        room: roomId,
        sender: this.currentUserId,
        content,
        timestamp: this.$moment().format('YYYY-MM-DD HH:mm:ss')
      }
      if (file) {
        message.file = {
          name: file.name,
          size: file.size,
          type: file.type,
          extension: file.extension,
          url: file.localUrl
        }
        if (file.audio) {
          message.file.audio = true
          message.file.duration = file.duration
        }
      }
      if (replyMessage) {
        message.replyMessage = {
          _id: replyMessage._id,
          content: replyMessage.content,
          sender_id: replyMessage.sender_id
        }
        if (replyMessage.file) {
          message.replyMessage.file = replyMessage.file
        }
      }
      // const { id } = await chatAPI.addMessage(message)
      this.$socket.sendObj({commands: 'new_message', data: message})
      // if (file) this.uploadFile({ file, messageId: id, roomId })
      const res = await chatAPI.updateRoom(roomId, { last_updated: new Date() })
    },
    async editMessage({ messageId, newContent, roomId, file }) {
      const newMessage = { 
        id: messageId,
        room: roomId,
        sender: this.currentUserId,
        edited: this.$moment().format('YYYY-MM-DD HH:mm:ss'),
        content: newContent
      }
      if (file) {
        newMessage.file = {
          name: file.name,
          size: file.size,
          type: file.type,
          extension: file.extension,
          url: file.url || file.localUrl
        }
        if (file.audio) {
          newMessage.file.audio = true
          newMessage.file.duration = file.duration
        }
      } else {
        newMessage.file = null
      }
      this.$socket.sendObj({commands: 'edit_message', data: newMessage })
      if (file) this.uploadFile({ file, messageId, roomId })
    },
    async deleteMessage({ messageId, roomId }) {
      const message = { 
        id: messageId,
        room: roomId,
        sender: this.currentUserId,
        deleted: this.$moment().format('YYYY-MM-DD HH:mm:ss') 
      }
      this.$socket.sendObj({commands: 'delete_message', data: message })
    },
    async uploadFile({ file, messageId, roomId }) {
    },
    menuActionHandler({ action, roomId }) {
      switch (action.name) {
        case 'inviteUser':
          return this.inviteUser(roomId)
        case 'removeUser':
          return this.removeUser(roomId)
        case 'deleteRoom':
          return this.deleteRoom(roomId)
      }
    },
    messageActionHandler() {
      // do something
    },
    textareaActionHandler({ message, roomId }) {
      this.roomMessage = 'Implement your own action!'
    },
    async sendMessageReaction({ reaction, remove, messageId, roomId }) {
      const dbAction = remove
        ? firebase.firestore.FieldValue.arrayRemove(this.currentUserId)
        : firebase.firestore.FieldValue.arrayUnion(this.currentUserId)
      await messagesRef(roomId)
        .doc(messageId)
        .update({
          [`reactions.${reaction.name}`]: dbAction
        })
    },
    typingMessage({ message, roomId }) {
      if (message?.length > 1) {
        return (this.typingMessageCache = message)
      }
      if (message?.length === 1 && this.typingMessageCache) {
        return (this.typingMessageCache = message)
      }
      this.typingMessageCache = message
      return
      const dbAction = message
        ? firebase.firestore.FieldValue.arrayUnion(this.currentUserId)
        : firebase.firestore.FieldValue.arrayRemove(this.currentUserId)
      roomsRef.doc(roomId).update({
        typingUsers: dbAction
      })
    },
    async listenRoomsTypingUsers(query) {
      const listener = query.onSnapshot(rooms => {
        // this.incrementDbCounter('Listen Rooms Typing Users', rooms.size)
        rooms.forEach(room => {
          const foundRoom = this.rooms.find(r => r.roomId === room.id)
          if (foundRoom) foundRoom.typingUsers = room.typingUsers
        })
      })
      this.roomsListeners.push(listener)
    },
    updateUserOnlineStatus() {
      const userStatusRef = firebase
        .database()
        .ref('/status/' + this.currentUserId)
      const isOfflineData = {
        state: 'offline',
        last_changed: firebase.database.ServerValue.TIMESTAMP
      }
      const isOnlineData = {
        state: 'online',
        last_changed: firebase.database.ServerValue.TIMESTAMP
      }
      firebase
        .database()
        .ref('.info/connected')
        .on('value', snapshot => {
          if (snapshot.val() == false) return
          userStatusRef
            .onDisconnect()
            .set(isOfflineData)
            .then(() => {
              userStatusRef.set(isOnlineData)
            })
        })
    },
    listenUsersOnlineStatus(rooms) {
      rooms.map(room => {
        room.users.map(user => {
          const listener = firebase
            .database()
            .ref('/status/' + user._id)
            .on('value', snapshot => {
              if (!snapshot || !snapshot.val()) return
              const timestampFormat = isSameDay(
                new Date(snapshot.val().last_changed),
                new Date()
              )
                ? 'HH:mm'
                : 'DD MMMM, HH:mm'
              const timestamp = parseTimestamp(
                new Date(snapshot.val().last_changed),
                timestampFormat
              )
              const last_changed =
                timestampFormat === 'HH:mm' ? `today, ${timestamp}` : timestamp
              user.status = { ...snapshot.val(), last_changed }
              const roomIndex = this.rooms.findIndex(
                r => room.roomId === r.roomId
              )
              this.$set(this.rooms, roomIndex, room)
            })
          this.roomsListeners.push(listener)
        })
      })
    },
    addRoom() {
      this.resetForms()
      this.addNewRoom = true
    },
    async createRoom() {
      this.disableForm = true
      const { id } = await usersRef.add({ username: this.addRoomUsername })
      await usersRef.doc(id).update({ _id: id })
      await roomsRef.add({
        users: [id, this.currentUserId],
        lastUpdated: new Date()
      })
      this.addNewRoom = false
      this.addRoomUsername = ''
      this.fetchRooms()
    },
    inviteUser(roomId) {
      this.resetForms()
      this.inviteRoomId = roomId
    },
    async addRoomUser() {
      this.disableForm = true
      const { id } = await usersRef.add({ username: this.invitedUsername })
      await usersRef.doc(id).update({ _id: id })
      await roomsRef
        .doc(this.inviteRoomId)
        .update({ users: firebase.firestore.FieldValue.arrayUnion(id) })
      this.inviteRoomId = null
      this.invitedUsername = ''
      this.fetchRooms()
    },
    removeUser(roomId) {
      this.resetForms()
      this.removeRoomId = roomId
      this.removeUsers = this.rooms.find(room => room.roomId === roomId).users
    },
    async deleteRoomUser() {
      this.disableForm = true
      await roomsRef.doc(this.removeRoomId).update({
        users: firebase.firestore.FieldValue.arrayRemove(this.removeUserId)
      })
      this.removeRoomId = null
      this.removeUserId = ''
      this.fetchRooms()
    },
    async deleteRoom(roomId) {
      const room = this.rooms.find(r => r.roomId === roomId)
      if (
        room.users.find(user => user._id === 'SGmFnBZB4xxMv9V4CVlW') ||
        room.users.find(user => user._id === '6jMsIXUrBHBj7o2cRlau')
      ) {
        return alert('Nope, for demo purposes you cannot delete this room')
      }
      const ref = messagesRef(roomId)
      ref.get().then(res => {
        if (res.empty) return
        res.docs.map(doc => ref.doc(doc.id).delete())
      })
      await roomsRef.doc(roomId).delete()
      this.fetchRooms()
    },
    resetForms () {

    }
  }
}
</script>

<style scoped>
  .ellipsis {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
</style>