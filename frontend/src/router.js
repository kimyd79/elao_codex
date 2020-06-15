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

import LNBStack01 from './views/templates/LNBStack/LNBStack01.vue'
import LNBStack02 from './views/templates/LNBStack/LNBStack02.vue'
import LNBStack03 from './views/templates/LNBStack/LNBStack03.vue'
import LNBStack04 from './views/templates/LNBStack/LNBStack04.vue'
import LNBStack05 from './views/templates/LNBStack/LNBStack05.vue'
import LNBStack06 from './views/templates/LNBStack/LNBStack06.vue'
import LNBStack07 from './views/templates/LNBStack/LNBStack07.vue'
import LNBStack08 from './views/templates/LNBStack/LNBStack08.vue'
import LNBStack09 from './views/templates/LNBStack/LNBStack09.vue'
import LNBStack10 from './views/templates/LNBStack/LNBStack10.vue'
import LNBStack11 from './views/templates/LNBStack/LNBStack11.vue'

import LNBSplit01 from './views/templates/LNBSplit/LNBSplit01.vue'
import LNBSplit02 from './views/templates/LNBSplit/LNBSplit02.vue'
import LNBSplit03 from './views/templates/LNBSplit/LNBSplit03.vue'
import LNBSplit04 from './views/templates/LNBSplit/LNBSplit04.vue'

import LNBComplex01 from './views/templates/LNBComplex/LNBComplex01.vue'
import LNBComplex02 from './views/templates/LNBComplex/LNBComplex02.vue'
import LNBComplex03 from './views/templates/LNBComplex/LNBComplex03.vue'
import LNBComplex04 from './views/templates/LNBComplex/LNBComplex04.vue'

import Stack01 from './views/templates/Stack/Stack01.vue'
import Stack02 from './views/templates/Stack/Stack02.vue'
import Stack03 from './views/templates/Stack/Stack03.vue'
import Stack04 from './views/templates/Stack/Stack04.vue'
import Stack05 from './views/templates/Stack/Stack05.vue'
import Stack06 from './views/templates/Stack/Stack06.vue'
import Stack07 from './views/templates/Stack/Stack07.vue'

import Split01 from './views/templates/Split/Split01.vue'
import Split02 from './views/templates/Split/Split02.vue'
import Split03 from './views/templates/Split/Split03.vue'
import Split04 from './views/templates/Split/Split04.vue'

import Complex01 from './views/templates/Complex/Complex01.vue'
import Complex02 from './views/templates/Complex/Complex02.vue'
import Complex03 from './views/templates/Complex/Complex03.vue'

import PopupXL from './views/templates/Popup/PopupXL.vue'
import PopupL from './views/templates/Popup/PopupL.vue'
import PopupM from './views/templates/Popup/PopupM.vue'
import PopupS from './views/templates/Popup/PopupS.vue'


// LogAnalyzer
import Analysis from "./views/Analysis.vue"
import Compare from "./views/Compare.vue"
import Detail from "./views/Detail.vue"

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
      path: '/compare',
      name: 'compare',
      component: Compare,
    },


    {
      path: '/template',
      name: 'template',
      component: Template,
      children: [
        {
          path: 'LNBStack01',
          name: 'LNBStack01',
          component: LNBStack01
        },
        {
          path: 'LNBStack02',
          name: 'LNBStack02',
          component: LNBStack02
        },
        {
          path: 'LNBStack03',
          name: 'LNBStack03',
          component: LNBStack03
        },
        {
          path: 'LNBStack04',
          name: 'LNBStack04',
          component: LNBStack04
        },
        {
          path: 'LNBStack05',
          name: 'LNBStack05',
          component: LNBStack05
        },
        {
          path: 'LNBStack06',
          name: 'LNBStack06',
          component: LNBStack06
        },
        {
          path: 'LNBStack07',
          name: 'LNBStack07',
          component: LNBStack07
        },
        {
          path: 'LNBStack08',
          name: 'LNBStack08',
          component: LNBStack08
        },
        {
          path: 'LNBStack09',
          name: 'LNBStack09',
          component: LNBStack09
        },
        {
          path: 'LNBStack10',
          name: 'LNBStack10',
          component: LNBStack10
        },
        {
          path: 'LNBStack11',
          name: 'LNBStack11',
          component: LNBStack11
        },
        {
          path: 'LNBSplit01',
          name: 'LNBSplit01',
          component: LNBSplit01
        },
        {
          path: 'LNBSplit02',
          name: 'LNBSplit02',
          component: LNBSplit02
        },
        {
          path: 'LNBSplit03',
          name: 'LNBSplit03',
          component: LNBSplit03
        },
        {
          path: 'LNBSplit04',
          name: 'LNBSplit04',
          component: LNBSplit04
        },
        {
          path: 'LNBComplex01',
          name: 'LNBComplex01',
          component: LNBComplex01
        },
        {
          path: 'LNBComplex02',
          name: 'LNBComplex02',
          component: LNBComplex02
        },
        {
          path: 'LNBComplex03',
          name: 'LNBComplex03',
          component: LNBComplex03
        },
        {
          path: 'LNBComplex04',
          name: 'LNBComplex04',
          component: LNBComplex04
        },
        {
          path: 'Stack01',
          name: 'Stack01',
          component: Stack01
        },
        {
          path: 'Stack02',
          name: 'Stack02',
          component: Stack02
        },
        {
          path: 'Stack03',
          name: 'Stack03',
          component: Stack03
        },
        {
          path: 'Stack04',
          name: 'Stack04',
          component: Stack04
        },
        {
          path: 'Stack05',
          name: 'Stack05',
          component: Stack05
        },
        {
          path: 'Stack06',
          name: 'Stack06',
          component: Stack06
        },
        {
          path: 'Stack07',
          name: 'Stack07',
          component: Stack07
        },
        {
          path: 'Split01',
          name: 'Split01',
          component: Split01
        },
        {
          path: 'Split02',
          name: 'Split02',
          component: Split02
        },
        {
          path: 'Split03',
          name: 'Split03',
          component: Split03
        },
        {
          path: 'Split04',
          name: 'Split04',
          component: Split04
        },
        {
          path: 'Complex01',
          name: 'Complex01',
          component: Complex01
        },
        {
          path: 'Complex02',
          name: 'Complex02',
          component: Complex02
        },
        {
          path: 'Complex03',
          name: 'Complex03',
          component: Complex03
        },
        {
          path: 'PopupXL',
          name: 'PopupXL',
          component: PopupXL
        },
        {
          path: 'PopupL',
          name: 'PopupL',
          component: PopupL
        },
        {
          path: 'PopupM',
          name: 'PopupM',
          component: PopupM
        },
        {
          path: 'PopupS',
          name: 'PopupS',
          component: PopupS
        }
      ]
    },
    {
      path: '/sets',
      name: 'componentset',
      component: ComponentSet,
      children: [
        {
          path: 'accordion',
          name: 'accordion',
          component: Accordion
        },
        {
          path: 'card',
          name: 'card',
          component: Card
        },
        {
          path: 'form',
          name: 'form',
          component: Form
        },
        {
          path: 'gnb',
          name: 'gnb',
          component: GNB
        },
        {
          path: 'list',
          name: 'list',
          component: List
        },
        {
          path: 'lnb',
          name: 'lnb',
          component: LNB
        },
        {
          path: 'step',
          name: 'step',
          component: Step
        },
        {
          path: 'tab',
          name: 'tab',
          component: Tab
        },
        {
          path: 'title',
          name: 'title',
          component: Title
        },
        {
          path: 'tree',
          name: 'tree',
          component: Tree
        },
        {
          path: 'viewpage',
          name: 'viewpage',
          component: ViewPage
        },
        {
          path: 'table',
          name: 'table',
          component: Table
        }
      ]
    },
  ]
})
