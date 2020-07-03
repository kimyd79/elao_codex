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
        <chart-line :width="800" :height="400"></chart-line>
        <chart-line :width="800" :height="400"></chart-line>
      </ui-container-box>

      <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <chart-stacked-bar :width="800" :height="400"></chart-stacked-bar>
        <chart-stacked-bar :width="800" :height="400"></chart-stacked-bar>
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

import GridTable from '@/components/layout/GridTable'
import Info from '@/components/layout/Info'
import Init from '@/components/layout/Init'
import Notice from '@/components/layout/Notice'
import Search from '@/components/layout/Search'
import SearchCompare1 from '@/components/layout/SearchCompare1'
import SearchCompare2 from '@/components/layout/SearchCompare2'
import Statistics from '@/components/layout/Statistics'

export default {
  name: 'Compare',

  // 컴포넌트 등록
  components:{
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
  }
}
</script>

<style scoped>

</style>