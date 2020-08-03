<template>

  <ui-container-box :columns="24" vertical align-center class="page-container-for-init">
  <div class="vld-parent">
    <ui-container-box :columns=12 vertical class="popup-container">
      <CommonPopup :is="currentView" v-on:popupClose="currentView=null"></CommonPopup>
      
            <div class="popup-header">
                <div class="popup-header__title">
                    Initialization
                </div>
                <div class="popup-header__desc">
                    Set initial information for log analysis
                </div>                
            </div>

            <ui-tab box :tabs="tabs" v-on:tabChange="tabChange"/>

            <div class="popup-form">

                <!-- STEP1 start -->
                <span id="step1" v-if="tabs[1].isSelected">
                
                <ui-form-item :columns=11 label="Project" required-left left-label :label-width=144 :label-padding=16>
                    <lego-radio v-model="radioValue" value="1" >New</lego-radio>
                    <lego-radio v-model="radioValue" value="2" v-on:click="getProjects">Exist</lego-radio>
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="Project Name" required-left left-label :label-width=144 :label-padding=16 >
                    <lego-text-field v-model="projectName"/>
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="Project Description" required-left left-label :label-width=144 :label-padding=16 >
                    <lego-text-field textarea rows="3" v-model="projectDescription"/>
                </ui-form-item>

                <!-- GridTable for existing project -->
                <ui-container-box :columns="11" vertical v-if="radioValue == 2">
                  <ui-table header-divider no-action :columns="columns" :items="itemList" class="mt20"></ui-table>
                </ui-container-box>
                <!-- STEP1 end -->
                </span>

                <!-- STEP2 start -->
                <span id="step2" v-if="tabs[2].isSelected">
                <ui-form-item :columns=11 
                    label="File" required-left left-label :label-width=144 :label-padding=16 >
                    <input type="file" id="file" ref="file" v-on:change="selectFile"/>
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="File Size" required-left left-label :label-width=144 :label-padding=16 >
                    {{ fileSize }} bytes
                </ui-form-item>

                <ui-form-item :columns=11 
                    label="File Format" required-left left-label :label-width=144 :label-padding=16>
                  <lego-dropdown :items="items" v-model="fileFormat"/>
                </ui-form-item>

                <ui-form-item :columns="11" label="Data Range" required-left left-label :label-width=144 :label-padding=16 >

                    <lego-radio v-model="dataRangeValue" value="1" >ALL</lego-radio>
                    <lego-radio v-model="dataRangeValue" value="2">Select Range</lego-radio>  

                </ui-form-item>

                <ui-form-item :columns="11" label="" required-left left-label :label-width=144 :label-padding=16 v-if="dataRangeValue == 2">
                    <lego-text-field v-model="dateFromValue" placeholder="YYYYMMDD" />
                    <lego-text-field v-model="timeFromValue" placeholder="hhmmss" />
                    &nbsp;&nbsp;&nbsp;&nbsp;~            
                    <lego-text-field v-model="dateToValue" placeholder="YYYYMMDD" />
                    <lego-text-field v-model="timeToValue" placeholder="hhmmss" />
                  
                </ui-form-item>
                
                <!-- STEP2 end -->
                </span>    

                <!-- Current Info / STEP3 start -->
                <span id="step3" v-if="tabs[0].isSelected | tabs[3].isSelected">
                <ui-form-item :columns=11 
                    label="Project Name" required-left left-label :label-width=144 :label-padding=16 >
                    {{ projectName }}
                </ui-form-item>
                <ui-form-item :columns=11 
                    label="Project Description" required-left left-label :label-width=144 :label-padding=16 >
                    {{ projectDescription }}
                </ui-form-item>
                <ui-form-item :columns=11 
                    label="File" required-left left-label :label-width=144 :label-padding=16 >
                    {{ fileName }}
                </ui-form-item>
                <ui-form-item :columns=11 
                    label="File Format" required-left left-label :label-width=144 :label-padding=16 >
                    {{ fileFormat }}
                </ui-form-item>
                
                <!--
                <ui-form-item :columns=11 
                    label="Data range" required-left left-label :label-width=144 :label-padding=16 >
                    {{ this.dateFromValue }} {{timeFromValue}} ~ {{ dateToValue }} {{timeToValue}}
                </ui-form-item>
                -->

                <!-- STEP3 end -->
                </span>
            </div>            

            <div class="popup-buttons">
                <lego-button v-if="isPrevShow" v-on:click="prevButton">Prev</lego-button>
                <lego-button v-on:click="nextButton" v-model="buttonName" main>{{ buttonName }}</lego-button>
                <lego-button v-on:click="deleteProjects" main>DelProjects</lego-button>
            </div>

        </ui-container-box>
        <!-- Loading Spinner --> 
        <loading :active.sync="isLoading"
          :can-cancel="false"        
          :is-full-page="false"></loading>      
    </div>
  </ui-container-box>
</template>

<script>

import axios from "axios";
import Info from '@/components/layout/Info'
import Init from '@/components/layout/Init'
import Notice from '@/components/layout/Notice'
import Search from '@/components/layout/Search'
import Statistics from '@/components/layout/Statistics'

import * as types from "@/vuex/mutation_types";
import { mapGetters } from "vuex";

//Popup
import CommonPopup from '@/components/layout/CommonPopup';

// Import Loading Spinner component, stylesheet
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

export default {
  name: 'Init',

     // 컴포넌트 등록
  components:{
    'Info': Info,
    'Notice': Notice, 
    'Search': Search, 
    'Statistics': Statistics,
    'CommonPopup': CommonPopup, 
    // export Loading Spinner components
    'Loading': Loading,

  },
  data: function() {
      return {
        buttonName: "Next",
        isPrevShow: false,

        projectName: "",
        projectDescription: "",
        creator: "Leehs",      // TODO : 인증처리 후 사용자 ID입력
        projectID: "",

        fileName: "",
        fileSize: 0,
        fileFormat: "",
        logfileID: "",
        isNewFileAdded: false,

        dateFromValue: "",
        dateToValue: "",
        timeFromValue: "",
        timeToValue: "",

        radioValue: "1",
        dataRangeValue: "1",

        // for file format
        items: [],

          // For file upload
          file: '',

          tabs: [
              { label: "Current Info",  isSelected: true },
              { label: "Step1",  isSelected: false },
              { label: "Step2",  isSelected: false },
              { label: "Step3",  isSelected: false }
          ],

          columns: [
            {label: 'Project Name', key: "projectName", sortable: true, sortValue: "asc", filtable: false, alignRight: false, width: 30 },
            {label: 'Project Description', key: "projectDescription", sortable: true, sortValue: "desc", filtable: true, filterValue:[], alignRight: false, width: 50 },
            {label: 'Creator', key: "creator", sortable: false, filtable: true, filterValue:[], alignRight: false, width: 15, filterList: ["Success","Error","Processing"] },
            {label: 'Created Date', key: "createdDate", sortable: false, filtable: false, alignRight: false, width: 30 },            
          ],

          // Grid Rows
          itemList: [
            //{projectName:'MW LogAnalysys 1', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},
            //{projectName:'MW LogAnalysys 2', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},
            //{projectName:'MW LogAnalysys 3', projectDescription:'LogAnalysys', creator:'Leehs', createdDate:'2020-06-29', isSelected: false},            
            
          ],
        // Loading Spinner data
        isLoading: false,
        fullPage: true,
        // Popup view
        currentView : null,
      }
  },

  created() {
    // TODO : 인증에 대해 처리한다.  
    
    // Initial Value Setting
    this.projectName = this.$store.state.projectName
    this.fileName = this.$store.state.fileNames
    this.fileFormat = this.$store.state.logFormat
    
    // File format 가져오기
    var url = "http://127.0.0.1:8000/logformat"

    let axiosConfig = {
        headers: {
        //'Authorization': 'Token '+ this.token // For Django
        }
    };

    axios.get(url,axiosConfig)
    .then(res => {
               
        for(let i = 0; i < res.data.results.length; i++){
            let tmp = res.data.results[i].format_kind + '/' + res.data.results[i].format_name
            this.items.push({value: tmp + '/' + res.data.results[i].format_strings, text: tmp + ' => ' + res.data.results[i].format_strings });
        }
                        
    })
    .catch(err => {
        console.error(err); 
    })
    
  },

  computed: { 
      
      ...mapGetters({
        isRowChecked: "getToggleSearch"
      }),
  },
      
  methods: {

      selectRow() {

      },

      // For Test : Project 전체 지우기(인자 받으면 1개만 지우기)
      deleteProjects(projectID){
          
          
          let projectIDList = []

          // Get Projects

          let axiosConfig = {
                headers: {
                //'Authorization': 'Token '+ this.token // For Django
                }
            };

          axios.get("http://127.0.0.1:8000/logmaster/",axiosConfig)
          .then(res => {
              console.log(res)

              for(let i = 0; i < res.data.results.length; i++){
                    
                    projectIDList.push(res.data.results[i].project_id);

                    axios.delete('http://127.0.0.1:8000/logmaster/'+res.data.results[i].project_id+'/', axiosConfig)  // '가 아니라 `이다.
                    .then(res => {
                        console.log(res.data)
                    })
                    .catch(err => {
                        console.error(err); 
                    })  
                }              
              
          })
          .catch(err => {
              console.error(err); 
          })

         //console.log(projectIDList)

      },
      
      setItemList(results) {

        this.itemList = [];

        for (let i = 0; i < results.length; i++) {
            this.itemList.push({
                projectName: results[i].project_name,
                projectDescription: results[i].project_description,
                creator: results[i].creator,
                createdDate: results[i].created,
                isSelected: false,
                projectID: results[i].project_id
            })
        }
      },

      getProjects(){          

          var url = "http://127.0.0.1:8000/logmaster/?search="+this.creator

          let axiosConfig = {
                headers: {
                //'Authorization': 'Token '+ this.token // For Django
                }
            };

          axios.get(url,axiosConfig)
          .then(res => {
              console.log(res)
              this.setItemList(res.data.results);
              
          })
          .catch(err => {
              console.error(err); 
          })
      },

      prevButton(){
        if(this.tabs[1].isSelected){
            this.isPrevShow = false
        }else if(this.tabs[3].isSelected){
            this.buttonName = "Next"
            this.isPrevShow = true
        }

        this.tabChange(1)

      },

      nextButton(){

        // Next 버튼 처리
        if(this.tabs[0].isSelected){
            this.isPrevShow = true
        }

        // Logic 처리 : TODO - Global 변수로 뺄 것
        var url = "http://127.0.0.1:8000"       

        if(this.tabs[1].isSelected){          // Step1 : logmaster    

            if(this.radioValue == 1){         // New인 경우 새로운 정보로 저장한다.
                 this.createLogmaster(url);
            }else if(this.radioValue == 2){   // Exist인 경우 기존 정보를 가져온다.
                 
                 // 로그 파일을 추가할 것인가?
                 if(confirm("Need to add another log file?")){
                     // Step2로 이동
                     this.isNewFileAdded = true;
                 }else{
                     // Step3으로 이동 :한번 더 이동시킨다.
                     this.tabChange(2);
                     this.buttonName = "OK"
                     this.isNewFileAdded = false;

                     //선택한 project의 file 정보를 가져온다.
                     this.getLogfile(this.projectID)
                 }
            }
            
        } else if(this.tabs[2].isSelected){   // Step2 : this.projectID

            this.createLogfile(url)
            this.buttonName = "OK"
            this.isNewFileAdded = true;

        } else if(this.tabs[3].isSelected){   // Step3 : this.logfileID

            // TODO : Multi-File 및 기존 project에 File Add시 처리

            // CASE1 : File을 새로 추가한 경우
            if (this.isNewFileAdded){
                this.createLogdetail(url);        
            }else{
            // CASE2 : 기존 File을 이용하는 경우
                this.getLogDetail(this.logfileID)
            }            
        }

        // Tab 변경 - Backward
        this.tabChange(2)
      },

      tabChange(dir){
        
        if( dir == 1 ){ // Forward
            for (let i = 0; i < this.tabs.length; i++) {
                if (this.tabs[i].isSelected == true){
                    if ( i-1 >= 0){
                        this.tabs[i].isSelected = false
                        this.tabs[i-1].isSelected = true
                        break;
                    }
                }
                    
            }
        } else {    // Backward
            for (let i = 0; i < this.tabs.length; i++) {
                if (this.tabs[i].isSelected == true){
                    if ( i+1 < this.tabs.length){
                        this.tabs[i].isSelected = false
                        this.tabs[i+1].isSelected = true
                        break;
                    }
                }
                    
            }
        }


      },

      createLogmaster(url){
          let postData = {
                
                project_name: this.projectName,        
                project_description: this.projectDescription,
                creator: this.creator
            };

            this.$store.dispatch("setProjectName", this.projectName);

            let axiosConfig = {
                headers: {
                //'Authorization': 'Token '+ this.token // For Django
                }
            };

            axios.post(url+"/logmaster/", postData, axiosConfig )
            .then(res => {
                console.log(res)                
                this.projectID = res.data.project_id
                
                // Set in vuex
                this.$store.dispatch("setProjectID", this.projectID);
                
            })
            .catch(err => {
                console.error(err); 
            })
      },

      selectFile(){

        this.file = this.$refs.file.files[0];
        console.log('size=' + this.file.size);
        console.log('name=' + this.file.name);

        this.fileName = this.file.name
        this.fileSize = this.file.size

        this.$store.dispatch("setFileNames", this.fileName);

      },

      createLogfile(url){

            // TODO : Multi-file upload 필요

            let formData = new FormData();
            formData.append('file_object', this.file);
            formData.append('file_name', this.fileName);
            formData.append('file_size', this.fileSize);     


            let splitedFormat = this.fileFormat.split("/")

            formData.append('format_kind', splitedFormat[0]);
            formData.append('format_name', splitedFormat[1]);
            formData.append('file_format', splitedFormat[2]);
            
            formData.append('project', this.projectID);  
            
            this.$store.dispatch("setLogFormat", this.fileFormat);            

            let axiosConfig = {
                headers: {
                    //'Authorization': 'Token '+ this.token // For Django
                    'Content-Type': 'multipart/form-data'
                }
            };

            this.isLoading = true

            axios.post(url+'/logfile/', formData, axiosConfig)
            .then(res => {
                console.log(res)
                
                this.logfileID = res.data.logfile_id

                // Set in vuex
                this.$store.dispatch("setLogFileID", this.logfileID);

                // Stop Loading Spinner
                this.isLoading = false 

                this.$store.dispatch("setPopupKind", 'Noti');
                this.$store.dispatch("setPopupHeader", 'Notification');
                this.$store.dispatch("setPopupBody", 'Get Logfile Upload completed..!!');
                this.$store.dispatch("setPopupButton", 'Close');
                this.currentView = 'CommonPopup';
            })
            .catch(err => {
                console.error(err);
                // Stop Loading Spinner
                this.isLoading = false 
            })
            
      },

      createLogdetail(url){

            let postData = {
                logfile: this.logfileID
            };

            let axiosConfig = {
                headers: {
                //'Authorization': 'Token '+ this.token // For Django
                }
            };

          // TODO : Progress Bar가 필요하다.
          // Start Loading Spinner
          this.isLoading = true 
          axios.post(url+"/logdetail/", postData, axiosConfig )
            .then(res => {
                console.log(res)

                // TODO : 로그의 시작날짜와 시간을 받아와서 vuex에 입력한다.
                //        끝 시간은 동일 시간으로 설정(기본)
                this.$store.dispatch("setFromDate", res.data.start_date);
                this.$store.dispatch("setToDate", res.data.end_date);
                this.$store.dispatch("setFromTime", res.data.start_time);
                this.$store.dispatch("setToTime", res.data.end_time);
                
                // Stop Loading Spinner
                this.isLoading = false 
                
            })
            .catch(err => {
                console.error(err);
                // Stop Loading Spinner
                this.isLoading = false 
            })
      },
      
      getLogfile(projectID){
          
          // http://127.0.0.1:8000/logfile?project=ce447191-fd2c-48b2-8ad6-732e8f7a8543
          var url = "http://127.0.0.1:8000/logfile?project="+projectID

          let axiosConfig = {
                headers: {
                //'Authorization': 'Token '+ this.token // For Django
                }
            };

          axios.get(url,axiosConfig)
          .then(res => {
              console.log(res.data)
              console.log(res.data.results[0])
              console.log(res.data.results[0].file_format)
              console.log(res.data.results[0].file_name)
              
              // TODO : 파일이 없는 경우도 있다. (프로젝트만 만들어놓은 경우)
              //        오류처리 해야 한다.
              this.fileName = res.data.results[0].file_name
              this.fileFormat = res.data.results[0].file_format
              this.logfileID = res.data.results[0].logfile_id

              this.$store.dispatch("setFileNames", this.fileName);
              this.$store.dispatch("setLogFormat", this.fileFormat);
              this.$store.dispatch("setLogFileID", this.logfileID);
          })
          .catch(err => {
              console.error(err); 
          })
      },

      getLogDetail(logfileID){

          console.log("getLogDetail logfileID : "+logfileID)

          var url = "http://127.0.0.1:8000/logdetail/start_end/"

          let postData = {
                logfile_id: logfileID
            };

          this.isLoading = true 
          axios.post(url, postData)
            .then(res => {
                console.log(res)
                
                this.$store.dispatch("setFromDate", res.data.start_date);
                this.$store.dispatch("setFromTime", res.data.start_time);
                this.$store.dispatch("setToDate", res.data.end_date);
                this.$store.dispatch("setToTime", res.data.end_time);
                
                // Stop Loading Spinner
                this.isLoading = false

                this.$store.dispatch("setPopupKind", 'Noti');
                this.$store.dispatch("setPopupHeader", 'Notification');
                this.$store.dispatch("setPopupBody", 'Get Data completed..!!');
                this.$store.dispatch("setPopupButton", 'Close');
                this.currentView = 'CommonPopup';
        
            })
            .catch(err => {
                console.error(err);
                // Stop Loading Spinner
                this.isLoading = false 
            })

      },
  },
  watch: {
      isRowChecked(){
        console.log("Is isRowChecked?")

        // 초기정보 설정 : 기존 project 가져오기          
        this.projectName = this.$store.state.projectName
        this.projectDescription = this.$store.state.projectDescription
        this.projectID = this.$store.state.projectID
        
        this.getLogfile(this.projectID)
      }
  }

}
</script>

<style scoped>
.popup-container {
    padding: 32px;
    border: 1px solid #D0D0D0;
    background-color: white;
}
.popup-header {
    position: relative;
    display: flex;
    flex-flow: column nowrap;
    margin-bottom: 32px;
}
.popup-header__title {
    font-size: 24px;
    font-weight: bold;
}
.popup-header__desc {
    color: #767676;
    margin-top: 16px;
}
.popup-header__close {
    position: absolute;
    top: 0;
    right: 0;
}
.popup-header__close:hover {
    cursor: pointer;
}
.popup-step {
    margin-top: 48px;
}
.popup-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 16px;
}
.popup-form .ui-form-item {
    margin-top: 32px;
}
</style>
