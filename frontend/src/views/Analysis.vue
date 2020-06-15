<template>

  <ui-container-box :columns="22" vertical align-center class="page-container">
    <ui-container-box :columns="20" horizontal align-center class="page-title">
      <span class="page-title__label">Analysis</span>
      <span class="page-title__sub">
        Menu1 > LNB Menu1 >
        <em>LNB Sub Menu1</em>
      </span>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal align-center class="page-form-area">
      <Info></Info>
      <Notice></Notice>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">
      <Search></Search>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-form-area">
      <div class="page-summary-title">Statistics</div>
      
      <ui-container-box :columns="5" :height="10" vertical class="mt20">
        <!-- Graph.vue -->
        <Graph></Graph>
        <Graph></Graph>
      </ui-container-box>      

      <ui-container-box :columns="10" vertical class="mt20">
        <!-- Statistics.vue -->
        <Statistics></Statistics>
        <Statistics></Statistics>
      </ui-container-box>

      <ui-container-box :columns="10" vertical class="mt20">
        <!-- Statistics.vue -->
        <Statistics></Statistics>
        <Statistics></Statistics>
      </ui-container-box>
    </ui-container-box>

    <ui-container-box :columns="20" horizontal class="page-tab-area">
      TODO : Footer 영역
    </ui-container-box>
  </ui-container-box>
</template>

<script>
import Graph from "@/components/layout/Graph";
import GridTable from "@/components/layout/GridTable";
import Info from "@/components/layout/Info";
import Init from "@/components/layout/Init";
import Notice from "@/components/layout/Notice";
import Search from "@/components/layout/Search";
import Statistics from "@/components/layout/Statistics";

export default {
  name: "Analysis",

  // 컴포넌트 등록
  components: {
    Info: Info,
    Notice: Notice,
    Search: Search,
    Statistics: Statistics,
    Graph: Graph
  }
};
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