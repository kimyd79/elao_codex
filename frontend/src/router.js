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
import Detail from "./views/Detail.vue"
import Management from "./views/Management.vue"
import Logformat from "./views/Logformat.vue"

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
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
      path: '/comparison',
      name: 'Comparison',
      component: Comparison,
    },
    {
      path: '/management',
      name: 'Management',
      component: Management,
      children: [
        {
          path: '/logformat',
          name: 'logformat',
          component: Logformat
        },
      ]
    },

  ]
})
