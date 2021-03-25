import session from './session';

export default {
  getEntries(entries) {
    return session.post('/api/entries/get_entries/', entries);
  },
  getLatestContest(game_id=-1) {
  	return session.post('api/entries/get_latestcontest/', {game_id})
  },
  getLatestEvent (game_id=-1, entry_number=0) {
  	return session.post('api/events/get_latestevent/', {game_id, entry_number})
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
  getContestHistoryDetail(event_id, game_id) {
    return session.post('api/entries/get_contest_history_detail/', {event_id, game_id})
  },
  getFaqs() {
    return session.get('api/faqs/')
  },
  submitTicket(form) {
    return session.post('api/faqs/submit_ticket/', form)
  },
  getMyTeams(option=30) {
    return session.post('api/entries/get_my_teams/', {option})
  }
}