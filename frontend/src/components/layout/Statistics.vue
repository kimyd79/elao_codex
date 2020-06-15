<template>
    <div id="statistics">
        <table class="page-summary-table">
          <thead>
            <tr>
              <th rowspan="2">Request Top3</th>
              <th rowspan="2">Request URI</th>
              <th rowspan="2">Count</th>            
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
.page-container {
  margin: 48px 0 32px;
  padding: 48px 80px;
  background-color: white;
}
.page-title {
  margin-top: 16px;
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid #cccccc;
}
.page-title__label {
  font-size: 32px;
  font-weight: bold;
}
.page-form-area {
  padding: 16px 0;
  border-bottom: 1px solid #cccccc;
}
.page-summary-area {
  margin-top: 48px;
}
.page-summary-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 24px;
}
.page-summary-table {
  border-spacing: 0;
}
.page-summary-table thead th {
  height: 28px;
  border-top: 1px solid #eaeaea;
  font-weight: normal;
  background-color: #f7f7f7;
}
.page-summary-table thead th + th {
  border-left: 1px solid #eaeaea;
}
.page-summary-table tbody td {
  height: 44px;
  text-align: center;
  border-bottom: 1px solid #eaeaea;
}
.page-summary-table tbody tr:first-child td {
  border-top: 1px solid #a5a5a5;
}
.page-summary-table tbody td + td {
  border-left: 1px solid #eaeaea;
}
.page-tab-area {
  margin-top: 60px;
  border-bottom: 1px solid #cccccc;
}
.page-table-area {
  margin: 32px 0 24px;
}
</style>