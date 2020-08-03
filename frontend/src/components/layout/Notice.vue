<template>
  <div id="notice">
    <ui-card :columns="10" :height="200">
      <ui-card-item header>Notice</ui-card-item>
      <ui-card-item sub>
        <span
          style="color:red">
          [CHECK] Long Transaction time [1,020 ms] : http://172.16.1.110:8080/#/analysis (Example)</span>
          
      </ui-card-item>      
      <ui-card-item body></ui-card-item>
    </ui-card>
    
  </div>  
</template>

<script>

import axios from "axios";
import { mapGetters } from "vuex";

// Import Loading Spinner component, stylesheet
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

export default {
  name: "Notice",

    components:{    
    // export Loading Spinner components
    'Loading': Loading,
    },

  data() {
    return {
      
     // Loading Spinner data
        isLoading: false,
        fullPage: false
    }
  },

  created(){
    this.getNotice()
  },

  computed: mapGetters({
    projectName: "getProjectName",
    fileNames: "getFileNames",
    logFormat: "getLogFormat",
    logfileID: "getLogFileID",

    dateFromValue: "getFromDate",
    dateToValue: "getToDate",
    timeFromValue: "getFromTime",
    timeToValue: "getToTime"
  }),

  methods: {
    getNotice() {

      var url = "http://127.0.0.1:8000"

      // TODO: common 파일로 뽑아내기, Spinner 추가하기
      let postData = {
        logfile_id: this.logfileID
      };

      // Start Loading Spinner
      this.isLoading = true;
      axios
        .post(url + "/logdetail/notice/", postData)
        .then(res => {
          console.log(res);

          // Stop Loading Spinner
          this.isLoading = false;
        })
        .catch(err => {
          console.error(err);
          // Stop Loading Spinner
          this.isLoading = false;
        });
    }
  }
};
</script>

<style scoped>
</style>