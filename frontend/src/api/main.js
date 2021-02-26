import session from './session';

export default {
  getEntries(entries) {
    return session.post('/api/entries/get_entries/', entries);
  },
  getLatestContest(game_id=-1) {
  	return session.post('api/entries/get_latestcontest/', {game_id})
  },
  getLatestEvent (game_id=-1) {
  	return session.post('api/events/get_latestevent/', {game_id})
  },
  getFighters() {
  	return session.get('api/fighters/')
  },
  createEntries(payload) {
  	return session.post('api/entries/', payload)
  },
  getLeaderboard () {
    return session.get('api/entries/get_leaderboard/')
  },
  loadGames() {
    return session.get('api/games/load_games/')
  },
  joinGame(payload) {
    return session.post('api/games/join_game/', payload)
  },
  getMyContestHistory () {
    return session.post('api/entries/get_contest_history/')
  },
  getContestHistoryDetail(entry_id) {
    return session.post('api/entries/get_contest_history_detail/', {entry_id})
  }
}