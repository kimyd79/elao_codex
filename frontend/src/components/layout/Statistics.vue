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
              <td>/test1 TODO : 열너비 증가</td>
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
    name: 'Statistics'
}
</script>

<style scoped>

</style>