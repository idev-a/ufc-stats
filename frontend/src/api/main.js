import session from './session';

export default {
  getEntries(entries) {
    return session.post('/api/entries/get_entries/', entries);
  },
  getLatestContest() {
  	return session.get('api/entries/get_latestcontest/')
  },
  getLatestEvent () {
  	return session.get('api/events/get_latestevent/')
  },
  getFighters() {
  	return session.get('api/fighters/')
  },
  createEntries(payload) {
  	return session.post('api/entries/', payload)
  }
}