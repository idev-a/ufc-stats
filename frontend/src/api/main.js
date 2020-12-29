import session from './session';

export default {
  getEntries(entries) {
    return session.post('/api/entries/get_entries/', entries);
  },
  getLatestContests() {
  	return session.get('api/entries/contest')
  }
}