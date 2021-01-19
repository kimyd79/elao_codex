import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

import ComponentSet from './views/ComponentSet.vue'
import Accordion from './views/sets/Accordion.vue'
import Card from './views/sets/Card.vue'
import Form from './views/sets/Form.vue'
import GNB from './views/sets/GNB.vue'
import List from './views/sets/List.vue'
import LNB from './views/sets/LNB.vue'
import Step from './views/sets/Step.vue'
import Tab from './views/sets/Tab.vue'
import Title from './views/sets/Title.vue'
import Tree from './views/sets/Tree.vue'
import ViewPage from  './views/sets/ViewPage.vue'
import Table from './views/sets/Table.vue'
import Template from './views/Template.vue'


// LogAnalyzer
import Init from "./views/Init.vue"
import Analysis from "./views/Analysis.vue"
import Comparison from "./views/Comparison.vue"
import ComparisonStatistic from "./views/ComparisonStatistic.vue"
import Detail from "./views/Detail.vue"
import Management from "./views/Management.vue"
import Logformat from "./views/Logformat.vue"
import Register from "./components/layout/Register.vue"
import LogIn from "./components/layout/LogIn.vue"
import LogOut from "./components/layout/LogOut.vue"
import Project from "./views/Project.vue"
import Metrics from "./views/Metrics.vue"
import store from "@/vuex/store";
import VueSimpleAlert from "vue-simple-alert";

Vue.use(Router)


const requireAdmin = () => (to, from, next) => {
  if(store.state.userName.toLowerCase() == 'leehs' || store.state.userName.toLowerCase() == 'admin') {
    next();
  } else {
    VueSimpleAlert.alert("Allow only admin to access.", "Notification", "error");
  }
};

const checkLoggedin = () => (to, from, next) => {
  if(store.state.userName == 'Not logged in') {
    next();
  } else {
    VueSimpleAlert.alert("You are already logged in.", "Notification", "error");
  }
};

const router = new Router({
  
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },

    // LogAnalyzer
    {
      path: '/initialization',
      name: 'initialization',
      component: Init,
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: Analysis,
    },
    {
      path: '/detail',
      name: 'detail',
      component: Detail,
    },
    {
      path: '/comparison_chart',
      name: 'comparison_chart',
      component: Comparison,
    },
    {
      path: '/comparison_statistic',
      name: 'comparison_statistic',
      component: ComparisonStatistic,
    },
    {
      path: '/management',
      name: 'Management',
      component: Management,
      children: [
        {
          path: '/logformat',
          name: 'logformat',
          component: Logformat,
        },
                {
          path: '/register',
          name: 'register',
          component: Register,
          beforeEnter: requireAdmin(),
        },
        {
          path: '/login',
          name: 'login',
          component: LogIn,
          beforeEnter: checkLoggedin(),
        },
        {
          path: '/logout',
          name: 'logout',
          component: LogOut,
        },
        {
          path: '/project',
          name: 'project',
          component: Project,
          beforeEnter: requireAdmin(),
        },
        {
          path: '/metrics',
          name: 'metrics',
          component: Metrics,
          // beforeEnter: requireAdmin(),
        },
      ]
    },    
    
  ]
});

router.beforeEach((to, from, next) => {
  if(to.path == '/login' || to.path == '/register') return next();
  if(store.state.userName == 'Not logged in') {
    next('/login');
  } else {
    next();
  }
});

export default router;