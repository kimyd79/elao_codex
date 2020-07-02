<template>
    <div id="statistics">
        <table class="page-summary-table">
          <thead>
            <tr>
              <th rowspan="2" style="width: 180px;">Request Top 1/5</th>
              <th rowspan="2" style="width: 460px;">Request URI</th>
              <th rowspan="2" style="width: 100px;">Count</th>            
            </tr>          
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>/test1</td>
              <td>1000</td>            
            </tr>
            <tr>
              <td>2</td>
              <td>/test2</td>
              <td>100</td>            
            </tr>
            <tr>
              <td>3</td>
              <td>/test3</td>
              <td>50</td>            
            </tr>
            <tr>
              <td>4</td>
              <td>/test4</td>
              <td>50</td>            
            </tr>
            <tr>
              <td>5</td>
              <td>/test5</td>
              <td>50</td>
            </tr>
          </tbody>
        </table>
    </div>
</template>

<script>
export default {
    name: 'Statistics',
    props: ['statisticsRow', 'statisticsKind'],

    data: function() {
      return {

      }
    },

    created() {
      console.log(this.statisticsRow, this.statisticsKind)

      // TODO : 넘어온 데이터로 v-for 이용해서 table 그리기

      // TODO : 데이터 가져오기 (기본 조건값 필요 - 그래야 변경분 반영된다.)    
    },

}
</script>

<style scoped>

</style>