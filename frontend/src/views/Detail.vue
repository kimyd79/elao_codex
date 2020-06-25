<template>
    <div id="detail">

      <ui-container-box :columns="18" :height="10" vertical class="mt20">
        <search></search>
        <grid-table></grid-table>
        <graph></graph>

      </ui-container-box>
    </div>
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

    // for Test
    'Graph': Graph,
  },

  methods: {
  },
}
</script>

<style scoped>

</style>