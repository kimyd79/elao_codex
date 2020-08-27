<template>
  <ui-container-box :columns="22" vertical align-center class="page-container">
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

    <ui-container-box :columns="20" vertical align-left class="page-form-area">
      
      <span class="page-title__label">Charts</span>

      <ui-form-row>
        <ui-form-item :columns="12" label="Timeline" align-left required-left >
          <lego-radio v-model="timeCondition" value="1" >HH</lego-radio>
          <lego-radio v-model="timeCondition" value="2" >HHMM</lego-radio>
          <lego-radio v-model="timeCondition" value="3" >HHMMSS</lego-radio>
        </ui-form-item>
      </ui-form-row>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      
        <ui-form-item :columns="10" label="Select" align-left required-left >       
          <lego-button @click="lineChartData(1)" main small >Line</lego-button>                
          <lego-button @click="multilineChartData(1)" main small>MultiLine</lego-button>
          <lego-button @click="barChartData(1)" main small>Bar</lego-button>
          <lego-button @click="stackedbarChartData(1)" main small>StackedBar</lego-button>
          <lego-button @click="pieChartData(1)" main small >Pie</lego-button>        
          <lego-button @click="search1Chart" small>Search-1 ALL</lego-button>
        </ui-form-item>

        <ui-form-item :columns="10" label="Select" align-left required-left >       
          <lego-button @click="lineChartData(2)" main small >Line</lego-button>                
          <lego-button @click="multilineChartData(2)" main small>MultiLine</lego-button>
          <lego-button @click="barChartData(2)" main small>Bar</lego-button>
          <lego-button @click="stackedbarChartData(2)" main small>StackedBar</lego-button>
          <lego-button @click="pieChartData(2)" main small >Pie</lego-button>        
          <lego-button @click="search2Chart" small>Search-2 ALL</lego-button>
        </ui-form-item>                
      

    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <!-- search1 -->
      <div class="vld-parent">
        <vue-element-loading :active="isActiveLine1" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5"/>
        <lego-button @click="resetZoom(1)" small >resetZoom</lego-button>
        <chart-line ref="lChart1" :chart-data="lChartData1" :options="lOptions" :width="800" :height="400"></chart-line>
      </div>
      <!-- search2 -->
      <div class="vld-parent">
        <vue-element-loading :active="isActiveLine2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5"/>
        <lego-button @click="resetZoom(4)" small >resetZoom</lego-button>
        <chart-line ref="lChart2" :chart-data="lChartData2" :options="lOptions" :width="800" :height="400"></chart-line>
      </div>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <!-- search1 -->
      <div class="vld-parent">
        <vue-element-loading :active="isActiveMultiLine1" spinner="spinner" text="Loading.." :is-full-screen="false" 
        color="#553ca5"/>
        <lego-button @click="resetZoom(2)" small >resetZoom</lego-button>
        <chart-line ref="mlChart1" :chart-data="mlChartData1" :options="mlOptions" :width="800" :height="400"></chart-line>
      </div>
      <!-- search2 -->
      <div class="vld-parent">
        <vue-element-loading :active="isActiveMultiLine2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5"/>
        <lego-button @click="resetZoom(5)" small >resetZoom</lego-button>
        <chart-line ref="mlChart2" :chart-data="mlChartData2" :options="mlOptions" :width="800" :height="400"></chart-line>
      </div>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <!-- search1 -->
      <div class="vld-parent">
        <vue-element-loading :active="isActiveStackedBar1" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5"/>
        <lego-button @click="resetZoom(3)" small >resetZoom</lego-button>
        <chart-stacked-bar ref="sbChart1" :chart-data="sbChartData1" :options="sbOptions" :width="800" :height="400"></chart-stacked-bar>
      </div>
      <!-- search2 -->
      <div class="vld-parent">
        <vue-element-loading :active="isActiveStackedBar2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5"/>
        <lego-button @click="resetZoom(6)" small >resetZoom</lego-button>
        <chart-stacked-bar ref="sbChart2" :chart-data="sbChartData2" :options="sbOptions" :width="800" :height="400"></chart-stacked-bar>
      </div>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <!-- search1 -->
      <div class="vld-parent">
        <vue-element-loading :active="isActiveBar1" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5"/>
        <chart-bar :chart-data="bChartData1" :options="bOptions" :width="800" :height="400"></chart-bar>
      </div>
      <!-- search2 -->
      <div class="vld-parent">
        <vue-element-loading :active="isActiveBar2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5"/>
        <chart-bar :chart-data="bChartData2" :options="bOptions" :width="800" :height="400"></chart-bar>
      </div>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <!-- search1 -->
      <div class="vld-parent">
        <vue-element-loading :active="isActivePie1" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5"/>
        <chart-pie :chart-data="pChartData1" :options="sbOptions" :width="800" :height="400"></chart-pie>
      </div>
      <!-- search2 -->
      <div class="vld-parent">
        <vue-element-loading :active="isActivePie2" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5"/>
        <chart-pie :chart-data="pChartData2" :options="sbOptions" :width="800" :height="400"></chart-pie>
      </div>
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

import { getPieChartTemplate, getBarChartTemplate, getStackedBarChartTemplate, getLineChartTemplate, getMultiLineChartTemplate, getMultiLineChartOptions,
        getPieChartOptions, getBarChartOptions, getStackedBarChartOptions, getLineChartOptions,
        getChartDataFromStatistics, getLineChartData } from "@/common"

import * as types from "@/vuex/mutation_types";
import { mapGetters } from "vuex";

import VueElementLoading from 'vue-element-loading'

export default {
  name: "Compare",

  // 컴포넌트 등록
  components: {
    Info,
    Notice,
    Search,
    SearchCompare1,
    SearchCompare2,
    Statistics,
    ChartLine,
    ChartBar,
    ChartPie,
    ChartStackedBar,
    VueElementLoading
  },
  data(){
    return {
      timeCondition: "2",

      // for chart reactivess Test
      lChartData1: null,
      lChartData2: null,
      lOptions: getLineChartOptions(),

      mlChartData1: null,
      mlChartData2: null,
      mlOptions: getMultiLineChartOptions(),

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
      project_id: '',

      // For Loading Spinner
      isActiveLine1: false,
      isActiveMultiLine1: false,
      isActiveBar1: false,
      isActiveStackedBar1: false,
      isActivePie1: false,
     
      isActiveLine2: false,
      isActiveMultiLine2: false,
      isActiveBar2: false,
      isActiveStackedBar2: false,
      isActivePie2: false,


    }
    
  },

  
  created() {
    console.log("serverUrl : ", serverUrl);
    this.logfile_id = this.$store.state.logFileID
    this.project_id = this.$store.state.projectID
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
    resetZoom(chart) {
      var comp;

      if ( chart == 1){
        comp = this.$refs.lChart1;
      } else if ( chart == 2){
        comp = this.$refs.mlChart1;
      } else if ( chart == 3){
        comp = this.$refs.sbChart1;
      } else if ( chart == 4){
        comp = this.$refs.lChart2;
      } else if ( chart == 5){
        comp = this.$refs.mlChart2;
      } else if ( chart == 6){
        comp = this.$refs.sbChart2;
      }

      comp._data._chart.resetZoom()
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
        project_id : this.project_id,
      }
      
      return filter
    },

    search1Chart(){

      console.log("search1Chart")
      
      this.lineChartData(1)
      this.multilineChartData(1)
      this.stackedbarChartData(1)
      this.barChartData(1)
      this.pieChartData(1)
      
    },

    search2Chart(){
      
      console.log("search2Chart")
      
      this.lineChartData(2)
      this.multilineChartData(2)
      this.stackedbarChartData(2)
      this.barChartData(2)
      this.pieChartData(2)
      
    },

    async pieChartData (searchArea) { 

      if ( searchArea == 1 ){        
        this.isActivePie1 = true
      } else if ( searchArea == 2 ){
        this.isActivePie2 = true
      }

      let filter = this.getFilter()
      
      try{
        let res = await getChartDataFromStatistics(1, this.project_id, filter, 5)

        if ( searchArea == 1 ){
          this.pChartData1 = getPieChartTemplate(res.x, res.y)
          this.isActivePie1 = false
        }else{
          this.pChartData2 = getPieChartTemplate(res.x, res.y)
          this.isActivePie2 = false
        }

      } catch(err) {
        console.log(err); // TypeError: failed to fatch

        //Stop Loading Spinner
        if ( searchArea == 1 ){        
        this.isActivePie1 = false
        } else if ( searchArea == 2 ){
          this.isActivePie2 = false
        }
      }    
    },
  
    async barChartData (searchArea) {
      // Start Loading Spinner
      if ( searchArea == 1 ){        
        this.isActiveBar1 = true
      } else if ( searchArea == 2 ){
        this.isActiveBar2 = true
      }

      let filter = this.getFilter()

      try {
        let res = await getChartDataFromStatistics(1, this.project_id, filter, 5)      
        if ( searchArea == 1 ){
          this.bChartData1 = getBarChartTemplate(res.x, res.y, res.label)
          this.isActiveBar1 = false
        }else{
          this.bChartData2 = getBarChartTemplate(res.x, res.y, res.label)
          this.isActiveBar2 = false
        }
      } catch (err) {
        
        console.log(err); // TypeError: failed to fatch

        if ( searchArea == 1 ){        
          this.isActiveBar1 = false
        } else if ( searchArea == 2 ){
          this.isActiveBar2 = false
        }
      }

    },

    async stackedbarChartData (searchArea) {

      if ( searchArea == 1 ){        
        this.isActiveStackedBar1 = true
      } else if ( searchArea == 2 ){
        this.isActiveStackedBar2 = true
      }

      let filter = this.getFilter()
      
      try {
        let res = await getLineChartData(2, this.timeCondition, this.project_id, filter)
        if ( searchArea == 1 ){
          this.sbChartData1 = getStackedBarChartTemplate(res.sbarX, res.sbarY_200, res.sbarY_300, res.sbarY_400, res.sbarY_500)
          this.isActiveStackedBar1 = false
        }else{
          this.sbChartData2 = getStackedBarChartTemplate(res.sbarX, res.sbarY_200, res.sbarY_300, res.sbarY_400, res.sbarY_500)
          this.isActiveStackedBar2 = false
        }
      } catch (err) {
        
        console.log(err); // TypeError: failed to fatch

        if ( searchArea == 1 ){        
          this.isActiveStackedBar1 = false
        } else if ( searchArea == 2 ){
          this.isActiveStackedBar2 = false
        }
      }
    },

    // 시계열 분석용 Line Chart
    async lineChartData (searchArea) {

      if ( searchArea == 1 ){        
        this.isActiveLine1 = true
      } else if ( searchArea == 2 ){
        this.isActiveLine2 = true
      }

      try {
        let filter = this.getFilter()
        let res = await getLineChartData(1, this.timeCondition, this.project_id, filter)
        if ( searchArea == 1 ){
          this.lChartData1 = getLineChartTemplate(res.x, res.y, "Request")
          this.isActiveLine1 = false
        }else{
          this.lChartData2 = getLineChartTemplate(res.x, res.y, "Request")
          this.isActiveLine2 = false
        }
      } catch (err) {
        
        console.log(err); // TypeError: failed to fatch

        if ( searchArea == 1 ){        
          this.isActiveLine1 = false
        } else if ( searchArea == 2 ){
          this.isActiveLine2 = false
        }
      }
    },

    // 시계열 분석용 Line Chart
    async multilineChartData (searchArea) {

      if ( searchArea == 1 ){        
        this.isActiveMultiLine1 = true
      } else if ( searchArea == 2 ){
        this.isActiveMultiLine2 = true
      }

      try {
        let filter = this.getFilter()
        let res = await getLineChartData(3, this.timeCondition, this.project_id, filter)
        if ( searchArea == 1 ){
          this.mlChartData1 = getMultiLineChartTemplate(res.x, res.y, "Request", res.yt, "Time-Taken")
          this.isActiveMultiLine1 = false
        }else{
          this.mlChartData2 = getMultiLineChartTemplate(res.x, res.y, "Request", res.yt, "Time-Taken")
          this.isActiveMultiLine2 = false
        }
      } catch (err) {
        
        console.log(err); // TypeError: failed to fatch

        if ( searchArea == 1 ){        
          this.isActiveMultiLine1 = false
        } else if ( searchArea == 2 ){
          this.isActiveMultiLine2 = false
        }
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
.page-container {
    margin: 48px 80px 32px;
    padding: 80px 80px;
    background-color: white;
}
</style>