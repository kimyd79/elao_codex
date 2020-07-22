<template>
  <div id="info">
     <ui-card :columns="10" :height="180">
        <ui-card-item header>Information</ui-card-item>
        <ui-card-item sub>
        <span style="color:blue">
          Project Name : {{ this.projectName }}
          <br>
          Logfile Name : {{ this.fileNames }}
          <br>
          LogFormat : {{ this.logFormat }}
        </span>
        </ui-card-item>
        <ui-card-item body></ui-card-item>
      </ui-card>      
    
  </div>
</template>

<script>
export default {
  name: "Info",
  data: function() {
    return {

      projectName: "",
      fileNames: "",      
      logFormat: ""

    };
  },
  created() {
    
    // Initial Value Setting
    this.projectName = this.$store.state.projectName
    this.fileNames = this.$store.state.fileNames
    this.logFormat = this.$store.state.logFormat
  },

};
</script>

<style scoped>
</style>