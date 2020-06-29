<template>

    <ui-container-box :columns="24" vertical align-center class="page-container">

      <ui-container-box :columns="20" horizontal align-center class="page-title">
        <span class="page-title__label">Compare</span>
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
        <graph :width="800" :height="400"></graph>
        <graph :width="800" :height="400"></graph>
      </ui-container-box>

      <ui-container-box :columns="20" horizontal align-center class="page-form-area">
        <graph :width="800" :height="400"></graph>
        <graph :width="800" :height="400"></graph>
      </ui-container-box>

       <ui-container-box :columns="20" horizontal class="page-tab-area">
        TODO : Footer 영역
      </ui-container-box>

    </ui-container-box>


</template>

<script>
import Graph from '@/components/layout/Graph'
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
    'Info': Info,
    'Notice': Notice, 
    'Search': Search, 
    'SearchCompare1': SearchCompare1,
    'SearchCompare2': SearchCompare2,
    'Statistics': Statistics,
    'Graph': Graph,
  }
}
</script>

<style scoped>

</style>