<template>
    <div id="compare">
        This page is Compare
        <Info></Info>
        <Notice></Notice>
        <Search></Search>
        <Statistics></Statistics>
        <Graph></Graph>
    </div>
</template>

<script>
import Graph from '@/components/layout/Graph'
import GridTable from '@/components/layout/GridTable'
import Info from '@/components/layout/Info'
import Init from '@/components/layout/Init'
import Notice from '@/components/layout/Notice'
import Search from '@/components/layout/Search'
import Statistics from '@/components/layout/Statistics'

export default {
  name: 'Compare',

  // 컴포넌트 등록
  components:{
    'Info': Info,
    'Notice': Notice, 
    'Search': Search, 
    'Statistics': Statistics,
    'Graph': Graph,
  }
}
</script>

<style scoped>

</style>