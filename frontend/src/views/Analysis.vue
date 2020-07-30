<template>

  <ui-container-box :columns="24" vertical align-center class="page-container">

    <ui-container-box :columns="20" horizontal align-center class="page-title">
      <span class="page-title__label">Analysis</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <info></info>
      <notice></notice>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">
      <search></search>
    </ui-container-box>

    <ui-container-box :columns="20" vertical align-left class="page-title">
      <span class="page-title__label">Statistics - Top</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">    
      
      <ui-container-box :columns="10" vertical class="mt20">
        <statistics-top :statisticsRow="1" :statisticsKind="1"></statistics-top>
        <statistics-top :statisticsRow="1" :statisticsKind="2"></statistics-top>
     </ui-container-box>

     <ui-container-box :columns="10" vertical class="mt20">
        <statistics-top :statisticsRow="1" :statisticsKind="3"></statistics-top>
        <statistics-top :statisticsRow="1" :statisticsKind="4"></statistics-top>
      </ui-container-box>
      
    </ui-container-box>

    <ui-container-box :columns="20" vertical align-left class="page-title">
      <span class="page-title__label">Statistics - Top5</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">    
      
      <ui-container-box :columns="10" vertical class="mt20">
        <statistics-top :statisticsRow="5" :statisticsKind="1"></statistics-top>
        <statistics-top :statisticsRow="5" :statisticsKind="2"></statistics-top>
     </ui-container-box>
           
      <ui-container-box :columns="10" vertical class="mt20">
        <statistics-top :statisticsRow="5" :statisticsKind="3"></statistics-top>
        <statistics-top :statisticsRow="5" :statisticsKind="4"></statistics-top>
      </ui-container-box>
      
    </ui-container-box>

    <ui-container-box :columns="20" vertical align-left class="page-title">
      <span class="page-title__label">Charts</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">
          
      <ui-container-box :columns="10" vertical class="mt20">
        <chart-line :chart-data="lChartData" :options="lOptions"></chart-line>
        <lego-radio v-model="timeCondition" value="1" >HH</lego-radio>
        <lego-radio v-model="timeCondition" value="2" >HHMM</lego-radio>
        <button @click="resetZoom">resetZoom Test</button>
        <!-- TODO : 선택버튼*Dropdown 추가, 같이 그릴까? Time-taken은 없는 경우도 있다. -->
        <!-- 
          Type1 : 시(HH)기준
             Kind1 : request(요청) 건수(count)
             Kind2 : time-taken 시간(max, min, count)
          Type2 : 시분(HHMM)기준                    
             Kind1 : request(요청) 건수(count)
             Kind2 : time-taken 시간(max, min, count)
        -->  
        <button @click="lineChartData">Get Data(Line)</button>                
        <!--// Top 5 일때
          // type=1. Status Codes Top5
          // type=2. Requests Top5
          // type=3. 최다 404 발생 URL Top5
          // type=4. Time Taken Top5 
        -->
        <!-- <chart-line :chart-data="chartdata" :options="options"></chart-line>-->
        <chart-bar :chart-data="bChartData" :options="bOptions"></chart-bar>
        <button @click="barChartData">Get Data(Bar)</button>
      </ui-container-box>      

      <ui-container-box :columns="10" vertical class="mt20">
        <chart-stacked-bar :chart-data="sbChartData" :options="sbOptions"></chart-stacked-bar>
        <button @click="stackedbarChartData">Get Data(StackedBar)</button>
        <chart-pie :chart-data="pChartData" :options="pOptions"></chart-pie>
        <button @click="pieChartData">Get Data(Pie)</button>
      </ui-container-box>

    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-tab-area">
      TODO : Footer 영역
    </ui-container-box>

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
import Statistics from "@/components/layout/Statistics";
import StatisticsTop from "@/components/layout/StatisticsTop";

import { mapGetters } from "vuex";

import { getPieChartTemplate, getBarChartTemplate, getStackedBarChartTemplate, getLineChartTemplate, 
        getPieChartOptions, getBarChartOptions, getStackedBarChartOptions, getLineChartOptions,
        getChartDataFromStatistics, getLineChartData, getSearchFilter } from "@/common"

export default {
  name: "Analysis",

  data(){
    return {
      // For Chart
      // chartdata : [],
      // options : [],

      timeCondition: "1",

      // For Statistics -> use 'props'
      statisticsRow: "1",   // Top or Top5 (Row 수)
      statisticsKind: "1",  // 전체 처리량 (통계 종류)  

      // for chart reactivess Test
      lChartData: null,
      lOptions: getLineChartOptions(),

      bChartData: null,
      bOptions: getBarChartOptions(),

      sbChartData: null,
      sbOptions: getStackedBarChartOptions(),

      pChartData: null,
      pOptions: getPieChartOptions(),

      logfile_id: '',
    }
  }, 

  // 컴포넌트 등록
  components: {
    Info: Info,
    Notice: Notice,
    Search: Search,
    Statistics: Statistics,
    StatisticsTop: StatisticsTop,
    ChartLine: ChartLine,
    ChartBar: ChartBar,
    ChartPie: ChartPie,
    ChartStackedBar: ChartStackedBar
  },

  created() {
    this.logfile_id = this.$store.state.logFileID
  },

  mounted () {

  },

  computed: mapGetters({
      
      dateFromValue: "getFromDate",
      dateToValue: "getToDate",
      timeFromValue: "getFromTime",
      timeToValue: "getToTime",

      conditionValue: "getCondition",
      searchValue: "getSearchKeyword",

      ttFromValue: "getFromTimeTaken",
      ttToValue: "getToTimeTaken",

    }),

  methods: {    
    resetZoom() {

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

    async pieChartData () { 
      let filter = this.getFilter()
      let res = await getChartDataFromStatistics(1, this.logfile_id, filter)
      this.pChartData = getPieChartTemplate(res.x, res.y)
      
    },
  
    async barChartData () {
      let filter = this.getFilter()
      let res = await getChartDataFromStatistics(1, this.logfile_id, filter)      
      this.bChartData = getBarChartTemplate(res.x, res.y, res.label)

    },

    async stackedbarChartData () {
      let filter = this.getFilter()
      let res = await getLineChartData(2, this.timeCondition, this.logfile_id, filter)      
      this.sbChartData = getStackedBarChartTemplate(res.sbarX, res.sbarY_200, res.sbarY_300, res.sbarY_400, res.sbarY_500)
    },

    // 시계열 분석용 Line Chart
    async lineChartData () {
      let filter = this.getFilter()
      let res = await getLineChartData(1, this.timeCondition, this.logfile_id, filter)
      this.lChartData = getLineChartTemplate(res.x, res.y, "Request")      
    },
    
  }
};
</script>

<style scoped>
</style>