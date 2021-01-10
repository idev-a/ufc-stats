import session from './session';

export default {
  twitterRequestToken() {
    return session.get('/auth/twitter/request_token/');
  },
  twitterCallback(url) {
    return session.get(url);
  },
  login(username, password) {
    return session.post('/auth/login/', { username, password });
  },
  logout() {
    return session.post('/auth/logout/', {});
  },
  createAccount(payload) {
    return session.post('/auth/registration/', payload);
  },
  changeAccountPassword(password1, password2) {
    return session.post('/auth/password/change/', { password1, password2 });
  },
  sendAccountPasswordResetEmail(email) {
    return session.post('/auth/password/reset/', { email });
  },
  resetAccountPassword(uid, token, new_password1, new_password2) { // eslint-disable-line camelcase
    return session.post('/auth/password/reset/confirm/', { uid, token, new_password1, new_password2 });
  },
  getAccountDetails() {
    return session.get('/auth/user/');
  },
  checkAlreadyTaken(user_id) {
    return session.get(`/api/check_user_already_taken?user_id=${user_id}`);
  },
  updateAccount(data) {
    return session.patch('/auth/user/', data);
  },
  verifyAccountEmail(key) {
    return session.post('/registration/verify-email/', { key });
  },
};
