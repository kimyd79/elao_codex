<template>
  <div id="notice">    
      <ui-card :columns="10" :height="150">
        <ui-card-item header > Notice (Async)</span></ui-card-item>
        <ui-card-item sub>
          <span style="color:red">
          [CHECK] Long Transaction time [1,020 ms] : http://172.16.1.110:8080/#/analysis (Example)
          </span>
        </ui-card-item>
        <ui-card-item body></ui-card-item>
      </ui-card>    
  </div>
</template>

<script>
export default {
  name: "Notice"
};
</script>

<style scoped>
</style>