<template>
  <div id="app">
      <ui-gnb style="width: 100%; z-index:900;">
          <template v-slot:lead>
              <ui-gnb-title>
                  <template v-slot:title>
                    <router-link to="/analysis">MW LogAnalyzer</router-link>
                  </template>
                  <template v-slot:sub>CI-TEC</template>
              </ui-gnb-title>
              <ui-gnb-menus :menus="menus">
                <template v-slot="{ menu }" >
                  <router-link :to="menu.linkto">{{menu.label}}</router-link>
                </template>
              </ui-gnb-menus>
          </template>
      </ui-gnb>
      
      <router-view style="padding-top: 73px; display:flex; justify-content:center;" />

  </div>
</template>

<script>

import store from './vuex/store'

export default {
  store,
  data() {
    return {
      menus: [
          //{ label:'Component Set', linkto:'/sets', key:'componentset', isSelected: false },
          //{ label:'Template', linkto:'/template', key:'template', isSelected: false },
          // LogAnalyzer
          { label:'Initialization', linkto:'/initialization', key:'initialization', isSelected: false },
          { label:'Analysis', linkto:'/analysis', key:'analysis', isSelected: false },
          { label:'Comparison', linkto:'/comparison', key:'comparison', isSelected: false },
          { label:'Detail', linkto:'/detail', key:'detail', isSelected: false },
          { label:'Setting', linkto:'/setting', key:'setting', isSelected: false }
      ]
    }
  },
  watch: {
    '$route' (to, from) {
      this.menus.forEach(function(menu){
        menu.isSelected = (to.path.includes(menu.linkto));
      })
    }
  }
}
</script>

<style lang="scss">
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  position: relative;
}
#nav {
  padding: 30px;
}

a {
  color: inherit;
  text-decoration: none;
}

em {
  color: inherit;
  text-decoration: none;
  font-style: normal;
}
.m24 {
  margin: 24px;
}
.mt8 {
  margin-top: 8px;
}
.mt12 {
  margin-top: 12px;
}
.mt16 {
  margin-top: 16px;
}
.mt20 {
    margin-top: 20px;
}
.mt24 {
    margin-top: 24px;
}
.mt32 {
  margin-top: 32px;
}
.mt48 {
  margin-top: 48px;
}
.mt50 {
    margin-top: 50px;
}
.mt70 {
    margin-top: 70px;
}
.mb48 {
    margin-bottom: 48px;
}
.mb50 {
    margin-bottom: 50px;
}
.ml20 {
    margin-left: 20px;
}
.ml48 {
    margin-left: 48px;
}
.ml50 {
    margin-left: 50px;
}
.ml80 {
  margin-left: 80px;
}
.bg-white {
    background-color: white;
}
.bg-gray {
  background-color: #eaeaea;
}
.bg-contents {
  background-color: #F7F7F7;
}
.mg-auto {
  margin: auto;
}
.pd16 {
  padding: 16px;
}
.pt8 {
  padding-top: 8px;
}
.pt32 {
  padding-top: 32px;
}
.pt80 {
  padding-top: 80px;
}
.pb80 {
  padding-bottom: 80px !important;
}
.pd80 {
  padding: 80px !important;
}
.mt0 {
  margin-top: 0px;
}

.page-container {
  margin: 48px 0 32px;
  padding: 48px 80px;
  background-color: white;
}
.page-title {
  margin-top: 16px;
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid #cccccc;
}
.page-title__label {
  font-size: 32px;
  font-weight: bold;
}
.page-form-area {
  padding: 16px 0;
  border-bottom: 1px solid #cccccc;
}
.page-summary-area {
  margin-top: 48px;
}
.page-summary-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 24px;
}
.page-summary-table {
  border-spacing: 0;
}
.page-summary-table thead th {
  height: 28px;
  border-top: 1px solid #eaeaea;
  font-weight: normal;
  background-color: #f7f7f7;
}
.page-summary-table thead th + th {
  border-left: 1px solid #eaeaea;
}
.page-summary-table tbody td {
  height: 44px;
  text-align: center;
  border-bottom: 1px solid #eaeaea;
}
.page-summary-table tbody tr:first-child td {
  border-top: 1px solid #a5a5a5;
}
.page-summary-table tbody td + td {
  border-left: 1px solid #eaeaea;
}
.page-tab-area {
  margin-top: 60px;
  border-bottom: 1px solid #cccccc;
}
.page-table-area {
  margin: 32px 0 24px;
}

</style>
