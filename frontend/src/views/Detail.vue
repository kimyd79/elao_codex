<template>
    <div id="detail">

      <ui-container-box :columns="18" :height="10" vertical class="mt20">
        <Search></Search>
        <GridTable></GridTable>
      </ui-container-box>
    </div>
</template>

<script>
import Search from '@/components/layout/Search'
import GridTable from '@/components/layout/GridTable'


export default {
  name: 'Compare',

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