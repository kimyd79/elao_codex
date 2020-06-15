<template>
    <div id="detail">
        This page is Detail
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
  name: 'Detail',

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