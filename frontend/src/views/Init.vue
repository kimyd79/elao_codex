<template>
    <div id="menu2">
        This page is menu2
        <Info></Info>
        <Notice></Notice>
        <Search></Search>
        <Statistics></Statistics>
        <Graph></Graph>
    </div>
</template>

<script>
import Graph from '@/components/component/Graph'
import GridTable from '@/components/component/GridTable'
import Info from '@/components/component/Info'
import Init from '@/components/component/Init'
import Notice from '@/components/component/Notice'
import Search from '@/components/component/Search'
import Statistics from '@/components/component/Statistics'

export default {
  name: 'Menu2',

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