<template>
  <div id="info">
     <ui-card :columns="10" :height="290">
        <ui-card-item header>Information</ui-card-item>
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
  name: "Info"
};
</script>

<style scoped>
</style>