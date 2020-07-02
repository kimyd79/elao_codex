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
      <span class="page-title__label">Statistics - Top1</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">    
      
      <ui-container-box :columns="10" vertical class="mt20">
        <statistics></statistics>
        <statistics></statistics>
     </ui-container-box>
           
      <ui-container-box :columns="10" vertical class="mt20">
        <statistics></statistics>
        <statistics></statistics>
      </ui-container-box>
      
    </ui-container-box>

    <ui-container-box :columns="20" vertical align-left class="page-title">
      <span class="page-title__label">Statistics - Top5</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">    
      
      <ui-container-box :columns="10" vertical class="mt20">
        <statistics-top :statisticsRow="statisticsRow" :statisticsKind="statisticsKind"></statistics-top>
        <statistics></statistics>
     </ui-container-box>
           
      <ui-container-box :columns="10" vertical class="mt20">
        <statistics></statistics>
        <statistics></statistics>
      </ui-container-box>
      
    </ui-container-box>

    <ui-container-box :columns="20" vertical align-left class="page-title">
      <span class="page-title__label">Charts</span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">
          
      <ui-container-box :columns="10" vertical class="mt20">
        <chart-line></chart-line> 
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
  }
};
</script>

<style scoped>
</style>