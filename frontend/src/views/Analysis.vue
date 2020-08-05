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
        <statistics-top :statisticsRow="5" :statisticsKind="3"></statistics-top>
     </ui-container-box>
           
      <ui-container-box :columns="10" vertical class="mt20">
        <statistics-top :statisticsRow="5" :statisticsKind="3"></statistics-top>
        <statistics-top :statisticsRow="5" :statisticsKind="4"></statistics-top>
        <statistics-top :statisticsRow="5" :statisticsKind="5"></statistics-top>
      </ui-container-box>
      
    </ui-container-box>

    <ui-container-box :columns="20" vertical align-left class="page-title">
      <span class="page-title__label">Charts</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">
          
      <ui-container-box :columns="10" vertical class="mt20">
        <chart-line id="test" ref='zoom' :chart-data="lChartData" :options="lOptions" ></chart-line>        
        <lego-radio v-model="timeCondition" value="1" >HH</lego-radio>
        <lego-radio v-model="timeCondition" value="2" >HHMM</lego-radio>
        <lego-radio v-model="timeCondition" value="3" >HHMMSS</lego-radio>
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
        <chart-bar :chart-data="bChartData" :options="bOptions" ></chart-bar>
        <button @click="barChartData">Get Data(Bar)</button>
        <chart-pie :chart-data="pChartDataVisitorTop5" :options="pOptions"></chart-pie>
        <button @click="pieChartData(5)">Get Data Visitor5(Pie)</button>
      </ui-container-box>      

      <ui-container-box :columns="10" vertical class="mt20">
        <chart-line :chart-data="mlChartData" :options="mlOptions" ></chart-line>
        <button @click="multilineChartData">Get Data(Line)</button>
        <chart-stacked-bar :chart-data="sbChartData" :options="sbOptions"></chart-stacked-bar>
        <button @click="stackedbarChartData">Get Data(StackedBar)</button>
        <chart-pie :chart-data="pChartData" :options="pOptions"></chart-pie>
        <button @click="pieChartData(1)">Get Data(Pie)</button>        
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
        getPieChartOptions, getBarChartOptions, getStackedBarChartOptions, getLineChartOptions, getMultiLineChartTemplate, getMultiLineChartOptions,
        getChartDataFromStatistics, getLineChartData, getSearchFilter } from "@/common"

// Import Loading Spinner component, stylesheet
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

export default {
  name: "Analysis",

  data(){
    return {
      // For Chart
      // chartdata : [],
      // options : [],

      timeCondition: "2",

      // For Statistics -> use 'props'
      statisticsRow: "1",   // Top or Top5 (Row 수)
      statisticsKind: "1",  // 전체 처리량 (통계 종류)  

      // for chart reactivess Test
      lChartData: null,
      lOptions: getLineChartOptions(),

      mlChartData: null,
      mlOptions: getMultiLineChartOptions(),

      bChartData: null,
      bOptions: getBarChartOptions(),

      sbChartData: null,
      sbOptions: getStackedBarChartOptions(),

      pChartData: null,
      pChartDataVisitorTop5: null,
      pOptions: getPieChartOptions(),

      logfile_id: '',
      
      
      // Loading Spinner data
      isLoadingLine: false,
      isLoadingMultiLine: false,
      isLoadingBar: false,
      isLoadingStackedBar: false,
      isLoadingPie: false,
      isLoadingPie5: false,
      fullPage: true,
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
    ChartStackedBar: ChartStackedBar,
    // export Loading Spinner components
    Loading: Loading,
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
      //alert('Test : ')
      //console.log(window.line-chart.resetZoom())
      //console.log(document.getElementById('line-chart'))  // canvas
      
      // Sample Code : TODO: 구조가 다르다.
      // window.resetZoom = function() {
      //   window.myLine.resetZoom();
      // };
          
      // var ctx = document.getElementById('canvas').getContext('2d');
      // window.myLine = new window.Chart(ctx, config)

      //console.log(window)      
      console.log(this.$refs.zoom) //.resetZoom();
      console.log(this.$refs.zoom.Test)
      console.log(document.getElementById('test'))
      console.log(document.getElementById('test').resetZoom)

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

    async pieChartData (type=1) { 
      // Start Loading Spinner
      if ( type == 1 ){        
        this.isLoadingPie = true
      } else if ( type == 5 ){
        this.isLoadingPie5 = true
      }
      
      let filter = this.getFilter()
      let res = await getChartDataFromStatistics(type, this.logfile_id, filter)

      if ( type == 1 ){
        this.pChartData = getPieChartTemplate(res.x, res.y)
        //Stop Loading Spinner
        this.isLoadingPie = false
      } else if ( type == 5 ){
        this.pChartDataVisitorTop5 = getPieChartTemplate(res.x, res.y)
        //Stop Loading Spinner
        this.isLoadingPie5 = false
      }
      
    },    
  
    async barChartData () {
      // Start Loading Spinner
      this.isLoadingBar = true
      
      let filter = this.getFilter()
      let res = await getChartDataFromStatistics(1, this.logfile_id, filter)      
      this.bChartData = getBarChartTemplate(res.x, res.y, res.label)
      
      //Stop Loading Spinner
      this.isLoadingBar = false

    },

    async stackedbarChartData () {
      // Start Loading Spinner
      this.isLoadingStackedBar = true
      
      let filter = this.getFilter()
      let res = await getLineChartData(2, this.timeCondition, this.logfile_id, filter)      
      this.sbChartData = getStackedBarChartTemplate(res.sbarX, res.sbarY_200, res.sbarY_300, res.sbarY_400, res.sbarY_500)
      
      //Stop Loading Spinner
      this.isLoadingStackedBar = false
      
    },

    // 시계열 분석용 Line Chart
    async lineChartData () {
      // Start Loading Spinner
      this.isLoadingLine = true
      
      let filter = this.getFilter()
      let res = await getLineChartData(1, this.timeCondition, this.logfile_id, filter)
      this.lChartData = getLineChartTemplate(res.x, res.y, "Request")   
      
      //Stop Loading Spinner
      this.isLoadingLine = false 

    },

    // 시계열 분석용 Line Chart
    async multilineChartData () {
      // Start Loading Spinner
      this.isLoadingMultiLine = true
      
      let filter = this.getFilter()
      let res = await getLineChartData(3, this.timeCondition, this.logfile_id, filter)
      this.mlChartData = getMultiLineChartTemplate(res.x, res.y, "Request", res.yt, "Time-Taken")    
      
      //Stop Loading Spinner
      this.isLoadingMultiLine = false 
    },
    
  }
};
</script>

<style scoped>
</style>
