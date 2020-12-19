import Vue from 'vue'
import Router from 'vue-router'

import store from './store';

const requireAuthenticated = (to, from, next) => {
  store.dispatch('auth/initialize')
    .then(() => {
      if (!store.getters['auth/isAuthenticated']) {
        next('/pages/login');
      } else {
        next();
      }
    });
};

const requireUnauthenticated = (to, from, next) => {
  store.dispatch('auth/initialize')
    .then(() => {
      if (store.getters['auth/isAuthenticated']) {
        next('/');
      } else {
        next();
      }
    });
};

const redirectLogout = (to, from, next) => {
  store.dispatch('auth/logout')
    .then(() => next('/pages/login'));
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
          beforeEnter: requireUnauthenticated
        },
        {
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
          component: () => import('@/views/dashboard/Dashboard'),
        },
        {
          name: 'Selection',
          path: 'selection',
          component: () => import('@/views/dashboard/component/Selection'),
        },
        {
          name: 'Contest',
          path: 'contest',
          component: () => import('@/views/dashboard/component/Contest'),
        },
      ],
    },
    {
      path: '/auth/callback',
      component: {
        template: '<div class="auth-component"></div>'
      }
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

// router.beforeEach((to, from, next) => {
//     if(to.matched.some(record => record.meta.requiresAuth)) {
//         if (localStorage.getItem('jwt') == null || localStorage.getItem('jwt') == 'null') {
//             next({
//                 path: '/pages/login',
//                 params: { nextUrl: to.fullPath }
//             })
//         } else {
//             let user = {}
//             try {
//               user = JSON.parse(localStorage.getItem('user'))
//             } catch (e) {}
//             if(to.matched.some(record => record.meta.is_admin)) {
//                 if(user.role == 'Admin'){
//                     next()
//                 }
//                 else{
//                     next({ name: 'Dashboard'})
//                 }
//             }else {
//                 next()
//             }
//         }
//     } else {
//         next()
//     }
// })


export default router