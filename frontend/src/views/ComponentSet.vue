<template>
  <div class="bg-gray">
      <ui-gnb style="position: fixed; width: 100%; z-index:999;">
          <template v-slot:lead>
              <ui-gnb-menus :menus="menus">
                <template v-slot="{ menu }" >
                  <router-link :to="menu.linkto">{{menu.label}}</router-link>
                </template>
              </ui-gnb-menus>
          </template>
      </ui-gnb>
      
      <router-view class="pt80 pb80"/>

  </div>
</template>

<script>
export default {
    data() {
        return {
            menus: [
                { label:'Accordion', linkto:'/sets/accordion', key:'accordion', isSelected: false },
                { label:'Card', linkto:'/sets/card', key:'card', isSelected: false },
                { label:'Form', linkto:'/sets/form', key:'form', isSelected: false },
                { label:'GNB', linkto:'/sets/gnb', key:'gnb', isSelected: false },
                { label:'List', linkto:'/sets/list', key:'list', isSelected: false },
                { label:'LNB', linkto:'/sets/lnb', key:'lnb', isSelected: false },
                { label:'Step', linkto:'/sets/step', key:'step', isSelected: false },
                { label:'Tab', linkto:'/sets/tab', key:'tab', isSelected: false },
                { label:'Title', linkto:'/sets/title', key:'title', isSelected: false },
                { label:'Tree', linkto:'/sets/tree', key:'tree', isSelected: false },
                { label:'View Page', linkto:'/sets/viewpage', key:'viewpage', isSelected: false },
                { label:'Table', linkto:'/sets/table', key:'table', isSelected: false },
            ]
        }
    },
    watch: {
      '$route' (to, from) {
        this.menus.forEach(function(menu){
          menu.isSelected = (menu.linkto === to.path);
        })
      }
    }
}
</script>