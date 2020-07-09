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
        <statistics-top :statisticsRow="5" :statisticsKind="1"></statistics-top>
      </ui-container-box>
      
    </ui-container-box>

    <ui-container-box :columns="20" vertical align-left class="page-title">
      <span class="page-title__label">Charts</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">
          
      <ui-container-box :columns="10" vertical class="mt20">
        <chart-line :chart-data="datacollection" :options="options"></chart-line>
        <button @click="fillData()">Randomize</button> 
        <!-- <chart-line :chart-data="chartdata" :options="options"></chart-line>-->
        <chart-bar></chart-bar>
      </ui-container-box>      

      <ui-container-box :columns="10" vertical class="mt20">
        <chart-stacked-bar></chart-stacked-bar>
        <chart-pie></chart-pie>
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

export default {
  name: "Analysis",

  data(){
    return {
      // For Chart
      // chartdata : [],
      // options : [],

      // For Statistics -> use 'props'
      statisticsRow: "1",   // Top or Top5 (Row 수)
      statisticsKind: "1",  // 전체 처리량 (통계 종류)  

      // for chart reactivess Test
      datacollection: null,
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
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
      this.fillData()
  },
  methods: {
    fillData () {

      var results1 = []
      var results2 = []
0
      for(var i=0 ; i<1000 ; i++){
        results1.push(this.getRandomInt())
        results2.push(this.getRandomInt())
      }

      this.datacollection = {
        //labels: [this.getRandomInt(), this.getRandomInt()],
        labels: results1,
        
        datasets: [          
          {
            label: 'Data One',
            fill: false,
            backgroundColor: '#f87979',
            borderColor: 'rgb(255, 99, 132)',
            //data: [this.getRandomInt(), this.getRandomInt()]
            data: results1
          }, {
            label: 'Data One',
            fill: false,
            backgroundColor: '#f87979',
            borderColor: 'rgba(54, 162, 235, 1)',
            //data: [this.getRandomInt(), this.getRandomInt()]
            data: results2
          }
        ]
      }
    },
    getRandomInt () {
      return Math.floor(Math.random() * (50 - 5 + 1)) + 5
    }
  }

};
</script>

<style scoped>
</style>