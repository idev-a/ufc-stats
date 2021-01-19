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
      path: '/pages',
      component: () => import('@/views/pages/Index'),
      children: [
        {
          name: 'Lock',
          path: 'lock',
          component: () => import('@/views/pages/Lock'),
          meta: {
            requiresAuth: false
          }
        },
        {
          name: 'Login',
          path: 'login',
          component: () => import('@/views/pages/Login'),
        },
        {
          name: 'Logout',
          path: 'logout',
          beforeEnter: redirectLogout,
        },
        {
          name: 'Pricing',
          path: 'pricing',
          component: () => import('@/views/pages/Pricing'),
          meta: {
            requiresAuth: false
          }
        },
        {
          name: 'Register',
          path: 'register',
          component: () => import('@/views/pages/Register'),
          meta: {
            requiresAuth: false
          }
        },
      ],
    },
    {
      path: '/',
      component: () => import('@/views/dashboard/Index'),
      children: [
        {
          name: 'Dashboard',
          path: '',
          component: () => import('@/views/dashboard/selection/Selection'),
        },
        {
          name: 'Selection',
          path: 'selection',
          component: () => import('@/views/dashboard/selection/Selection'),
        },
        {
          name: 'Contest',
          path: 'contest',
          component: () => import('@/views/dashboard/contest/ContestContainer'),
          beforeEnter: requireAuthenticated
        },
        {
          name: 'Score',
          path: 'score',
          component: () => import('@/views/dashboard/component/Score'),
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
          component: () => import('@/views/dashboard/pages/Callback'),
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