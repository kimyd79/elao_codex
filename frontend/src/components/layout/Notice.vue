<template>
  <div id="notice">
    <ui-card :columns="10" :height="200">
      <ui-card-item header>Notice</ui-card-item>
      <ui-card-item sub>

        <!-- bar-fade-scale, color="#FF6700" -->
        <vue-element-loading :active="isActive" spinner="spinner" text="Loading.." :is-full-screen="false" color="#553ca5"/>
        <span style="color:red">

          [CHECK] Long Transaction time [1,020 ms] : http://172.16.1.110:8080/#/analysis (Example)         
            
          </span>
          
      </ui-card-item>      
      <ui-card-item body></ui-card-item>

      

    </ui-card>
    
  </div>  
</template>

<script>

import axios from "axios";
import { mapGetters } from "vuex";
import VueElementLoading from 'vue-element-loading'

export default {
  name: "Notice",

    components:{    
    // export Loading Spinner components
      VueElementLoading,

    },

  data() {
    return {
      isActive: true,
    }
  },

  created(){
    
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