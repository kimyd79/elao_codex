<template>
  <div id="notice">    
      <ui-card :columns="10" :height="290">
        <ui-card-item header>Notice TODO : 붉은색</ui-card-item>
        <ui-card-item sub>
          Lorem Ipsum is simply dummy text of the printing and
          typesetting industry.
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