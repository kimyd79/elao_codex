<template>
  <div id="info">
     <ui-card :columns="10" :height="200">
        <ui-card-item header>Information <span style="color:blue">BLUE</span></ui-card-item>
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