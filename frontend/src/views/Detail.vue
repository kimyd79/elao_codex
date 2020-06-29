<template>
    <ui-container-box :columns="24" vertical align-center class="page-container">

    <ui-container-box :columns="20" horizontal align-center class="page-title">
      <span class="page-title__label">Detail</span>
    </ui-container-box>

      <ui-container-box :columns="20" vertical align-center class="page-form-area">
        <search></search>        
      </ui-container-box>

      <ui-container-box :columns="20" vertical align-center class="page-form-area">
        <grid-table></grid-table>
      </ui-container-box>

       <ui-container-box :columns="20" horizontal class="page-tab-area">
        TODO : Footer 영역
      </ui-container-box>
      
    </ui-container-box>

</template>

<script>
import Search from '@/components/layout/Search'
import GridTable from '@/components/layout/GridTable'
import Graph from '@/components/layout/Graph'


export default {
  name: 'Detail',

  // 컴포넌트 등록
  components:{
    'Search': Search, 
    'GridTable': GridTable,
  },

  methods: {
  },
}
</script>

<style scoped>

</style>