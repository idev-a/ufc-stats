import Vue from 'vue'
import Router from 'vue-router'

import store from '@/store';

const requireAuthenticated = (to, from, next) => {
  const self = Object.assign({}, store)
  store.dispatch('auth/initialize')
    .then(() => {
      if (!self.getters['auth/isAuthenticated']) {
        if (from != to) { 
          next('/')
          self.commit('auth/showLoginDlg')
        }
      } else {
        next();
      }
    });
};

const requireUnauthenticated = (to, from, next) => {
  const self = Object.assign({}, store)
  store.dispatch('auth/initialize')
    .then(() => {
      if (self.getters['auth/isAuthenticated']) {
        next('/');
      } else {
        next();
      }
    });
};

const redirectLogout = (to, from, next) => {
  const self = Object.assign({}, store)
  store.dispatch('auth/logout')
    .then(() => self.commit('auth/showLoginDlg'));
};

Vue.use(Router)

let router = new Router({
  mode: 'history',
  saveScrollPosition: true,
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: () => import('@/views/dashboard/Index'),
      children: [
        {
          name: 'Selection',
          path: '',
          component: () => import('@/views/dashboard/selection/SelectionContainer'),
        },
        {
          name: 'Game',
          path: '/game/:type',
          component: () => import('@/views/dashboard/selection/SelectionContainer'),
        },
        {
          name: 'Contest',
          path: 'contest/:game_id?',
          component: () => import('@/views/dashboard/contest/ContestContainer'),
          beforeEnter: requireAuthenticated
        },
        {
          name: 'Leaderboard',
          path: 'leaderboard',
          component: () => import('@/views/dashboard/leaderboard/LeaderboardContainer'),
          beforeEnter: requireAuthenticated
        },
        {
          name: 'Referral',
          path: 'rf/:id',
          component: () => import('@/views/dashboard/referral/ReferralCallback'),
        },
        {
          name: 'Lobby',
          path: 'lobby',
          component: () => import('@/views/dashboard/lobby/LobbyContainer'),
          beforeEnter: requireAuthenticated
        },
        {
          name: 'Old Contests',
          path: 'history/contest',
          component: () => import('@/views/dashboard/history/ContestHistoryContainer'),
          beforeEnter: requireAuthenticated
        },
        {
          name: 'MyContestDetail',
          path: 'history/contest/:event_id/:game_id',
          component: () => import('@/views/dashboard/history/ContestHistoryDetailContainer'),
          beforeEnter: requireAuthenticated
        },
      ],
    },
    {
      path: '/twitter/callback',
      component: () => import('@/views/dashboard/layout/Layout'),
      children: [
        {
          path: '',
          component: () => import('@/views/dashboard/pages/TwitterCallback'),
        }
      ]
    },
    {
      path: '*',
      component: () => import('@/views/pages/Index'),
      children: [
        {
          name: '404 Error',
          path: '',
          component: () => import('@/views/pages/Error'),
          meta: {
            requiresAuth: false
          }
        },
      ],
    },
  ],
})

export default router