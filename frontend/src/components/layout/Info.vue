<template>
  <div id="info">
     <ui-card :columns="10" :height="200">
        <ui-card-item header>Information</ui-card-item>
        <ui-card-item sub>
        <span style="color:gray">
          Project Name : {{ this.projectName }}
          <br>
          Logfile Name : {{ this.fileNames }}
          <br>
          LogFormat : {{ this.logFormat }}
          <br>
          Period(Date/Time) : {{ this.dateFromValue }}/{{ this.timeFromValue }} ~ {{ this.dateToValue }}/{{ this.timeToValue }}
        </span>
        </ui-card-item>
        <ui-card-item body></ui-card-item>
      </ui-card>      
    
  </div>
</template>

<script>

import { mapGetters } from "vuex";

export default {
  name: "Info",
  data: function() {
    return {

    };
  },
  created() {
    
  },

  computed: mapGetters({
      
      projectName: "getProjectName",
      fileNames: "getFileNames",
      logFormat: "getLogFormat",

      dateFromValue: "getFromDate",
      dateToValue: "getToDate",
      timeFromValue: "getFromTime",
      timeToValue: "getToTime",

    }),

};
</script>

<style scoped>
</style>