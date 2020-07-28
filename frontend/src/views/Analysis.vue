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

import axios from "axios";
import { getPieChartTemplate, getBarChartTemplate, getStackedBarChartTemplate, getLineChartTemplate, 
        getPieChartOptions, getBarChartOptions, getStackedBarChartOptions, getLineChartOptions } from "@/common"

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

      // For ChartData
      axisX: [],
      axisY: [],

      barX: [],
      barY: [],

      sbarX: [],
      sbarY_200: [],
      sbarY_400: [],
      sbarY_500: [],      

      pieX: [],
      pieY: [],

      title:'',
      content:'',

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

  mounted () {

  },
  methods: {

    // 
    getChartDataFromStatistics(type){
      var url = "http://127.0.0.1:8000/logdetail/statistics_top"

          // Top 5 일때
          // type=1. Status Codes Top5
          // type=2. Requests Top5
          // type=3. 최다 404 발생 URL Top5
          // type=4. Time Taken Top5        
          
            this.title = "Top 5"

            switch(type){
              case 1:
                this.content = "HTTP Status Codes(count)"
                break;
              case 2:
                this.content = "Requests URI(count)"
                break;
              case 3:
                this.content = "404 Requests URI(count)"
                break;
              case 4:
                this.content = "Requests Time-taken(ms/㎲)"
                break;
              default:
            }

          let logfile_id = this.$store.state.logFileID
          console.log(logfile_id)

          var url = "http://127.0.0.1:8000/logdetail/statistics_top5/"

          let postData = {
                
                logfile_id: logfile_id,
                type: type
            };

          let axiosConfig = {
                headers: {
                //'Authorization': 'Token '+ this.token // For Django
                }
            };

          axios.post(url, postData, axiosConfig)
          .then(res => {
              console.log(res)
              //this.setItems(res.data.results);
              // 0~4까지 루프돌면서 x[], y[] 만들어야 한다.
              this.barX = []
              this.barY = []

              this.pieX = []
              this.pieY = []

              for (let i = 0; i < res.data.results.length; i++) {
                this.barX.push(res.data.results[i].result);
                this.barY.push(res.data.results[i].result_count);

                this.pieX.push(res.data.results[i].result);
                this.pieY.push(res.data.results[i].result_count);
              }

              console.log(this.barX)
              console.log(this.barY)
          })
          .catch(err => {
              console.error(err); 
          })

    },

    pieChartData () {

      this.getChartDataFromStatistics(1)
      this.pChartData = getPieChartTemplate(this.pieX, this.pieY)
    },
  

    barChartData () {

      this.getChartDataFromStatistics(1)
      this.bChartData = getBarChartTemplate(this.barX, this.barY, this.content)
    },

    stackedbarChartData () {
      
      this.getLineChartData(2)      
      this.sbChartData = getStackedBarChartTemplate(this.sbarX, this.sbarY_200, this.sbarY_400, this.sbarY_500)
    },


    // 시계열 분석용 Line Chart
    getLineChartData(kind=1){
      var url = "http://127.0.0.1:8000/logdetail/chartdata/"

      // TODO : for test
      let logfile_id = this.$store.state.logFileID

      let postData = {
                
          logfile_id: logfile_id,
          
          //Type1 : 시(HH)기준
          //   Kind1 : request(요청) 건수(count)
          //   Kind2 : status code 건수(count)
          //   Kind3 : time-taken 시간(max, min, count)
          //Type2 : 시분(HHMM)기준                    
          //   Kind1 : request(요청) 건수(count)
          //   Kind2 : status code 건수(count)
          //   Kind3 : time-taken 시간(max, min, count)

          type: this.timeCondition,
          kind: kind

      };

      let axiosConfig = {
          headers: {
          //'Authorization': 'Token '+ this.token // For Django
          }
      };

      axios.post(url, postData, axiosConfig)

      .then(res => {
          console.log(res)
          
          if ( kind == 1){
            this.axisX = res.data.resultX
            this.axisY = res.data.resultY 
          } else if ( kind == 2){
            this.sbarX = res.data.resultX
            this.sbarY_200 = res.data.resultY_200
            this.sbarY_400 = res.data.resultY_400
            this.sbarY_500 = res.data.resultY_500

            console.log(this.sbarX)
            console.log(this.sbarY_200)
            console.log(this.sbarY_400)
            console.log(this.sbarY_500)

          }
          
      })
      .catch(err => {
          console.error(err); 
      })

    },

    lineChartData () {

      this.getLineChartData(1)
      this.lChartData = getLineChartTemplate(this.axisX, this.axisY, "Request")       
      
    },
    
  }

};
</script>

<style scoped>
</style>