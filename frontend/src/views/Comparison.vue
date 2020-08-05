<template>
  <ui-container-box :columns="24" vertical align-center class="page-container">
    <ui-container-box :columns="20" horizontal align-center class="page-title">
      <span class="page-title__label">Comparison</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <info></info>
      <notice></notice>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <search-compare1></search-compare1>
      <search-compare2></search-compare2>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <lego-radio v-model="timeCondition" value="1" >HH</lego-radio>
      <lego-radio v-model="timeCondition" value="2" >HHMM</lego-radio>
      <lego-radio v-model="timeCondition" value="3" >HHMMSS</lego-radio>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <button @click="search1Chart">Search1 Test</button>
      <button @click="resetZoom1">resetZoom1</button>

      <button @click="search2Chart">Search2 Test</button>
      <button @click="resetZoom1">resetZoom2</button>
      
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <!-- search1 -->
      <chart-line :chart-data="lChartData1" :options="lOptions" :width="800" :height="400"></chart-line>
      <!-- search2 -->
      <chart-line :chart-data="lChartData2" :options="lOptions" :width="800" :height="400"></chart-line>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <!-- search1 -->
      <chart-stacked-bar :chart-data="sbChartData1" :options="sbOptions" :width="800" :height="400"></chart-stacked-bar>
      <!-- search2 -->
      <chart-stacked-bar :chart-data="sbChartData2" :options="sbOptions" :width="800" :height="400"></chart-stacked-bar>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <!-- search1 -->
      <chart-bar :chart-data="bChartData1" :options="sbOptions" :width="800" :height="400"></chart-bar>
      <!-- search2 -->
      <chart-bar :chart-data="bChartData2" :options="sbOptions" :width="800" :height="400"></chart-bar>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <!-- search1 -->
      <chart-pie :chart-data="pChartData1" :options="sbOptions" :width="800" :height="400"></chart-pie>
      <!-- search2 -->
      <chart-pie :chart-data="pChartData2" :options="sbOptions" :width="800" :height="400"></chart-pie>
    </ui-container-box>


    <ui-container-box :columns="20" horizontal class="page-tab-area">TODO : Footer 영역</ui-container-box>
  </ui-container-box>
</template>

<script>
import ChartLine from "@/components/layout/ChartLine";
import ChartBar from "@/components/layout/ChartBar";
import ChartPie from "@/components/layout/ChartPie";
import ChartStackedBar from "@/components/layout/ChartStackedBar";

import GridTable from "@/components/layout/GridTable";
import Info from "@/components/layout/Info";
import Init from "@/components/layout/Init";
import Notice from "@/components/layout/Notice";
import Search from "@/components/layout/Search";
import SearchCompare1 from "@/components/layout/SearchCompare1";
import SearchCompare2 from "@/components/layout/SearchCompare2";
import Statistics from "@/components/layout/Statistics";

import { serverUrl } from "@/common";

import { getPieChartTemplate, getBarChartTemplate, getStackedBarChartTemplate, getLineChartTemplate, 
        getPieChartOptions, getBarChartOptions, getStackedBarChartOptions, getLineChartOptions,
        getChartDataFromStatistics, getLineChartData } from "@/common"

import * as types from "@/vuex/mutation_types";
import { mapGetters } from "vuex";

export default {
  name: "Compare",

  data(){
    return {
      timeCondition: "2",

      // for chart reactivess Test
      lChartData1: null,
      lChartData2: null,
      lOptions: getLineChartOptions(),

      bChartData1: null,
      bChartData2: null,
      bOptions: getBarChartOptions(),

      sbChartData1: null,
      sbChartData2: null,
      sbOptions: getStackedBarChartOptions(),

      pChartData1: null,
      pChartData2: null,
      pOptions: getPieChartOptions(),

      logfile_id: '',

    }
    
  },

  // 컴포넌트 등록
  components: {
    Info: Info,
    Notice: Notice,
    Search: Search,
    SearchCompare1: SearchCompare1,
    SearchCompare2: SearchCompare2,
    Statistics: Statistics,
    ChartLine: ChartLine,
    ChartBar: ChartBar,
    ChartPie: ChartPie,
    ChartStackedBar: ChartStackedBar
  },
  created() {
    console.log("serverUrl : ", serverUrl);
    this.logfile_id = this.$store.state.logFileID
  },
  computed: {
    ...mapGetters({
      isSearch1: "getToggleSearch1",
      isSearch2: "getToggleSearch2",

      dateFromValue: "getFromDate",
      dateToValue: "getToDate",
      timeFromValue: "getFromTime",
      timeToValue: "getToTime",

      conditionValue: "getCondition",
      searchValue: "getSearchKeyword",

      ttFromValue: "getFromTimeTaken",
      ttToValue: "getToTimeTaken",
    }),
  },
  methods: {
    resetZoom1() {

    },
    getFilter() {
      
      let filter = {
        dateFromValue: this.dateFromValue,
        dateToValue: this.dateToValue,
        timeFromValue: this.timeFromValue,
        timeToValue: this.timeToValue,

        conditionValue: this.conditionValue,
        searchValue: this.searchValue,

        ttFromValue: this.ttFromValue,
        ttToValue: this.ttToValue,
      }
      
      return filter
    },

    search1Chart(){

      console.log("search1Chart")
      this.stackedbarChartData(1)
      this.lineChartData(1)
      this.barChartData(1)
      this.pieChartData(1)
    },

    search2Chart(){
      
      console.log("search2Chart")
      this.stackedbarChartData(2)
      this.lineChartData(2)
      this.barChartData(2)
      this.pieChartData(2)
    },

    async pieChartData (searchArea) { 

      let filter = this.getFilter()
      let res = await getChartDataFromStatistics(1, this.logfile_id, filter)

      if ( searchArea == 1 ){
        this.pChartData1 = getPieChartTemplate(res.x, res.y)
      }else{
        this.pChartData2 = getPieChartTemplate(res.x, res.y)
      }
    },
  
    async barChartData (searchArea) {
      let filter = this.getFilter()
      let res = await getChartDataFromStatistics(1, this.logfile_id, filter)      
      if ( searchArea == 1 ){
        this.bChartData1 = getBarChartTemplate(res.x, res.y, res.label)
      }else{
        this.bChartData2 = getBarChartTemplate(res.x, res.y, res.label)
      }

    },

    async stackedbarChartData (searchArea) {
      let filter = this.getFilter()
      let res = await getLineChartData(2, this.timeCondition, this.logfile_id, filter)
      if ( searchArea == 1 ){
        this.sbChartData1 = getStackedBarChartTemplate(res.sbarX, res.sbarY_200, res.sbarY_300, res.sbarY_400, res.sbarY_500)
      }else{
        this.sbChartData2 = getStackedBarChartTemplate(res.sbarX, res.sbarY_200, res.sbarY_300, res.sbarY_400, res.sbarY_500)
      }
    },

    // 시계열 분석용 Line Chart
    async lineChartData (searchArea) {
      let filter = this.getFilter()
      let res = await getLineChartData(1, this.timeCondition, this.logfile_id, filter)
      if ( searchArea == 1 ){
        this.lChartData1 = getLineChartTemplate(res.x, res.y, "Request")
      }else{
        this.lChartData2 = getLineChartTemplate(res.x, res.y, "Request")
      }
    },
  },

  watch: {
    isSearch1() {
      this.search1Chart()
    },

    isSearch2() {
      this.search2Chart()
    },

  }
};
</script>

<style scoped>
</style>