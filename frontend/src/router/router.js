import Vue from 'vue';
import Router from 'vue-router';
import UserPage from '../pages/User.vue';
import LoginPage from '../pages/Login.vue';
import AdminPage from '../pages/Admin.vue';
import AdminEdit from '../pages/AdminEdit.vue';
import NotFound from '../pages/NotFound.vue';
import GymRules from '../pages/GymRules.vue';
import AdminPayments from '../pages/Payments.vue';
import FixedProgram from '../pages/Fixed.vue';
import { isAuthenticated, refreshToken, isSuperuser } from '../utils/auth';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  routes: [
    { 
      path: '/userpage', 
      component: UserPage, 
      meta: { requiresAuth: true, requiresUser: true } 
    },
    { 
      path: '/gymrules', 
      component: GymRules, 
      meta: { requiresAuth: true, requiresUser: true } 
    },
    { 
      path: '/adminpage', 
      component: AdminPage, 
      meta: { requiresAuth: true, requiresSuperuser: true } 
    },
    { 
      path: '/adminedit', 
      component: AdminEdit, 
      meta: { requiresAuth: true, requiresSuperuser: true } 
    },
    { 
      path: '/payments', 
      component: AdminPayments, 
      meta: { requiresAuth: true, requiresSuperuser: true } 
    },
    { 
      path: '/fixed', 
      component: FixedProgram, 
      meta: { requiresAuth: true, requiresSuperuser: true } 
    },
    { path: '/login', component: LoginPage },
    { 
      path: '/logout', 
      beforeEnter: (to, from, next) => {
        localStorage.clear();
        next('/login');
      }
    },
    { 
      path: '*', 
      component: NotFound, 
      beforeEnter: (to, from, next) => {
        next('/login');
      }
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated()) {
      try {
        const refreshed = await refreshToken();
        if (!refreshed) {
          return next('/login');
        }
      } catch (error) {
        console.error('Error during authentication check:', error);
        return next('/login');
      }
    }
    
    return checkUserRole(to, next);
  } else {
    return next();
  }
});

function checkUserRole(to, next) {
  const userIsSuperuser = isSuperuser();

  if (to.meta.requiresSuperuser && !userIsSuperuser) {
    return next('/userpage');
  } else if (to.meta.requiresUser && userIsSuperuser) {
    return next('/adminpage');
  } else {
    return next();
  }
}

export default router;